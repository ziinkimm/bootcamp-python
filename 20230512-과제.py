from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# 검색어 입력 받기
query = input("검색어를 입력하세요: ")

# 브라우저 옵션 설정
options = Options()
options.add_argument("--headless")  # 브라우저를 표시하지 않고 실행

# Chrome 드라이버 생성
webdriver_service = Service("path_to_chrome_driver")  # Chrome 드라이버의 경로로 변경
driver = webdriver.Chrome(service=webdriver_service, options=options)

# 검색 페이지로 이동
url = f"https://search.shopping.naver.com/search/all?query={query}&cat_id=&frm=NVSHATC"
driver.get(url)

# 페이지 로딩을 위해 최대 10초 대기
wait = WebDriverWait(driver, 10)

# 스크롤을 최하단까지 내리고 데이터 추출하는 함수
def scroll_and_extract():
    # 스크롤을 최하단까지 내리기
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # 스크롤 후 잠시 대기

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 현재 페이지의 HTML 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 원하는 정보 추출
    items = soup.select('div.basicList_item__0T9JD')

    data = []
    for item in items:
        # 상품 정보 추출
        name = item.select_one('a.basicList_link__JLQJf').text.strip()       
        price_elem = item.select_one('span.price_num__S2p_v')
        price = price_elem.text.strip() if price_elem else 'N/A'       
        review_elem = item.select_one('em.basicList_num__sfz3h')
        review = review_elem.text.strip() if review_elem else 'N/A' 
        regdate_elem = item.select_one('span.basicList_etc__LSkN_')
        regdate_raw = regdate_elem.text.strip() if regdate_elem else ''
        regdate_match = re.search(r'(\d{4})\.(\d{2})', regdate_raw)
        regdate = f"{regdate_match.group(1)}.{regdate_match.group(2)}" if regdate_match else ''
        description_elem = item.select_one('div.basicList_detail_box__OoXKt')
        description = description_elem.text.strip() if description_elem else 'N/A'
        link = item.select_one('div.basicList_title__VfX3c').find("a").get('href')

#        regdate = item.select_one('span.basicList_etc__LSkN_').text.strip()

        # 데이터 리스트에 추가
        data.append([name, price, review, regdate, description, link])

    return data

# 스크롤과 페이지 이동 반복하기
desired_page = int(input("원하는 페이지 갯수를 입력하세요: "))
page = 1
total_data = []

while page <= desired_page:
    print(f"---------페이지 데이터 처리중 현재 {page} 페이지입니다----------")
    data = scroll_and_extract()
    total_data.extend(data)

    # 다음 페이지로 이동
    pagination = driver.find_element(By.CSS_SELECTOR, 'div.pagination_num__b1BF2')
    next_page_link = pagination.find_element(By.XPATH, f'./a[text()="{page+1}"]')
    driver.execute_script("arguments[0].click();", next_page_link)
    time.sleep(2)

    page += 1
    
# 데이터프레임 생성

print("현재 데이터프레임에 저장중입니다...")

columns = ['상품명', '가격', '리뷰 수', '등록일', '세부정보', '링크']
df = pd.DataFrame(total_data, columns=columns)
# 리뷰 수를 기준으로 내림차순 정렬
df = df.sort_values(by='리뷰 수', ascending=False)

# 가격 정보가 없는 경우 빈 문자열로 처리
df['가격'] = df['가격'].fillna('')


# CSV 파일로 저장
keyword = query.replace(' ', '_')  # 공백을 언더스코어로 변경하여 키워드로 사용
current_time = time.strftime("%Y%m%d_%H%M%S")  # 현재 시간을 포맷팅하여 파일명에 사용
num_rows = len(df)  # 데이터프레임의 행 개수
filename = f"{keyword}_{current_time}_{num_rows}rows.csv"

df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"{filename} 파일로 저장이 완료되었습니다.")

# 브라우저 종료
driver.quit()
