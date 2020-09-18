"""
1. 먼저 해당 회사의 종목코드를 가져와야한다.
2. 종목 코드를 이용하여 api를 통해 주식 정보를 가져온다.
3. 엑셀로 만들고 차트로 만든다.
"""
import pandas_datareader as pdr
import pandas as pd

stock_type = {
    'kospi':'stockMkt',
    'kosdaq':'kosdaqMkt'
}

# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df,name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)

# 위와 같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로
# strip() 하여 공백 제거
    code = code.strip()
    return code

def get_download_stock(market_type=None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType='+market_type

    df = pd.read_html(download_link,header=0)[0]
    return df

# kospi 종목코드 목록 다운로드
def get_download_kospi():
    df = get_download_stock('kospi')
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
    # df안의 종목코드의 value들을 모두 6자리.KS의 문자열 형태로 변경해준다.
    return df

# kosdaq 종목코드 목록 다운로드
def get_download_kosdaq():
    df = get_download_stock('kosdaq')
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
    return df

kospi_df = get_download_kospi()
kosdaq_df = get_download_kosdaq()

# data frame merge
code_df = pd.concat([kospi_df,kosdaq_df])

code_df = code_df[['회사명','종목코드']]

# data frame title 변경
code_df = code_df.rename(columns={'회사명':'name','종목코드':'code'})
code = get_code(code_df,'삼성전자')
df = pdr.get_data_yahoo(code)
print(code)
print(df)

"""
Open:개장가 High:고가 Low:저가 Close:마감 Volume:거래랑
"""


