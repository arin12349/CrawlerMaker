from selenium import webdriver
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
import re

#브라우저
browser=[("드라이버 설정", ("combobox","entry"), ("드라이버 종류를 선택하기", "드라이버의 경로를 입력하기"), ["크롬", "파이어폭스", "인터넷익스플로러"]),
         ("웹 페이지 접속", ("entry",), ("접속할 URL을 입력하기",))
         ]
#제어
action=[("요소 클릭", ("entry",), ("클릭할 요소를 입력하기",)),
         ("요소에 메시지보내기", ("entry", "combobox"), ("요소를 입력하기","보낼 키값을 입력하기"), ["엔터", "스페이스"]),
         ("멈추기", ("entry",), ("멈춰있을 시간을 초단위로 입력하기",))
        ]

#도구
tool=[("동영상 다운로드", ("entry",), ("다운로드할 URL을 입력하기",)),
      ("사진 다운로드", ("entry",), ("다운로드할 URL을 입력하기",))
     ]

control=[("무한반복", (), ()),
         ("횟수 반복하기", ("entry",), ("반복할 횟수를 입력하세요",)),
         ("만약~라면", ("entry",), ("조건을 입력하세요",)),]

#function list
findfunc = ["find_element_by_xpath", "find_elements_by_xpath"]
setfunc = ["webdriver.Chrome","get"]
timefunc = ["time.sleep"]

first_list = findfunc + setfunc + timefunc

second_list=[]

findsec = ["click", "send_keys"]
third_list=[]

global code
code = [('webdriver.Chrome', 'chromedriver.exe', '')]

#color
browserbg="#ffc742"
actionbg="#ff7575"
toolbg="#75a2ff"
controlbg="#b0ffa8"

def newcreate():
    code.delete()
    listbox.delete(0, END)

def filesave():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("text files", "*.txt"),("all files", "*.*")))
        
    print(filename)
    file = open(filename+".txt", 'w')

    vstr = ''
    sep = " "
    

    for a in code.lista :

        for b in a  :     

            vstr = vstr + str(b) + sep

        vstr = vstr.rstrip(sep)  # 마지막에도 추가되는  sep을 삭제 

        vstr = vstr + '\n'

    

    file.writelines(vstr)          # 한 라인씩 저장 

        

    file.close()




def fileload():
    try:
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("text files", "*.txt"),("all files", "*.*")))
        lista = []
        newcreate()
        print(filename)
        data=open(filename,'rt',encoding="utf-8")
        while True:
            line = data.readline()
            if not line:
                break
            line =line.rstrip("\n")
            line = line.split(" ")
            if len(line) == 2:
                line.append("")
            lista.append(tuple(line))
        code.lista = lista
        redraw()
    except:
        pass

def redraw():
    for lista in code.lista:
        func, text, method = lista
        print(make(func, text, method))
        listbox.insert(END, (make(func, text, method)))
    
class codelist():
    def __init__(self, lista):
        self.lista = lista
    
    def codeget(self):
        codes = []
        for a in self.lista:
            func, text, method = a
            code = make(func, text, method)
            codes.append(code)

        return codes

    
    def entryget(self, num):
        num, = num
        func, text, method = self.lista[num]
        return (func, text, method)

    def append(self, func, text, method):
        self.lista.append((func, text, method))

    def delete(self):
        self.lista = []
        

class Command():
    def __init__(self, name, color, entry):
        self.name = name
        self.color = color
        self.entry = entry

class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        #self.bind("<Return>", self.enter)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            try:
                self.lb.destroy()
            except:
                pass
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    #def enter(self, event):
    #    words = self.lb.get(ACTIVE)
    #    self.var.set(words)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]


def entrychange(*args):
    func = entry.var.get()
    print(func)
    if func in findfunc:
        third_list = findsec
        entry3.lista = third_list
    
def append():
    func = entry.get()
    text = entry2.get()
    method = entry3.get()

    #if no text
    if func == "":
        if text =="":
            if method=="":
                return print("Enter the text")
            
    #add to code
    code.append(func, text, method)
    listbox.insert(END, (make(func, text, method)))
    print(code.lista)

def make(func, text, method):
    if method == "":
        pass
    else:
        string = "driver."+func+"(\""+text+"\")."+method+"()"

    if func == "webdriver.Chrome":
        string = "driver="+func+"(\""+text+"\")"
    if func == "time.sleep":
        string = func+"("+text+")"
        
    print(string)
    return string

def launch():
    for i in code.codeget():
        print(i)
        exec(i)

def close():
    UI.quit()
    UI.destroy()

def buttonclick(btn):
    commandframe.destroy()
    commandframeupdate()
    text = btn.cget("text")
    bg = btn.cget("bg")
    commandframechange(text, bg)

def commandframechange(text, bg):
    commandtext.configure(text = text, bg=bg)
    commandframe.configure(bg=bg)
    child=[]
    lists=()
    print(text)
    for i in browser+action+tool+control:
        if text == i[0]:
            lists=i[1]
            textlists=tuple(i[2])
            print(lists)
            print(textlists)

    #draw
    entryx=5
    entryy=50
    for i in lists:
        if i == 'entry':
            entry = Entry(commandframe)
            entry.place(x=entryx, y=entryy, width= 200, height= 25)
        elif i == 'combobox':
            for i in browser+action+tool+control:
                if text == i[0]:
                    combolist=i[3]
            combobox = ttk.Combobox(commandframe, values=combolist)
            combobox.place(x=entryx, y=entryy, width= 200, height= 25)
        entryx+=218
    entryx=5
    entryy=50
    for i in textlists:
        print(i)
        label=Label(commandframe, text=i)
        label.place(x=entryx, y=25)
        entryx+=218

