from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import urllib.parse

driver = webdriver.Chrome()
url_base = "https://www.coupang.com/np/search?component=&q="
search = input("검색어를 입력하세요: ")
url = url_base + str(search)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

driver.get(url)
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

items = soup.select("ul.search-product-list")
results = []

for item in items:
    temp = []
    title = item.select_one('div.name').text.strip()
    price = item.select_one('div.price').text.strip()
    rating = item.select_one('span.rating-total-count').text.strip()
    temp.append(title)
    temp.append(price)
    temp.append(rating)
    results.append(temp)
    print(title,price,rating)
    print(temp)
