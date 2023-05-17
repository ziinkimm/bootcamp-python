import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

driver=webdriver.Chrome()

query=input("검색할 상품을 입력하시오 : ")
url=f"https://www.coupang.com/np/search?component=&q={query}&channel=user"

print()

driver.get(url)
time.sleep(3)
soup=bs(driver.page_source,features="html.parser")
lis=soup.findAll("li",{"class":"search-product"})
index=1
for li in lis:
    name=li.find("div",{"class":"name"})
    price=li.find("strong",{"class":"price-value"})
    addr=li.find("a").get("href")
    print(index,name.text)
    print(price.text+"원")
    print("http://www.coupang.com"+addr)
    print()
    index+=1
