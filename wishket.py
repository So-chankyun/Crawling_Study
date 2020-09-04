"""
2. 위시캣에 로그인한 후 정보 불러오기(프로젝트 정보)

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_INFO = {
    'id_identification' : 'sock97',
    'id_password':'skdltm97!'
}

login_url = 'https://www.wishket.com/accounts/login/'

options = webdriver.ChromeOptions()
options.add_argument('headless') # headless모드
options.add_argument('window-size=1920x1080') 
options.add_argument('--log-level=3') # 이 코드가 없으면 headless 모드시 log가 많이 표시된다.

driver = webdriver.Chrome(r'C:\chromedriver.exe',chrome_options=options)
driver.implicitly_wait(3)
driver.get(login_url)
print('Title : %s\nLogin URL : %s'%(driver.title,driver.current_url))

id_elem = driver.find_element_by_id("id_identification")
id_elem.clear()
id_elem.send_keys(LOGIN_INFO['id_identification'])

driver.find_element_by_id("id_password").clear()
driver.find_element_by_id("id_password").send_keys(LOGIN_INFO['id_password'])
# clear()와 send_key()는 None을 리턴한다.

login_btn = driver.find_element_by_xpath('//div[@id="submit"]')
# 태그는 어떻것이던 관계없이 현재 document에서 속성 id가 btnLogin인 것을 찾아라.
login_btn.click() # None 리턴

board_url = 'https://www.wishket.com/mywishket/client/'
driver.get(board_url)

user_project = driver.find_element_by_class_name('user-project')

print(user_project.text)

driver.save_screenshot("screenshot.png")

