from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import time

melon = "https://www.melon.com/chart/index.htm"
folder = "멜론차트/"
num = 30
driver = webdriver.Chrome('chromedriver.exe')

def melonchart():
    driver.get(melon)
    #rank = driver.find_element_by_xpath("//form[@id='frm']/div/table/tbody")
    #ranking = rank.find_elements_by_tag_name("tr")
    #타이틀
    title = driver.find_elements_by_xpath("//div[@class='ellipsis rank01']/span/a")
    #가수
    singer = driver.find_elements_by_xpath("//div[@class='ellipsis rank02']/a")
    #num까지 순위의 차
    for i in range(num):
        print(i+1)
        print(title[i].text)
        print(singer[i].text)
        print("================================")

    write(title, singer)

def write(title, singer):
    now = time.localtime()
    name = "%04d%02d%02d %02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    f = open(folder+name+".txt", "w")
    f.write(name+"\n")
    f.write("=====================================\n")

    #순위 적기
    for i in range(num):
        f.write(str(i+1)+"\n")
        f.write(title[i].text+"\n")
        f.write(singer[i].text+"\n")
        f.write("=====================================\n")

melonchart()

