from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import extract_number_in_string
import os
import time
import json

url = "https://maison.kose.co.jp/site/e/eproducts-end-nailholic/"

driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

driver.implicitly_wait(10)

driver.get(url)
eolDataList = []
products = driver.find_elements(By.CLASS_NAME, "c-product__item")
for product in products:
	link = product.find_element(By.CLASS_NAME, "c-product__thumb__img").get_attribute("href")
	description = product.find_element(By.CLASS_NAME, "c-product__about")
	name = description.find_element(By.CLASS_NAME, "c-product__product-name").text
	priceToStr = description.find_element(By.CLASS_NAME, "c-product__price").text
	eolDataList.append({
		"brand": "NAILHOLIC",
		"product": name,
		"url": link,
		"category": "nail",
		"price": extract_number_in_string.extract_number_in_string(priceToStr)
	})
json.dump(eolDataList, open("/workspaces/data/NAILHOLIC.json", "w", encoding="utf-8"), ensure_ascii=False)

time.sleep(5)
driver.quit()
