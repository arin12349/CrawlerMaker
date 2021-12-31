import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import pyperclip
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

url = "http://www.naver.com"

#ID PASS
USERID = ""
PASSWORD = ""


driver = webdriver.Chrome('chromedriver.exe')
driver.get(url)

time.sleep(2)
#로그인 버튼
driver.find_element_by_xpath("//i[@class='ico_naver']").click()

time.sleep(.5)

#id
driver.find_element_by_xpath("//input[@name='id']").click()
for i in USERID:
    time.sleep(random.uniform(0,1))
    driver.find_element_by_xpath("//input[@name='id']").send_keys(i)
    
#password
time.sleep(.5)
driver.find_element_by_xpath("//input[@name='pw']").click()
for i in PASSWORD:
    time.sleep(random.uniform(0,1))
    driver.find_element_by_xpath("//input[@name='pw']").send_keys(i)

#click login button
driver.find_element_by_xpath("//input[@title='로그인']").click()
