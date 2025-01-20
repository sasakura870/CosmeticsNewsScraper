from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time

url = "https://www.suqqu.com/ja/news"
keyword = "スクレイピング"

driver = webdriver.Remote(
    command_executor = os.environ["SELENIUM_URL"],
    options = webdriver.ChromeOptions()
)

driver.implicitly_wait(10)

driver.get(url)
lists = driver.find_elements(By.CLASS_NAME, "m-suqqu_newsList-item")
for li in lists:
    link = li.find_element(By.CLASS_NAME, "m-suqqu_newsList-link")
    print(link.get_attribute("href"))
    title = link.find_element(By.CLASS_NAME, "m-suqqu_newsList-title").text
    print(title)

time.sleep(5)
driver.quit()