def commandframeupdate():
    global commandframe
    global commandtext
    commandframe = Frame(UI, bg='white', relief="solid", borderwidth=1)
    commandframe.place(x=230, y=10, width= 650, height=80)

    commandtext = Label(commandframe,bg='white',text="None")
    commandtext.place(x=5, y=5)
    
def draw(canvas, lista, color):
    iy= 30
    for i in lista:
        button= Button(canvas, text=i[0], bg=color)
        button.configure(command=lambda btn=button: buttonclick(btn))
        canvas.create_window(90, iy, window=button)
        iy+=40
        
#setting
UI = Tk()
UI.title("CrollerMaker Ver 1.0")
UI.geometry("1000x500+100+100")
UI.resizable(False, False)

#임시 리스트
code = codelist(code)

entryx = 5
entryy = 50

buttonx = 890

#왼쪽

notebook = ttk.Notebook(UI, width=200, height= 450)
notebook.place(x=10, y=10)

frame1=Frame(UI)
notebook.add(frame1, text="브라우저" )


frame2=Frame(UI)
notebook.add(frame2, text="동작")

frame3=Frame(UI)
notebook.add(frame3, text="도구")

frame4=Frame(UI)
notebook.add(frame4, text="제어")


h1 = Scrollbar(frame1, orient=VERTICAL)
h2 = Scrollbar(frame2, orient=VERTICAL)
h3 = Scrollbar(frame3, orient=VERTICAL)
h4 = Scrollbar(frame4, orient=VERTICAL)

canvas1 = Canvas(frame1, width=200, height=450, bg="white", yscrollcommand=h1.set)
canvas1.config(scrollregion=(0,0, 1000, 1000))
canvas2 = Canvas(frame2, width=200, height=450, bg="white", yscrollcommand=h2.set)
canvas2.config(scrollregion=(0,0, 1000, 1000))
canvas3 = Canvas(frame3, width=200, height=450, bg="white", yscrollcommand=h3.set)
canvas3.config(scrollregion=(0,0, 1000, 1000))
canvas4 = Canvas(frame4, width=200, height=450, bg="white", yscrollcommand=h4.set)
canvas4.config(scrollregion=(0,0, 1000, 1000))



h1.pack(side="right", fill="y")
h2.pack(side="right", fill="y")
h3.pack(side="right", fill="y")
h4.pack(side="right", fill="y")
h1.config(command=canvas1.yview)
h2.config(command=canvas2.yview)
h3.config(command=canvas3.yview)
h4.config(command=canvas4.yview)
canvas1.pack(side=TOP, fill=BOTH, expand=1)
canvas2.pack(side=TOP, fill=BOTH, expand=1)
canvas3.pack(side=TOP, fill=BOTH, expand=1)
canvas4.pack(side=TOP, fill=BOTH, expand=1)

draw(canvas1, browser, browserbg)
draw(canvas2, action, actionbg)
draw(canvas3, tool, toolbg)
draw(canvas4, control, controlbg)


#오른쪽

global commandframe
global commandtext

commandframeupdate()


#entry = AutocompleteEntry(first_list, commandframe)
#entry.var.trace("w", entrychange)
#entry.place(x=entryx, y=entryy, width= 200, height= 25)

#entry2 = AutocompleteEntry(second_list ,commandframe)
#entry2.place(x=entryx+218, y=entryy, width=200, height= 25)

#entry3 = AutocompleteEntry(third_list, commandframe)
#entry3.var.trace("w", entrychange)
#entry3.place(x=entryx+436, y=entryy, width = 200, height= 25)

button = Button(UI, text="실행", command = launch)
button.place(x= buttonx, y=entryy, width= 100)

button = Button(UI, text="추가", command = append)
button.place(x= buttonx, y=entryy+30, width= 100)

button = Button(UI, text="초기화")
button.place(x= buttonx, y=entryy+60, width= 100)


menubar=Menu(UI, relief="solid")

menu_1=Menu(menubar, tearoff=0)
menu_1.add_command(label="새로 만들기", command=newcreate)
menu_1.add_separator()
menu_1.add_command(label="불러오기", command=fileload)
menu_1.add_separator()
menu_1.add_command(label="저장하기", command=filesave)
menu_1.add_separator()
menu_1.add_command(label="종료", command=close)
menubar.add_cascade(label="File", menu=menu_1)

menu_2=Menu(menubar, tearoff=0, selectcolor="red")
menu_2.add_radiobutton(label="하위 메뉴 2-1", state="disable")
menu_2.add_separator()
menu_2.add_radiobutton(label="하위 메뉴 2-2")
menu_2.add_separator()
menu_2.add_radiobutton(label="하위 메뉴 2-3")
menubar.add_cascade(label="Edit", menu=menu_2)

menu_3=Menu(menubar, tearoff=0)
menu_3.add_checkbutton(label="하위 메뉴 3-1")
menu_3.add_separator()
menu_3.add_checkbutton(label="하위 메뉴 3-2")
menubar.add_cascade(label="Options", menu=menu_3)

menu_4=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=menu_4)


UI.config(menu=menubar)

######################################################

def entryfill(event):
    cur = listbox.curselection()
    print(cur)
    func, text, method = code.entryget(cur)
    entry.var.set(func)
    entry.lb.destroy()
    entry2.var.set(text)
    entry3.var.set(method)

def selection():
    cur = listbox.selection_get()
    try:
        dictionary[cur](cur)
    except:
        pass


items = StringVar(value=tuple(code.codeget()))

listbox = Listbox(UI, listvariable=items, width=90, height=24)
listbox.place(x=230, y=95)
listbox.focus()

#listbox.bind('<Double-1>', lambda x: selectButton.invoke())
listbox.bind('<Double-1>', entryfill)

######################################################

UI.mainloop()
