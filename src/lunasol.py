from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    hoge = section.find_elements(By.CLASS_NAME, "newsArticle-subTitle")
    if len(hoge) == 0:
        continue
    title = section.find_element(By.CLASS_NAME, "newsArticle-subTitle").text
    date = ""
    if title:
        match = re.search(r'(\d{4})年(\d{1,2})月', title)
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
                    "product": f"{category} {product}",
                    "url": url
                })
json.dump(eolDataList, open("/workspaces/data/LUNASOL.json", "w", encoding="utf-8"), ensure_ascii=False)

time.sleep(5)
driver.quit()
