from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pymysql

from bs4 import BeautifulSoup
import time
from datetime import datetime

conn = pymysql.connect(host='localhost', user='root',
                       password='root1234', charset='utf8',
                       database='mini')
cursor = conn.cursor()

options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")

s = Service("/Users/suhyeon/Desktop/sparta/chromedriver")

driver = webdriver.Chrome(service=s)

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%AC%B4%EB%A3%8C%EC%A0%84%EC%8B%9C%ED%9A%8C"
driver.get(url)

driver.find_element(By.XPATH,"/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div/div[1]/div/div/div/ul/li[2]/div/ul/li[1]/a").click()
time.sleep(0.5)
soup = BeautifulSoup(driver.page_source, 'html.parser')
pageNum = int(soup.find("span", attrs={"class":"_total"}).text)
tag = soup.find_all("div",attrs={"class":"card_item"})
cardNum = len(tag)
print(pageNum)

from datetime import timedelta
for page in range(1, pageNum+1):
    for num in range(1,cardNum+1):
        sql = "INSERT INTO exhibitions (exhibition_id, title,init_date, end_date, place, img_url) VALUES (null, %s, %s, %s, %s, %s)"
        title = soup.select(f"#mflick > div > div > div > div > div:nth-child({num}) > div.data_area > div > div.title > div > strong")[0].text

        date = soup.select(f"#mflick > div > div > div > div > div:nth-child({num}) > div.data_area > div > div.info > dl:nth-child(1) > dd")[0].text
        place = soup.select(f"#mflick > div > div > div > div > div:nth-child({num}) > div.data_area > div > div.info > dl:nth-child(2) > dd")[0].text
        img = soup.select(f"#mflick > div > div > div > div > div:nth-child({num}) > div.data_area > a > img")[0]['src']

        try:
            initDate = datetime.strptime(date.split('~')[0].rstrip('.').replace('.', '-'), '%Y-%m-%d')
            endDate = datetime.strptime(date.split('~')[1].rstrip('.').replace('.', '-'), '%Y-%m-%d')
            cursor.execute(sql,(title, initDate, endDate, place, img))
            conn.commit()
        #날짜가 만약 날짜형식이 아니면 어떻게 처리하는게 제일 좋을지...
        except Exception as e:
            endDate = initDate + timedelta(days=30)
            continue

    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div/div/div[3]/div/a[2]").click()
    time.sleep(0.2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tag = soup.find_all("div", attrs={"class": "card_item"})
    cardNum = len(tag)

conn.close()