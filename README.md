# CrawlerMaker
 I made crawler making into a tool that makes it easier to learn for education.   
 The basic design refers to scratch, an educational language.
 
## Test Video
 https://blog.naver.com/arin12349/222220340648
 
## How to Use
 install CrawlerMaker.py
 
1. Choose the action you want   
 ![image](https://user-images.githubusercontent.com/65750019/171865430-6224c2fe-04a7-4fab-965a-ea500c06a380.png)   
 
2. Fill in the blanks in the Action   
 ![image](https://user-images.githubusercontent.com/65750019/171865642-b920a139-da97-41c6-9840-2b1e685fb3d8.png)   
3. Choose more action or crawler start   
![image](https://user-images.githubusercontent.com/65750019/171865860-a15ccc42-ec17-45df-b435-e855351222b9.png)

## Technologies
 ### Block Coding
 The crawler's movements were made easier and more visible in the form of blocks.
 
 ### Crawler actions
 There are simple crawling actions and additional deletion is easy if desired.
 ``` PY
 def imgdownload(url, keywords):
    keywords = keywords + ".png"
    urllib.request.urlretrieve(url, keywords)
    print("Save Sucess")
 ```
 
 ### File save and Load
 You can load or save the crawling actions you create.
