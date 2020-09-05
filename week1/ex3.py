import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

BASE_URL = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok='

KOSPI_CODE = 0
KOSDAK_CODE = 1
START_PAGE = 1

def main(code):
    # total_page을 가져오기 위한 requests
    res = requests.get(BASE_URL+str(code)+"&page="+str(START_PAGE))
    page_soup = BeautifulSoup(res.text,'lxml')

    # total_page 가져오기
    total_page_num = page_soup.select_one('td.pgRR > a')
    total_page_num = int(total_page_num.get('href').split('=')[-1])
    # ~~&page=32, '='를 기준으로 문자열을 나눠 list로 만든다. 
    # 따라서 2개로 나뉘게 되는데 '='의 앞부분과 뒷부분인 total page number 
    # 즉, 문자열 형태인 32를 int형으로 형변환 시켜주어 저장한다.

    # page마다 정보를 긁어오게끔 하여 result에 저장
    # DataFrame의 객체를 배열형태로 저장.
    result = [crawl(code,str(page)) for page in range(1,total_page_num+1)]

    # page마다 가져온 정보를 df에 하나로 합침
    # 여러개의 DataFrame을 하나로 합친다.
    df = pd.concat(result, axis=0,ignore_index=True)

    # 엑셀로 내보내기
    df.to_excel('NaverFinance.xlsx')

def crawl(code,page):
    res = requests.get(BASE_URL+str(code)+"&page="+str(page))
    page_soup = BeautifulSoup(res.text,'lxml')
    # 크롤링할 table html 가져오기
    table_html = page_soup.select_one('div.box_type_l')

    #Column명
    header_data = [item.get_text().strip() for item in table_html.select('thead th')][1:-1]
    # 첫번째 열의 N과 마지막 열의 토론방은 필요가 없는 header 정보이다.
    
    # 종목명 + 수치 추출 (a.title = 종목명, td.number=기타수치)
    inner_data = [item.get_text().strip() for item in table_html.find_all(lambda x: 
                                            (x.name == 'a' and 'tltle' in x.get('class',[])) or
                                            (x.name == 'td' and 'number' in x.get('class',[]))
                                            )]
                                            # list중에 class를 key 값으로 갖는 value가 title
                                            # 이고 태그명이 a인 경우 & key값이 number이고 태그명이 td인 
                                            # 객체를 item에 저장.
                                            # 그냥 get을 사용하지 않고 lambda를 사용한 이유는
                                            # None이 반환되어 저장되는 것을 방지하기 위함이다.(?)
    # page마다 있는 종목의 순번 가져오기
    no_data = [item.get_text().strip() for item in table_html.select('td.no')]
    number_data = np.array(inner_data)

    # 가로 x 세로 크기에 맞게 행렬화
    number_data.resize(len(no_data),len(header_data))
    # number_data.resize(len(no_data),len(header_data))
    # 한 페이지에서 얻은 정보를 모아 DataFrame로 만들어 리턴
    df = pd.DataFrame(number_data,columns=header_data)
    return df

main(KOSPI_CODE)