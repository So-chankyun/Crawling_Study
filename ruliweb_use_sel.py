"""
1. 루리웹 로그인 후 게시판 글 읽어오기(PC)

* 문제점
  - staleelementreferenceexception이 발생.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_INFO = {
    'user_id' : 'sock97',
    'user_pw':'skdltm97!'
}

class writing_info:
    def __init__(self,uid,title,content):
        self.uid = uid
        self.title = title
        self.content = content
    
    def print(self):
        print("user id : {}".format(self.uid))
        print("title : {}".format(self.title))
        print("content",sep='\n')
        print(self.content)

class Website:
    """
    웹사이트의 구조에 관한 정보를 저장한다.
    게시판의 각각의 글 내용의 정보를 저장.
    """

    def __init__(self,uidName,titleName,contentName):
        self.uidName = uidName
        self.titleName = titleName
        self.contentName = contentName

class Crawler:

    def __init__(self,siteData):
        self.site = siteData

    def parse(self,url,site):

        # url을 받아 콘텐츠를 추출한다.

        driver.get(url)
        title = driver.find_element_by_class_name('subject_text').text
        uid = driver.find_element_by_class_name('nick').text
        content = driver.find_element_by_class_name('view_content').text

        if title != '' and uid != '' and content != '':
            info = writing_info(uid,title,content)
            info.print()
    
    def crawl(self,url):
        driver.get(url)
        writing = driver.find_elements_by_xpath('//td[@class="subject"]')
        
        for u in writing:
            # staleelementreferenceexception이 발생.
            target_url = u.find_element_by_class_name('deco').get_attribute('href')
            self.parse(target_url,self.site)

login_url = 'https://user.ruliweb.com/member/login'

options = webdriver.ChromeOptions()
options.add_argument('headless') # headless모드
options.add_argument('window-size=1920x1080') 
options.add_argument('--log-level=3') # 이 코드가 없으면 headless 모드시 log가 많이 표시된다.

driver = webdriver.Chrome(r'C:\chromedriver.exe',chrome_options=options)
driver.implicitly_wait(3)
driver.get(login_url)
print('Title : %s\nLogin URL : %s'%(driver.title,driver.current_url))

id_elem = driver.find_element_by_id("user_id")
id_elem.clear()
id_elem.send_keys(LOGIN_INFO['user_id'])

driver.find_element_by_id("user_pw").clear()
driver.find_element_by_id("user_pw").send_keys(LOGIN_INFO['user_pw'])
# clear()와 send_key()sms None을 리턴한다.

login_btn = driver.find_element_by_xpath('//div[@id="login_submit"]')
# 태그는 어떻것이던 관계없이 현재 document에서 속성 id가 btnLogin인 것을 찾아라.
login_btn.click() # None 리턴

board_url = 'https://bbs.ruliweb.com/pc/board/1007?page='
driver.get(board_url)

i = 1

siteData = Website('nick','subject_text','view_content')
crawler = Crawler(siteData)
crawler.crawl(board_url+str(i))

