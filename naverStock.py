from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(ChromeDriverManager().install())
from tqdm import tqdm_notebook
import time
from bs4 import BeautifulSoup
import pandas as pd
import folium

def get_search_page_url(page):
    return "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page={}".format(page)

page=1 #시작페이지
url=get_search_page_url(page)
total_page = 5
stock_total=[]

for page in tqdm_notebook(range(1, total_page + 1)):
    # 1.검색 페이지 이동
    url = get_search_page_url(page)
    driver.get(url)
    # 페이지 로딩 시간이 필요하므로 2초 딜레이
    time.sleep(2)

    # 2.로드된 페이지의 html 태그 읽어오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 현재페이지의 상품정보 영역 읽어오기
    stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
    stock_total.append(stock_list)
    
    ans = []

for i in range(0,5):
    data_list=stock_total[i]
    for data in data_list:
        ans.append(data.get_text().split())
        
pd.DataFrame(ans, columns = ['순위', '종목명' , '현재가' , '전일비' , '등락률', '액면가', '시가총액' , '상장주식수' , '외국인비율', '거래량', 'PER', 'ROE','a','b','c'])        
