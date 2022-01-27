from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

driver=webdriver.Chrome(ChromeDriverManager().install())
url="https://www.instagram.com"
driver.get(url)
html=driver.page_source
soup=BeautifulSoup(html, 'html.parser')

time.sleep(2)#로딩시간 배려

email="pjs19q4@gmail.com" ##본인의 ID 입력
input_id=driver.find_element_by_css_selector('input._2hvTZ.pexuQ.zyHYP')
input_id.send_keys(email)

password="!@#$%12345"  ##본인의 PW입력
input_ps=driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
input_ps.send_keys(password)
input_ps.submit()
time.sleep(2) #로딩시간 배려

#키워드 입력하고 이동
word='서울데이트'
driver.get('https://www.instagram.com/explore/tags/'+word)
time.sleep(5)#여기서 로딩이 오래 걸려서 오류 발생하면 sleep을 더 길게


#첫번째 게시글로 이동
first=driver.find_element_by_css_selector("div._9AhH0")
first.click()
time.sleep(3)
tour_data=[]

for i in range(0,5):#5회 반복
    html=driver.page_source
    soup=BeautifulSoup(html, 'html.parser')
    content = soup.select("div.C4VMK > span")[0].text  # 본문
    try:
        like = soup.select("a.zV_Nj > span")[0].text  # 좋아요
    except:
        like=0
    try:
        date = soup.select("time._1o9PC.Nzb55")[0].text  # 작성시간
    except:
        date="Unknown"
    try:
        location = soup.select("div.M30cS")[0].text  # 장소
    except:
        location = " "
    data = [content, like, date, location]
    tour_data.append(data)#데이터 저장
    next = driver.find_element_by_css_selector("div.l8mY4.feth3")
    next.click()  # 오른쪽 글로 이동
    time.sleep(2)

##pandas로 데이터프레임, 엑셀화하여 출력
seoulDate=pd.DataFrame(tour_data, columns=['본문', '좋아요', '작성시간', '위치'])
seoulDate.to_excel("seoulDate.xlsx", index=False)
