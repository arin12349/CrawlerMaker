from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import os

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

#검색어
key = input("Keyword :")
#몇개
num = int(input("Count :"))

url = "www.google.com"
imglocation = "//div[@data-ri="
foldername = "구글링/"
driver = webdriver.Chrome('chromedriver.exe', options=options)

driver.get("https://www.google.com/search?q="+key+"&newwindow=1&hl=ko&sxsrf=ALeKk00NSloGVparepValutM-_K2ZzVJaA:1600753254571&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj09vHIhvzrAhXKFogKHSUKABEQ_AUoAXoECBsQAw&biw=1920&bih=969")
action = ActionChains(driver)


#디렉토리 만들기
def createDIR():
    try:
        if not(os.path.isdir(foldername)):
            os.makedirs(os.path.join(foldername))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

createDIR()

for i in range(num):
    #이미지 1~num 까지 찾기
    try:
        tag = imglocation+"'"+str(i)+"']/a/div/img"
        #action.move_to_element(driver.find_element_by_xpath(tag)).perform()
        target = driver.find_element_by_xpath(tag)
        target.location_once_scrolled_into_view
        img = driver.find_element_by_xpath(tag)
        src = img.get_attribute('src')
        print(src)
        urllib.request.urlretrieve(src, foldername+key+str(i+1)+".png")
    except:
        num+=1

driver.quit()
