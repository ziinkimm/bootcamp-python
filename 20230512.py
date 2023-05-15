#멜론 챠트 크롤링

import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

# https://www.melon.com/chart/
url_melon="https://www.melon.com/chart/"
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
res_melon=req.get(url_melon,headers=headers)
soup=bs(res_melon.text,"html")
titles=soup.select("div.ellipsis.rank01>span>a")
artists=soup.select("div.ellipsis.rank02>span")

title_lst=[]
artist_lst=[]
index=1

for i in range(len(titles)):
    title_lst.append(titles[i].text)
    artist_lst.append(artists[i].text)
    print(index,titles[i].text,"\t",artists[i].text)
    index+=1
    print()

melon_dic={"타이틀":title_lst,"아티스트":artist_lst}
melon_dic

melon_df=pd.DataFrame(melon_dic)
melon_df

melon_df.to_csv("melon_chart100.csv",encoding="utf-8-sig")

# 네이버 뉴스 검색
import requests as req
from bs4 import BeautifulSoup as bs
import csv

query = input("검색어를 입력하세요: ")
url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}'
response = req.get(url)
soup = bs(response.text, "html.parser")
articles = soup.select("ul.list_news > li")
index = 1

for article in articles:
    title = article.select_one("a.news_tit").text.strip()
    link = article.select_one("a.news_tit")['href']
    summary = article.select_one("a.api_txt_lines.dsc_txt_wrap").text.strip()
        
    print(f"{index}. {title}")
    print(link)
    print(summary)
    print()
    
    index += 1
with open(f'{query}.csv',"w",encoding='utf-8-sig',newline='')as f:
    writer=csv.writer(f)
    writer.writerow(['제목','링크','요약'])
    for article in articles:
        title=article.select_one('.news_tit').text.strip()
        link=article.select_one('.news_tit').get('href')
        summary=article.select_one('.dsc_wrap').text.strip()
        writer.writerow([title,link,summary])

print(f'{query}.csv파일이 생성 되었습니다.')


# 네이버 검색창으로 홈쇼핑의 정보를 크롤링하고 저장?
import requests as req
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

list=[]

url="https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query="
query=input("검색어는?")
res=req.get(url+str(query))
soup=bs(res.text,"html.parser")
divs=soup.findAll("div",{"class":re.compile("^basicList_info_area__TWvzp")})
#divs는 리스트형태로 크롤링된것임.

tlts=[]
links=[]
prices=[]
for div in divs:
    tlts.append(div.find("div",{"class":"basicList_title__VfX3c"}).text)
    links.append(div.find("div",{"class":"basicList_title__VfX3c"}).find("a").get('href'))
    prices.append(div.find("div",{"class":"basicList_price_area__K7DDT"}).find("span",{"class":"price_price__LEGN7"}).text)

df=pd.DataFrame({
    "Title":tlts,
    "Link":links,
    "Price":prices
})
print(df)
df.to_csv(f'{query}.csv',encoding='utf-8-sig')

#함수를 구성하여 크롤링하는 방법?
import requests as req
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}

def create_soup(url):
    res=req.get(url,headers=headers)
    soup=bs(res.text,"html.parser")
    return soup

def scrape_headline_news():
    print("헤드라인 뉴스")
    url="https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
    soup=create_soup(url)
    
    news_list=soup.find("ul",{"class":"section_list_ranking_press _rankingList"})
    lis=news_list.findAll("a",{"class":"list_tit nclicks('rig.renws2')"})
    
    index=1
    for news in lis:
        title=news.text
        link=news.get("href")
        print(index,title,link)
        index+=1
        
if __name__=="__main__":
    scrape_headline_news()    
    
    
