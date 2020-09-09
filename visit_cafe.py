from selenium import webdriver
import sys, os, time

URL = 'http://cafe.daum.net/trotidol'

def getPage():
    options = webdriver.ChromeOptions()
    options.add_argument('headless') # headless모드
    options.add_argument('window-size=1920x1080') 
    options.add_argument('--log-level=3') # 이 코드가 없으면 headless 모드시 log가 많이 표시된다.
    
    if getattr(sys,'frozen',False):
        chromedriver_path = os.path.join(sys._MEIPASS,"chromedriver.exe")
        driver = webdriver.Chrome(chromedriver_path,chrome_options=options)
    else:
        driver = webdriver.Chrome(r'C:/chromedriver.exe',chrome_options=options)
    
    # driver = webdriver.Chrome(r'C:/chromedriver.exe',chrome_options=options)
    driver.implicitly_wait(3)
    return driver

def Crawling(driver,count):
    for i in range(0,count):
        driver.get(URL)
        driver.switch_to_frame('down')
        visit = driver.find_element_by_xpath('//*[@id="cafeinfo_list"]/ul/li[4]/span[2]')
        print('Number of visitors : '+visit.text+', Iteration : '+str(i+1),sep='\n')

if __name__ == "__main__":
    count = int(input('방문 횟수를 입력하세요 : '))
    driver = getPage()
    Crawling(driver,count)

 



