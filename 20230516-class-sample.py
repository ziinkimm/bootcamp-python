import requests, openpyxl
from bs4 import BeautifulSoup
import re
excel_file = openpyxl.Workbook()
excel_sheet = excel_file.active
excel_sheet.append(['랭킹', '상품명', '판매가격', '상품상세링크'])

url = "https://www.coupang.com/np/search?component=&q=%EC%8B%A0%EC%9D%BC+%EC%84%9C%ED%81%98%EB%A0%88%EC%9D%B4%ED%84%B0&channel=user"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36"}
res = requests.get(url, headers = headers, verify=False)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

items = soup.find_all("li", attrs={"class":re.compile("^search-product")})

item_list = []
for index, item in items:
    name = item.find("div", attrs={"class":"name"}).get_text()
    price = item.find("strong", attrs={"class":"price-value"}).get_text()
    rate = item.find("em", attrs={"class":"rating"})
    if rate:
            rate = rate.get_text()
    else:
        continue
        
    review = item.find("span", attrs={"class":"rating-total-count"})
    if review:
            review = review.get_text()
            review = review[1:-1]
    else:
        continue

    link = item.find("a", attrs={"class":"search-product-link"})["href"]

    print(f"제품명 : {name}")
    print(f"가격 : {price}")
    print(f"평점 : {rate}점 ({review}개)")
    print("바로가기 : {}".format("https://www.coupang.com"+link))
    print("-"*30)
    excel_sheet.append([index+1, name, price, rate, "https://www.coupang.com"+link])
excel_file.save('PRODUCT_LIST.xlsx')
excel_file.close()
