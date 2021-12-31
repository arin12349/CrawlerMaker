from selenium import webdriver
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
import re
from selenium.webdriver.common.keys import Keys
import pytube
import urllib.request
from PIL import Image
import tkinter.font as font
import os

#브라우저
browser=[("드라이버 설정", ("combobox","entry"), ("드라이버 종류를 선택하기", "드라이버의 경로를 입력하기"), ["크롬", "파이어폭스", "인터넷익스플로러"]),
         ("웹 페이지 접속", ("entry",), ("접속할 URL을 입력하기",)),
         ("드라이버 종료", ("",),())
         ]
#제어
action=[("요소 클릭", ("entry",), ("클릭할 요소를 입력하기",)),
         ("요소에 키보드입력하기", ("entry", "combobox"), ("요소를 입력하기","보낼 키값을 입력하기"), ["엔터", "스페이스"]),
         ("멈추기", ("entry",), ("멈춰있을 시간을 초단위로 입력하기",))
        ]

#도구
tool=[("동영상 다운로드", ("entry", "entry"), ("다운로드할 URL을 입력하기", "저장할 이름 입력하기")),
      ("사진 다운로드", ("entry", "entry"), ("다운로드할 URL을 입력하기", "저장할 이름 입력하기")),
      ("유튜브 동영상 다운로드", ("entry", "button"), ("검색어 입력하기", "저장할 경로 입력하기")),
      ("구글 사진 다운로드", ("entry", "entry", "button"), ("검색어 입력하기", "저장할 갯수 입력하기", "저장할 경로 입력하기"))
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

global blocklist
blocklist = []

global framelist
framelist = []

global textlists

global driver
global handleblock
handleblock = ""

#color
browserbg="#ffc742"
actionbg="#ff7575"
toolbg="#75a2ff"
controlbg="#b0ffa8"

def folder(event):
    folder = filedialog.askdirectory()
    print(folder)
    print(buttonentry)
    buttonentry.insert(0, folder)
    return folder

def filesave():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("text files", "*.txt"),("all files", "*.*")))
        
    print(filename)
    file = open(filename+".txt", 'w')

    vstr = ''
    sep = "|"
    

    #for a in code.lista :

    #    for b in a  :     

    #        vstr = vstr + str(b) + sep

    #    vstr = vstr.rstrip(sep)  # 마지막에도 추가되는  sep을 삭제 

    #    vstr = vstr + '\n'

    for i in blocklist:
        vstr = vstr + i.whatis + sep
        for i1 in i.lista:
            vstr = vstr + i1 + sep

        vstr = vstr.rstrip(sep)
        vstr = vstr + '\n'
    print(vstr)
    file.writelines(vstr)          # 한 라인씩 저장 

        

    file.close()




def fileload():
    try:
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",filetypes=(("text files", "*.txt"),("all files", "*.*")))
        lista = []
        clear()
        print(filename)
        data=open(filename,'rt',encoding="euc-kr")
        while True:
            line = data.readline()
            if not line:
                break
            line =line.rstrip("\n")
            line = line.split("|")
            if len(line) <= 3:
                while True:
                    line.append("")
                    if len(line) == 4:
                        break
            print(line)
            lista.append(tuple(line))
    except:
        pass
    for i in lista:
        print(i)
        whatis, a, b, c = i
        lists = [a,b, c]
        print(lists)
        blocklist.append(block(whatis, lists))
    canvasredraw()
    print(lista)
    canvasredraw()

def redraw():
    for lista in code.lista:
        func, text, method = lista
        print(make(func, text, method))
        listbox.insert(END, (make(func, text, method)))

#동영상 다운로드
def mp3download(url, keywords):
    print("Downloading . . .")
    print(url)
    yt = pytube.YouTube(url)
    video = yt.streams.filter(only_audio = True)[0]
    video.download(filename = keywords)
    print("Downloading Sucess")

#이미지 다운로드
def imgdownload(url, keywords):
    keywords = keywords + ".png"
    urllib.request.urlretrieve(url, keywords)
    print("Save Sucess")

