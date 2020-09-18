"""
1. 먼저 해당 회사의 종목코드를 가져와야한다. o
2. 종목 코드를 이용하여 api를 통해 주식 정보를 가져온다. o
3. 엑셀로 만들고 차트로 만든다. o

+ 원하는 회사의 이름을 입력 받고 종목코드를 가져와서 주식정보를 가져올 수 있도록 하자.
- 문제점 -
1) 나스닥 csv 파일을 html로 불러와지지 않는다.
2) get_code 함수에서 df type으로 객체리스트를 받으려고 했으나 
   실행되지 않음
"""
import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt

# 2019년 한 해의 주식을 가져오도록 설정한다.
start_date = '2020-01-01'
end_date = '2020-09-18'

# 증권거래소에 등록된 회사들의 TICKER를 담고 있는 파일이다.
# 아래의 주소는 나스닥 거래소의 상장된 회사들의 TICKER를 담고 있는 파일 주소이다.
# TICKER_URL = 'https://old.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df,name):
    ticker = df[df['Name'].str.contains(name)]['Symbol'].to_string(index=False) 
    # 위와 같이 ticker를 가져오면 앞에 공백 및 개행 문자가 붙어있음
    code = ticker.split('\n') # 개행 문자 제거
    new_com = []
    for com in code:
        new_com.append(com.strip())
        # strip() 하여 공백 제거
    return new_com # 회사 리스트 return

code_df = pd.read_csv('companylist.csv')
code_df = code_df[['Symbol','Name']]
company = input("회사명을 입력하세요. : ")
ticker = get_code(code_df,company) # 회사들의 ticker가 담긴다.(list)

for show in ticker:
    try:
        info = pdr.get_data_yahoo(show,start_date,end_date)
    except: # yahooDailyReader에 해당 회사의 데이터가 없는 경우 예외 발생
        print(show+" : No Data in YahooDailyReader\n")
    name = code_df[code_df['Symbol'] == show]['Name'].to_string(index=False)
    print("Company Name : "+name)
    print("Company Ticker : "+show)
    print(info)
    info['Close'].plot()
    info.to_excel(name+'_stock.xlsx')

"""
Open:개장가 High:고가 Low:저가 Close:마감 Volume:거래량
"""


