"""
3. 네이버에서 원하는 이미지 불러오기
  - https://ultrakid.tistory.com/13 참조.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

TARGET = input('검색어를 입력하세요 : ')
BASE_URL = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
# URL = BASE_URL+검색어
URL = BASE_URL+quote_plus(TARGET)
html = urlopen(URL)
bs = BeautifulSoup(html,'html.parser')
img = bs.find_all(class_='_img')

n=1

for i in img:
    imgUrl = i['data-source']
    with urlopen(imgUrl) as f:
        with open('week2/img/'+TARGET+str(n)+'.jpg','wb') as h:
            img = f.read()
            h.write(img)
    n+=1

print("다운로드 완료.")