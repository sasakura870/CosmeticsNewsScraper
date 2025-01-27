from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import time
import re
import json

url = "https://www.lunasol-official.com/news/old_product"

driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

driver.implicitly_wait(10)

driver.get(url)
sections = driver.find_elements(By.CLASS_NAME, "newsArticle-section")
eolDataList = []
for section in sections:
    date = ""
    try:
        dateInfo = section.find_element(By.CLASS_NAME, "newsArticle-subTitle").text
    except NoSuchElementException:
        print("invalid product section")
        continue
    if dateInfo:
        match = re.search(r'(\d{4})年(\d{1,2})月', dateInfo)
        if match:
            date = f"{match.group(1)}/{match.group(2)}/1"
    if date:
        categories = section.find_elements(By.CLASS_NAME, "newsArticle-text")
        categoryProducts = section.find_elements(By.CLASS_NAME, "newsArticle-list")
        results = []
        for i in range(min(len(categories), len(categoryProducts))):
            category = categories[i].text
            products = [li.text for li in categoryProducts[i].find_elements(By.TAG_NAME, "li")]
            for product in products:
                eolDataList.append({
                    "date": date,
                    "brand": "LUNASOL",
                    "product": product,
                    "url": url,
                    "category": category,
                    "price": 0
                })
json.dump(eolDataList, open("/workspaces/data/LUNASOL.json", "w", encoding="utf-8"), ensure_ascii=False)

time.sleep(5)
driver.quit()
