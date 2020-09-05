"""
1. 루리웹 로그인 후 게시판 글 읽어오기(PC)

* 문제점
  - 로그인된 세션을 제대로 불러오지 못함.
  - 같은 세션 객체를 이용했는데도 불구하고 로그인 후 사용할 수 있는 페이지를 불러오지 못함
"""

import requests
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'user_id' : 'sock97',
    'user_pw':'skdltm97!'
}

class writing_info:
    """
    게시판 글의 유저 닉네임, 글 제목, 글 내용을 저장하는 클래스이다.
    """
    
    def __init__(self,uid,title,content):
        self.uid = uid
        self.title = title
        self.content = content
    
    # 글의 정보들을 출력하는 함수이다.
    def print(self):
        print('-'*50)
        print("user id : {}".format(self.uid))
        print("title : {}".format(self.title))
        print("content",sep='\n')
        print(self.content)

class Website:
    """
    웹사이트의 구조에 관한 정보를 저장한다.
    게시판의 각각의 글 내용의 정보를 저장.
    """

    # user의 닉네임, 글 제목, 글 내용 class name을 초기화한다.
    def __init__(self,uidName,titleName,contentName):
        self.uidName = uidName
        self.titleName = titleName
        self.contentName = contentName

class Crawler:
    """
    크롤링을 진행하는 클래스이다.
    """

    # siteData 에는 user의 닉네임, 글 제목, 글 내용의 class name
    # 정보가 저장되어 있다.
    def __init__(self,siteData):
        self.site = siteData

    # url을 가져오는데 오류가 발생하지 않는다면 beautifulsoup 객체를 반환한다.
    def getPage(self,url, session):
        try:
            req = session.get(url)
        except session.exception.RequestException:
            return None
        return bs(req.text,'html.parser')

    # url을 받아 콘텐츠를 추출한다.
    def parse(self,url,session,site):
        bs = self.getPage(url,session)
        if bs is not None:
            title = bs.find('span',{'class':site.titleName}).get_text()
            uid = bs.find('strong',{'class':site.uidName}).get_text()
            content = bs.find('div',{'class':site.contentName}).get_text()
            if title != '' and uid != '' and content != '':
                info = writing_info(uid,title,content) # 읽어온 데이터를 writing_info type의 객체에 저장한다.
                info.print() # 정보 출력
    
    # PC 게시판의 글들의 url을 저장하고 해당 url로 들어가서 크롤링을 진행한다.
    def crawl(self,url,session):
        bs = self.getPage(url,session)
        writing = bs.find_all('td',{'class':'subject'})

        for url in writing:
            target_url = url.find('a',{'class':'deco'}).get('href')
            self.parse(target_url,session, self.site)

LOGIN_URL = 'https://user.ruliweb.com/member/login'
board_url = 'https://bbs.ruliweb.com/pc/board/1007?page='

# Session 생성, with 구문 안에서 유지
with requests.Session() as s:
    # HTTP POST Request : 로그인을 위해 POST url와 함께 전송될 data를 넣어주자.
    login_req = s.post(LOGIN_URL,data=LOGIN_INFO)

    # 로그인이 되지 않으면 경고를 띄워준다.
    if login_req.status_code != 200:
        raise Exception('로그인이 되지 않았어요! 아이디와 비밀번호를 다시 확인해주세요!')

    """
    pc게시판의 글제목, 글쓴이, 글 내용, 작성일자, 글 id를 가져올 수 있도록 하자.
    일단 첫페이지만 크롤링하자.
    """

    i = 1   
    siteData = Website('nick','subject_text','view_content') # user의 닉네임, 글 제목, 글 내용의 class name을 저장
    crawler = Crawler(siteData) # Crawler type의 객체 생성(siteData로 초기화)
    crawler.crawl(board_url+str(i),s) # 크롤링 진행