#유튜브 다운로드
def youtubedownload(keywords, folder=""):
    if not folder == "":
        createDIR(folder)
    #검색
    driver.get("http://youtube.com")
    driver.find_element_by_xpath("//input[@id='search']").send_keys(keywords)
    driver.find_element_by_xpath("//button[@id='search-icon-legacy']").click()

    #유튜브 영상들리스트
    time.sleep(2)
    youtube = driver.find_elements_by_xpath("//ytd-video-renderer[@class='style-scope ytd-item-section-renderer']")

    #첫번째 영상
    first = youtube[0].find_element_by_xpath("//a[@id='video-title']").click()

    #현재 url 저장후 다운로드
    url = driver.current_url
    yt = pytube.YouTube(url)
    video = yt.streams.filter(only_audio = True)[0]
    video.download(output_path=folder+"/", filename = keywords)
    print("Downloading Sucess")

#구글 이미지 다운로드
def googledownload(keywords, num, folder=""):
    if not folder == "":
        createDIR(folder)
        folder=folder+"/"
    num = int(num)
    driver.get("https://www.google.com/search?q="+keywords+"&newwindow=1&hl=ko&sxsrf=ALeKk00NSloGVparepValutM-_K2ZzVJaA:1600753254571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj09vHIhvzrAhXKFogKHSUKABEQ_AUoAXoECBsQAw&biw=1920&bih=969")
    for i in range(num):
    #이미지 1~num 까지 찾기
        try:
            tag = "//div[@data-ri="+"'"+str(i)+"']/a/div/img"
            #action.move_to_element(driver.find_element_by_xpath(tag)).perform()
            target = driver.find_element_by_xpath(tag)
            target.location_once_scrolled_into_view
            img = driver.find_element_by_xpath(tag)
            src = img.get_attribute('src')
            print(src)
            print(folder+"/"+keywords+str(i+1)+".png")
            urllib.request.urlretrieve(src, folder+keywords+str(i+1)+".png")
        except:
            num+=1

def createDIR(foldername):
    try:
        if not(os.path.isdir(foldername)):
            os.makedirs(os.path.join(foldername))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

 
