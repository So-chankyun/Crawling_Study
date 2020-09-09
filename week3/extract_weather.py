"""
1. 엑셀 데이터 읽고 쓰기
2. 엑셀 데이터 편집하기
3. 엑셀 데이터 출력하기
4. XML 기상청 날씨 데이터 지역별 파싱 및 출력
5. 본인 거주 지역 날씨 정보 XML 파싱 및 출력
"""
import xml.etree.ElementTree as ET
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# 기상청 URL
URL = 'http://www.weather.go.kr/weather/lifenindustry/sevice_rss.jsp'

html = urlopen(URL)
bs = BeautifulSoup(html,'html.parser')
province = [] # 각 지방의 날씨 정보를 담는 변수이다.(DataFrame type의 변수들이 담긴다.)

# 한 도시의 날씨 정보를 출력한다.
def residence_weather(city):
    info = pd.read_excel(r'weather.xlsx')
    match_col = []

    # enumerate : 리스트가 있는 경우 순서와 리스트의 값을 전달해주는 함수이다.
    # 주로 for문과 자주 사용된다.
    # 도시명이 매개변수 'city'와 일치하는 행의 index를 match_col에 저장한다.
    for index,data in enumerate(info['도시명']):
        if(city == str(data)):
            match_col.append(index)

    # new_datas 리스트에 match_col 행에 값을 저정한다.
    # iloc : 행 번호를 기준으로 행 데이터 읽기
    # loc : 인덱스 기준으로 행 데이터 일기
    new_datas = info.iloc[match_col] # 각 인덱스에 해당하는 데이터를 읽어서 저장한다.
    # 읽은 데이터들을 새로운 엑셀 파일로 저장한다.
    new_datas.to_excel('./'+city+'_weather.xlsx',sheet_name='Sheet1',index=False)

# 한 도시의 날씨 정보를 얻는다.
def getInfo(city_info):
    header = ['시/도','도시명','날짜','날씨','최저 기온','최고 기온','강수 확률']
    weather = []
    province_name = city_info.find('province')
    city_name = city_info.find('city')
    data = city_info.find_all('data')

    for o in data:
        city_detail = []
        city_detail.append(province_name.text)
        city_detail.append(city_name.text)
        cd = o.text.strip().split('\n')
        for i in range(1,7):
            if i != 5:
                city_detail.append(cd[i])
        # print(city_detail,sep='\n')
        weather.append(city_detail) # 한 날짜의 날씨 정보 리스트를 삽입
    
    return pd.DataFrame(weather,columns=header) # 한 도시의 날씨 정보리스트를 반환

def city_weather(url):
    # 해당 지역 xml 파싱.
    global province

    city = urlopen(url)
    xml = BeautifulSoup(city,'lxml')
    # 날짜(오전, 오후), 날씨, 최저 기온, 최고 기온, 강수 확률
    city_info = xml.find_all('location')
    
    for i in city_info: 
        province.append(getInfo(i)) # province 배열에 도시별로 날씨정보를 저장하자.(dataframe type)

# 3. 엑셀로 정리된 지역별 날씨를 출력하는 함수이다.
def print_weather():
    info = pd.read_excel('weather.xlsx')
    # 모든 정보를 출력한다.
    print(info)
    # 지역의 날씨 중에서 도시명, 날짜 최저 기온, 최고 기온만 출력한다.
    ex_info = info[['도시명','날짜','최저 기온','최고 기온']]
    print(ex_info)

# 엑셀 파일을 편집하는 함수이다.
def edit_excel():
    df = pd.read_excel('weather.xlsx')
    # 날짜를 추출하여 새로운 열을 추가한다.
    df['일'] = df['날짜'].str.slice(start=8,stop=10)
    df.head()
    df.to_excel('edit_weather.xlsx')

# 해당 지역의 날씨 정보를 불러와 엑셀의 한 시트로 저장하기.
"""
for i in range(2,11):
    city_xml = bs.find('a',{'id':'dfs_rss'+str(i)}).get('href')
    city_weather(city_xml) # 시도군별 링크 전송

# DataFrame type의 각 지역의 날씨정보들을 모두 합친다.
df = pd.concat(province, axis=0,ignore_index=True)
# 하나의 엑셀파일로 만든다.
df.to_excel('weather.xlsx',index=False)

name = input('거주지를 입력하세요 : ')
residence_weather(name)

print_weather()
"""
edit_excel()

