from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver=webdriver.Chrome(ChromeDriverManager().install())
from tqdm import tqdm_notebook
import time
from bs4 import BeautifulSoup
import pandas as pd
import folium

def get_search_page_url(keyword, page):
    return "http://search.danawa.com/dsearch.php?query={}&originalQuery={}&volumeType=allvs&page={}&limit=40&sort=saveDESC&list=list&boost=true&addDelivery=N&recommendedSort=Y&defaultUICategoryCode=102207&defaultPhysicsCategoryCode=72%7C80%7C81%7C0&defaultVmTab=2618&defaultVaTab=383552&tab=goods".format(keyword,keyword,page)

keyword="무선청소기" #검색하고 싶은 키워드로 변경
page=1 #시작페이지
url=get_search_page_url(keyword,page)
total_page = 10 # 어디까지 검색하고싶은가?

for page in tqdm_notebook(range(1, total_page + 1)):
    # 1.검색 페이지 이동
    url = get_search_page_url(keyword, page)
    driver.get(url)
    # 페이지 로딩 시간이 필요하므로 2초 딜레이
    time.sleep(2)

    # 2.로드된 페이지의 html 태그 읽어오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 현재페이지의 상품정보 영역 읽어오기
    prod_items = soup.select("ul.product_list > li.prod_item")

    prod_data_total = []
    prod_data = []

    for prod_item in prod_items:
        try:  # 상품명
            title = prod_item.select("p.prod_name > a")[0].text.strip()
        except:
            title = ""
        try:  # 스펙정보
            spec_list = prod_item.select("div.spec_list")[0].text.strip().replace("\n", '').replace('\t', '')
        except:
            spec_list = ""
        try:  # 가격정보
            price = prod_item.select("li.rank_one>p.price_sect>a>strong")[0].text.strip().replace(",", "")
        except:
            price = ""
            price = 0
        prod_data.append([title, spec_list, price])
    prod_data_total.append(prod_data)
    df = pd.DataFrame(prod_data_total, columns = ['상품명', '제품정보' , '가격'])

df.to_excel('danawa.xlsx', index=False)