#캔버스안에 블록들
class block():
    def __init__(self, whatis="", lista=[], indexlista=()):
        self.whatis = whatis
        browserbg="#ffc742"
        actionbg="#ff7575"
        toolbg="#75a2ff"
        controlbg="#b0ffa8"
        for i in browser:
            if self.whatis == i[0]:
                self.color = browserbg
        for i in action:
            if self.whatis == i[0]:
                self.color = actionbg
        for i in tool:
            if self.whatis == i[0]:
                self.color = toolbg
        for i in control:
            if self.whatis == i[0]:
                self.color = controlbg
        
        self.lista = lista
        self.indexlista = indexlista
        self.first = lista[0]
        self.second = lista[1]
        self.third = lista[2]
        try:
            self.firstindex = indexlista[0]
            self.secondindex = indexlista[1]
            self.thirdindex = indexlista[2]
        except:
            pass
        
    #make code
    def make(self):
        text = self.whatis

        #브라우저
        if text == "드라이버 설정":
            if self.first == "파이어폭스":
                first = "Firefox"
            elif self.first == "크롬":
                first = "Chrome"
            elif self.first == "인터넷익스플로러":
                frist = "Ie"
            string = "global driver; driver = webdriver."+first+"(\'"+self.second+"\')"

        elif text == "웹 페이지 접속":
            string = "driver.get"+"(\'"+self.first+"\')"

        elif text == "드라이버 종료":
            string = "driver.quit()"

        #동작
        elif text == "요소 클릭":
            string = "driver.find_element_by_xpath"+"(\'"+self.first+"\').click()"
            
        elif text == "요소에 키보드입력하기":
            if self.second == "엔터":
                string = "driver.find_element_by_xpath"+"(\'"+self.first+"\').send_keys(Keys.ENTER)"
                
            elif self.second == "스페이스":
                string = "driver.find_element_by_xpath"+"(\'"+self.first+"\').send_keys(Keys.SPACE)"

            else:
                string = "driver.find_element_by_xpath"+"(\'"+self.first+"\').send_keys(\'"+self.second+"\')"

        elif text == "멈추기":
            string = "time.sleep("+self.first+")"
        #도구
        if text == "동영상 다운로드":
            string = "mp3download(\'"+self.first+"\',\'"+self.second+"\')"

        elif text == "사진 다운로드":
            string = "imgdownload(\'"+self.first+"\',\'"+self.second+"\')"
            
        elif text == "유튜브 동영상 다운로드":
            string = "youtubedownload(\'"+self.first+"\',\'"+self.second+"\')"

        elif text == "구글 사진 다운로드":
            string = "googledownload(\'"+self.first+"\',\'"+self.second+"\',\'"+self.third+"\')"
        #제어

        return string

    def draw(self, x, y):
        frame = Frame(canvas5, bg= self.color, relief="solid", borderwidth=1)
        frame.bind("<Button-1>",self.click)
        commandtext = Label(frame,bg=self.color,text=self.whatis)
        commandtext.place(x=5, y=5)
        for i in browser+action+tool+control:
            if self.whatis == i[0]:
                lists=i[1]
                textlists=tuple(i[2])
                try:
                    comboboxvalue = i[3]
                except:
                    pass
        entryx=5
        entryy=50
        num = 0
        for i in self.lista:
            if i == "":
                break
            label = Label(frame, text=i, bg='white')
            label.place(x=entryx, y=entryy, width= 200, height= 25)
            entryx+=218
            num +=1
        entryx=5
        entryy=50
        for i in textlists:
            if i == "":
                break
            print(i)
            label=Label(frame, text=i, bg='white')
            label.place(x=entryx, y=25)
            entryx+=218
        canvas5.create_window(x, y, window=frame, width= 640, height=80)

    def click(self, event):
        global handleblock
        print(self.whatis+"클릭")
        handleblock = self
        commandframe.destroy()
        commandframeupdate()
        print(self.lista)
        commandframechange(self.whatis, self.color, self.lista)

    def change(self, lista):
        self.lista = lista
        self.first = lista[0]
        self.second = lista[1]
        self.third = lista[2]
    
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
    
#def append():
#    func = entry.get()
#    text = entry2.get()
#    method = entry3.get()

    #if no text
#    if func == "":
#        if text =="":
#            if method=="":
#                return print("Enter the text")
            
    #add to code
#    code.append(func, text, method)
#    listbox.insert(END, (make(func, text, method)))
#print(code.lista)

def append():
    lista = ["","", ""]
    indexlista = ["", "", ""]
    text = commandtext.cget("text")
    num = 0
    for i in framelist:
        lista[num]=(i.get())
        num+=1
    num = 0
    for i in textlists:
        indexlista[num]=i
        num+=1
    if not text == "드라이버 종료":
        if lista[0] == "":
            print("Error:  입력을 다 채워주세요")
            return
    blocklist.append(block(text, lista, indexlista))
    canvasredraw()

def change():
    global handleblock
    print(handleblock)
    if not handleblock == "":
        lista = ["","", ""]
        num = 0
        text = commandtext.cget("text")
        for i in framelist:
            lista[num]=(i.get())
            num+=1
        if not text == "드라이버 종료":
            if lista[0] == "":
                print("Error:  입력을 다 채워주세요")
                return
        handleblock.change(lista)
        canvasredraw()
    
def canvasredraw():
    canvas5.delete("all")
    x=325
    y=44
    for i in blocklist:
       i.draw(x, y)
       print(x, y)
       y+=85
    
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
    for i in blocklist:
        print(i.make())
        exec(i.make())

def close():
    UI.quit()
    UI.destroy()

def buttonclick(btn):
    commandframe.destroy()
    commandframeupdate()
    global handleblock
    handleblock = ""
    text = btn.cget("text")
    bg = btn.cget("bg")
    commandframechange(text, bg)

