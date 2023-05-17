import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # headless로 하면 접근이 제한되므로 실행 안함
driver = webdriver.Chrome(options = options)

url = 'https://www.coupang.com/np/search?component=&q=노트북가방&channel=user'
driver.get(url)
time.sleep(3)

html = driver.page_source
soup = bs(html, 'html.parser')
driver.quit()  # 파싱 직후 브라우저를 닫는다

items = soup.select('ul#productList > li.search-product')

for i in range(len(items)):
    #item_name = items[i].find('div', 'name').text  # find()방식: Tag를 리턴
    item_name = items[i].select('div.name')[0].text  # select()방식: List를 리턴
    link = 'https://coopang.com/'+items[i].find('a', 'search-product-link').get('href')
    
    #price = items[i].find('strong', 'price-value').text  # 유일할 때는 'price-value'를 빼도 상관없다
    price = items[i].select('strong.price-value')[0].text  # 유일할 때는 .price-value를 빼도 상관없다
    
    print('{}. {}'.format(i+1, item_name))
    print(link)
    print('가격 : {}원'.format(price))
    print()