# 정규식 in crawling
import re
p=re.compile("ca.e")
# .  : 하나의 문자를 의미함
# ^  : 문자열의 시작
# $  : 문자열의 끝
m=p.match("cafe")
def print_match(m):
    if m:
        print("m.group()", m.group()) # 일치하는 문자열의 반환
        print("m.string()", m.string) # 입력 받는 문자열
        print("m.start()", m.start()) # 일치하는 문자열의 시작 index
        print("m.end()", m.end()) # 일치하는 문자열의 끝 index
        print("m.span()", m.span()) # 일치하는 문자열의 시작과 끝
    else:
        print("매칭되지 않음.")
        
m=p.match("caseless")
print_match(m)

### 네이버 시가총액 정보 크롤링
## 네이버 코스피 시가총액 순위를 가져오기
import csv
import re
import requests as req
from bs4 import BeautifulSoup as bs

url = "https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page="
for page in range(1, 3):
    res = req.get(url + str(page))
    soup = bs(res.text, "html.parser")
    data_rows = soup.find("table", {"class": "type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1: # 의미없는 데이터로 skip
            continue
        data = [column.get_text().strip() for column in columns]
          # 한줄 for 문임 ex.data=[i for in i in list]
        print(data)
        
 import csv
import re
import requests as req
from bs4 import BeautifulSoup as bs

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="
filename = "시가총액2.csv"
f = open(filename, 'w', encoding="CP949", newline='')
writer = csv.writer(f)
title = ["N", "종목명", "현재가", "전일비", "등락률", "액면가", "시가총액", "상장주식수", "외국인비율", "거래량", "PER", "ROE"]
writer.writerow(title)

for page in range(1, 3):
    res = req.get(url + str(page))
    soup = bs(res.text, 'html.parser')
    data_rows = soup.find("table", {"class": "type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1:
            continue
        data = [column.get_text().strip() for column in columns]
        writer.writerow(data)
print(f'{filename} 파일이 생성 되었습니다.')
f.close()

## 다음 2022년 영화순위 크롤링
import requests as req
from bs4 import BeautifulSoup as bs

res=req.get("https://search.daum.net/search?w=tot&q=2022%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR")
res
soup=bs(res.text,"html")

images=soup.findAll('img',{"class":"thumb_img"})
for idx, image in enumerate(images):
    image_url=image["src"]
    if image_url.startswith("//"):
        image_url="http:"+image_url
    print(image_url)
 
    
    #이파일들을 연결하여 저장하는 방법으로
    image_res=req.get(image_url)
    with open("movie{}.jpg".format(idx+1),"wb")as f:
        f.write(image_res.content)#content는 이미지 파일을 의미합니다.

#### 2022년부터 5년간을 지정해서 상위 5개의 영화이미지를 가져오기

#2022년부터 5년간을 지정해서 상위 5개의 영화이미지를 가져오기
import requests as req
from bs4 import BeautifulSoup as bs

for year in range(2018,2022):
    url=f'https://search.daum.net/search?w=tot&q=[year]%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR'
    res=req.get(url)
    soup=bs(res.text,"html")
    images=soup.findAll('img',{"class":"thumb_img"})
    
for idx, image in enumerate(images):
    image_url=image["src"]
    if image_url.startswith("//"):
        image_url="http:"+image_url
        print(image_url)
 
    
    #이파일들을 연결하여 저장하는 방법으로
    image_res=req.get(image_url)
    with open("movie{}_[].jpg".format(year,idx+1),"wb")as f:
        f.write(image_res.content)#content는 이미지 파일을 의미합니다.
        
import requests as req
from bs4 import BeautifulSoup as bs

for year in range(2018, 2022):
    url = f'https://search.daum.net/search?w=tot&q={year}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR'
    res = req.get(url)
    soup = bs(res.text, "html")
    images = soup.findAll('img', {"class": "thumb_img"})

    for idx, image in enumerate(images[:5]):
        image_url = image["src"]
        if image_url.startswith("//"):
            image_url = "http:" + image_url

        print(f"Downloading {image_url}")
        image_res = req.get(image_url)
        with open(f"movie{year}_{idx+1}.jpg", "wb") as f:
            f.write(image_res.content)