def commandframechange(text, bg, valuelista=["", "", ""]):
    commandtext.configure(text = text, bg=bg)
    commandframe.configure(bg=bg)
    child=[]
    lists=()
    print(text)
    global textlists
    textlist = ""
    for i in browser+action+tool+control:
        if text == i[0]:
            lists=i[1]
            textlists=tuple(i[2])
            try:
                comboboxvalue = i[3]
            except:
                pass
    print("change")
    print(valuelista)
    #draw
    entryx=5
    entryy=50
    num = 0
    global framelist
    framelist = []
    for i in lists:
        if i == 'entry':
            v = StringVar(UI, value=valuelista[num])
            framelist.append(Entry(commandframe, textvariable=v))
            framelist[num].place(x=entryx, y=entryy, width= 200, height= 25)
        elif i == 'combobox':
            for i in browser+action+tool+control:
                if text == i[0]:
                    combolist=i[3]
            combobox = ttk.Combobox(commandframe, values=combolist)
            if not valuelista[num] == "":
                combobox.current(comboboxvalue.index(valuelista[num]))
            framelist.append(combobox)
            framelist[num].place(x=entryx, y=entryy, width= 200, height= 25)
        elif i == "button":
            global buttonentry
            v = StringVar(UI, value=valuelista[num])
            buttonentry = Entry(commandframe, textvariable=v)
            button = Button(commandframe, text="찾기")
            button.bind("<Button-1>", lambda btn=button: folder(btn))
            #button.configure(command=lambda btn=button: folder(btn))
            framelist.append(buttonentry)
            framelist[num].place(x=entryx, y=entryy, width= 200, height= 25)
            button.place(x=entryx+170, y=25, width= 30, height = 25)
        entryx+=218
        num +=1
    entryx=5
    entryy=50
    for i in textlists:
        print(i)
        label=Label(commandframe, bg='white', text=i)
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
        iy+=50

def clear():
    global blocklist
    blocklist=[]
    canvasredraw()
    
#setting
UI = Tk()
UI.title("CrollerMaker Ver 1.0")
UI.geometry("1010x500+100+100")
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

myFont = font.Font(size=15)


#launchimage = PhotoImage(file = "launch.png")
#button = Button(UI, text="실행", command = launch, image=launchimage)
button = Button(UI, text="실행", command = launch)
button['font'] = myFont
button.configure(background='white')
button.place(x= buttonx+25, y=10, width= 80, height = 60)

#appendimage = PhotoImage(file = "append.png")
#button = Button(UI, text="추가", command = append, image=appendimage)
button = Button(UI, text="추가", command = append)
button.configure(background='white')
button['font'] = myFont
button.place(x= buttonx+25, y=80, width= 80, height = 60)

button = Button(UI, text="수정", command = change)
button.configure(background='white')
button['font'] = myFont
button.place(x= buttonx+25, y=150, width= 80, height = 60)

#clearimage = PhotoImage(file = "clear.png")
#button = Button(UI, text="초기화", command = clear, image=clearimage)
button = Button(UI, text="초기화", command = clear)
button['font'] = myFont
button.configure(background='white')
button.place(x= buttonx+25, y=420, width= 80, height = 60)


menubar=Menu(UI, relief="solid")

menu_1=Menu(menubar, tearoff=0)
menu_1.add_command(label="새로 만들기", command=clear)
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

#listbox = Listbox(UI, listvariable=items, width=90, height=24)
#listbox.place(x=230, y=95)
#listbox.focus()

#listbox.bind('<Double-1>', lambda x: selectButton.invoke())
#listbox.bind('<Double-1>', entryfill)


frame5 = Frame(UI)
frame5.place(x=228, y=96)
h5 = Scrollbar(frame5, orient=VERTICAL)

global canvas5
canvas5 = Canvas(frame5, width=650, height=380, bg="gray", yscrollcommand=h5.set)
canvas5.config(scrollregion=(0,0, 0, 1000))
h5.pack(side="right", fill="y")
h5.config(command=canvas5.yview)
canvas5.pack(side=TOP, fill=BOTH, expand=1)
######################################################

UI.mainloop()
