
import time
from selenium.common.exceptions import NoSuchElementException
import insta_url
link_list=[]
like_list=[]
content_list=[]
tag_list=[]
date_list=[]
place_list=[]
src_img_list=[]
src_vid_list=[]
flag=0

#함수 작성
def insta_searching(word):  #word라는 매개변수를 받는 insta_searching 이라는 함수 생성
    url = 'https://www.instagram.com/explore/tags/' + word
    return url

#첫번째 게시물 찾아 클릭 함수 만들기
import time 
def select_first(driver):
    first = driver.find_element_by_css_selector('div._9AhH0') 
    #find_element_by_css_selector 함수를 사용해 요소 찾기
    first.click()
    time.sleep(3) #로딩을 위해 3초 대기
    #본문 내용, 작성 일시, 위치 정보 및 해시태그(#) 추출

def get_content(driver):
    # 현재 페이지의 HTML 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    #1. 링크 주소 가져오기
    try:
        link= soup.find("a", {"class": "c-Yi7"}).attrs['href']
        
    except:
        link='NULL'
    tmp_img=[]
    tmp_vid=[]
    while(1):
        time.sleep(1)
        pageString = driver.page_source 
        soup = BeautifulSoup(pageString, "lxml")
        try:
            videos= soup.find("video", {"class": 'tWeCl'}).attrs['src']
            tmp_vid.append(videos)
        except:
            imgs = soup.select('img')[1]
            imgs = imgs.attrs['src']
            if imgs:
                tmp_img.append(imgs)
            else:
                imgs = imgs.attrs['srcset']
                tmp_img.append(imgs)
        try :
            driver.find_element_by_class_name("coreSpriteRightChevron").click()

        except NoSuchElementException :
            break
    
    
    # 2. 본문 내용 가져오기
    try:  			#여러 태그중 첫번째([0]) 태그를 선택  
        content = soup.select('div.C4VMK > span')[0].text 
        			#첫 게시글 본문 내용이 <div class="C4VMK"> 임을 알 수 있다.
                                #태그명이 div, class명이 C4VMK인 태그 아래에 있는 span 태그를 모두 선택.
    except:
        content = ' ' 
    # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
    tags = re.findall(r'#[^\s#,\\]+', content) # content 변수의 본문 내용 중 #으로 시작하며, #뒤에 연속된 문자(공백이나 #, \ 기호가 아닌 경우)를 모두 찾아 tags 변수에 저장
   
    
    # 4. 작성 일자 가져오기
    try:
        date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10] #앞에서부터 10자리 글자
    except:
        date = ''

    # 5. 좋아요 수 가져오기
    try:
        like = soup.select('div.Nm9Fw > button')[0].text[4:-1] 
    except:
        like = 0

    # 6. 위치 정보 가져오기
    try:
        place = soup.select('div.JF9hh')[0].text
    except:
        place = ''
        
    # 7. 수집한 정보 저장하기
    link_list.append(link)
    content_list.append(content)
    like_list.append(like)
    tag_list.append(tags)
    date_list.append(date)
    place_list.append(place)
    src_img_list.append(tmp_img)
    src_vid_list.append(tmp_vid)
def move_next(driver):
    right = driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow') 
    right.click()
    time.sleep(3)
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re 
#1. 크롬으로 인스타그램 - '사당맛집' 검색
driver = webdriver.Chrome("./chromedriver.exe")
search = input('검색어를 입력하세요: ')
word=str(search)
url = insta_searching(word)

#2. 로그인 하기
id=input("아이디 입력:")
pw=input("비밀번호 입력:")
lurl = 'http://www.instagram.com'
driver.get(lurl)
driver.implicitly_wait(5)
driver.find_element_by_name('username').send_keys(id)    # id 입력
elem_pw = driver.find_element_by_name('password')    # pw 입력
elem_pw.send_keys(pw)
elem_pw.submit()

driver.implicitly_wait(5)    # 파싱될 때까지 5초 기다림 (미리 완료되면 waiting 종료됨)
driver.find_element_by_class_name('cmbtv').click()    # 비밀번호 저장하지 않음

driver.implicitly_wait(5)
driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div/div[3]/button[2]').click() 

#3. 검색페이지 접속하기
driver.get(url)
time.sleep(4) 
#4. 첫번째 게시글 열기
select_first(driver) 
#5. 비어있는 변수(results) 만들기
results = [] 
#여러 게시물 크롤링하기
target= 6 #크롤링할 게시물 수
for i in range(target):
    data = get_content(driver) #게시물 정보 가져오기
    results.append(data)
    move_next(driver)    

import pandas as pd
from selenium.common.exceptions import NoSuchElementException 
from time import sleep


insta_dict = {
              'link':link_list,
              'content':content_list,
              'tags':tag_list,
              'date':date_list,
              'place':place_list,
             'like':like_list,
             'img':src_img_list,
              'video':src_vid_list
             }
df = pd.DataFrame(insta_dict)
df=df[~df.content.str.contains("광고")]
now=time.strftime('%m%d_%H_%M',time.localtime(time.time()))
df.to_csv(word+'_'+now+'.csv',encoding='utf-8-sig')
