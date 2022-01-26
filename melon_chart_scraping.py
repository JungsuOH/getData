from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

url="https://www.melon.com/chart/index.htm"

driver.get(url)

from bs4 import BeautifulSoup

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

songs = soup.select("table > tbody > tr")

rank = 0
song_data = []
for song in songs:
    title = song.select("span > a")[0].text
    singer = song.select("div.rank02 > a")[0].text
    rank += 1
    song_data.append(['melon',rank,title,singer])

import pandas as pd

pd.DataFrame(song_data)

melon_df = pd.DataFrame(song_data, columns = ['서비스', '순위' , '타이틀' , '가수'])

melon_df.to_excel('melon.xlsx', index=False)
