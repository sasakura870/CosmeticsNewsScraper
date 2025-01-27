from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from utils import extract_path_between, extract_number_in_string
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
    productInfoList = [
        {"name": product.text, "link": product.get_attribute("href")}
        for product in products
    ]
    for productInfo in productInfoList:
        price = 0
        try:
            driver.get(productInfo["link"])
            priceToStr = driver.find_element(By.CLASS_NAME, "price").text
            price = extract_number_in_string.extract_number_in_string(priceToStr)
        except NoSuchElementException:
            print("Price not found")
        categories = extract_path_between.extract_path_between(productInfo["link"], "categories", "p")
        category = ""
        if len(categories) == 1:
            category = categories[0]
        elif len(categories) == 2:
            category = categories[1]
        eolDataList.append({
            "date": date,
            "brand": "SUQQU",
            "product": productInfo["name"],
            "url": productInfo["link"],
            "category": category,
            "price": price
        })
json.dump(eolDataList, open("/workspaces/data/SUQQU.json", "w", encoding="utf-8"), ensure_ascii=False)

time.sleep(5)
driver.quit()
