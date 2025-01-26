from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time
import json

url = "https://www.suqqu.com/ja/news"
keyword = "販売終了商品のお知らせ"

driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

driver.implicitly_wait(10)

driver.get(url)
eolNewsLinkList = []
lists = driver.find_elements(By.CLASS_NAME, "m-suqqu_newsList-item")
for li in lists:
    link = li.find_element(By.CLASS_NAME, "m-suqqu_newsList-link")
    title = link.find_element(By.CLASS_NAME, "m-suqqu_newsList-title").text
    if title == keyword:
        eolNewsLinkList.append(link.get_attribute("href"))

eolDataList = []
for link in eolNewsLinkList:
    driver.get(link)
    date = driver.find_element(By.CLASS_NAME, "suqqu_newsDtail-time").text
    content = driver.find_element(By.CLASS_NAME, "suqqu_newsDtail-text")
    products = content.find_elements(By.TAG_NAME, "a")
    for product in products:
        eolDataList.append({
            "date": date,
            "brand": "SUQQU",
            "product": product.text,
            "url": product.get_attribute("href")
        })
json.dump(eolDataList, open("data/SUQQU/eol.json", "w", encoding="utf-8"), ensure_ascii=False)

time.sleep(5)
driver.quit()
