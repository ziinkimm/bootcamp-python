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
