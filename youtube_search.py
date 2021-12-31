from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
import pytube
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
foldername = "유튜브영상/"

def createDIR():
    try:
        if not(os.path.isdir(foldername)):
            os.makedirs(os.path.join(foldername))
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

createDIR()

url = "http://www.youtube.com"
driver = webdriver.Chrome('chromedriver.exe', options=options)

def download(url, keywords):
    print("Downloading . . .")
    yt = pytube.YouTube(url)
    video = yt.streams.filter(only_audio = True)[0]
    video.download(output_path='유튜브영상/', filename = keywords)
    print("Downloading Sucess")

#검색어
keywords = input("Keyword : ")

driver.get(url)

#검색
driver.find_element_by_xpath("//input[@id='search']").send_keys(keywords)
driver.find_element_by_xpath("//button[@id='search-icon-legacy']").click()

#유튜브 영상들리스트
time.sleep(.5)
youtube = driver.find_elements_by_xpath("//ytd-video-renderer[@class='style-scope ytd-item-section-renderer']")

#첫번째 영상
first = youtube[0].find_element_by_xpath("//a[@id='video-title']").click()

#현재 url 저장후 다운로드
current_url = driver.current_url
download(current_url, keywords)
driver.quit()


