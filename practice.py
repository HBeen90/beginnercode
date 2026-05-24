#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 13:02:20 2026

@author: hyobeen
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import requests
from bs4 import BeautifulSoup as bs
import time
import lxml



'''
filename='t.txt'
f=open(filename)
sentence = f.read()


#print(f.tell())

class Calculator:
    def __init__(self):
        self.result = 0 
    def adds(self,num):
        self.result += num
        return self.result

cal1 = Calculator()
A = cal1.adds(30)
#print(A)

class A:
    def __init__(self,name):
        self.name = '로섬'
    def __str__(self):
        return('아무도 아님')

class B:
    def print_name(self,name):
        print(self.name)
b_io= B('j')
q=b_io.print_name('귀도 반 로섬')
print(q)


property_candidate = {'이재명':3217161, '윤석열':7745343, '심상정':1406297,
                      '안철수':197985542, '오준호':264067, '허경영':26401367, '이백윤':171800,
                      '옥은호':337062, '김동연':4053544, '김경재':2202623, '조원진':2058661,
                      '김재연':51807, '이경희':149907313, '김민찬':421648}

name = list(property_candidate.keys())
money = np.array(list(map(lambda x: x/100, property_candidate.values())))

from matplotlib import font_manager
font_name = './NanumGothic.ttf'
fontprop = font_manager.FontProperties(fname=font_name, size=10)

def plot():
    
    plt.bar(name,money)
    plt.xticks(fontproperties = fontprop, rotation=-90)
    plt.show()
    
def plot_sns():
    plt.figure(figsize =(4,4))
    sns.set_theme(style='white', context='talk')
    sns.barplot(x=name,y=money)
    plt.xticks(fontproperties=fontprop, rotation =-90)
    plt.show()


def dict_data():
    dict_data={'a':1, 'b':2, 'c':3}
    sr=pd.Series(dict_data)
    print(sr)
    
    list_data = ['2019-01-02', 3.14, 'ABC', 100, True]
    sr_1 = pd.Series(list_data)
    print(sr_1)
    A=list(sr.index)
    B=list(sr_1.index)
    print(A)
    print(B)

def dataframe_w():
    df = pd.DataFrame([
        [1,2,3,4, 'Hello'],
        [5,6,7,8,'World'],
        [9,10,11,12,'foo']])
    df.to_csv('ex1.csv',index =False, header = False)
    
def dataframe_w1():
    df = pd.DataFrame([
        ['key1', 'key2', 'value1', 'value2'],
        ['one', 'a',1,2],
        ['one','b',3,4],
        ['one','c',5,6],
        ['one','d',7,8],
        ['two','a',9,10],
        ['two','b',11,12],
        ['two','c',13,14],
        ['two','d',15,16]])
    df['new_colum']= ['value3',11,22,33,44,55,66,77,88]
    df.loc[len(df)] = ['three','a', 232,343,454]
    

    df.to_csv('ex2.csv',index = 0, header = 0)
'''    

def parse_page(page):
    base_url = 'https://finance.naver.com/news/news_list.naver'
    base_params ={"mode":"LSS2D", "section_id": "101", "section_id2":"258"}
    params = {**base_params, "page": page}
    response = requests.get(base_url, params=params)
    soup = bs(response.text, 'html.parser')
    articlesubject_list = soup.select('.articleSubject')
    articleSummary_list = soup.select('.articleSummary')
    articles =[]
    for i, item in enumerate(articlesubject_list):
        a_tag = item.select_one('a')
        title = a_tag.get_text(strip=True)
        href = 'http://finance.naver.com' + a_tag.get("href", "")
        press = articleSummary_list[i].select_one('.press').get_text(strip=True)
        dummy_dict = {'제목': title, 'URL': href, '페이지': page, '언론사': press}
        articles.append(dummy_dict)
    return articles

def finance_news(max_pages =3, delay =1.0):
    all_articles =[]
    for page in range(1, max_pages+1):
        print(f"[{page}/{max_pages}]페이지 수집 중..")
        try:
            articles = parse_page(page)
            all_articles.extend(articles)
        except Exception as e:
            print(e)
        if page < max_pages:
            time.sleep(delay)
    df = pd.DataFrame(all_articles)
    print(f"\n 총 {len(df)}건 수집 완료 \n")
    return df



def N_fin():
    base_url = 'https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258'
    params_base ={'mode': 'LSS2D', 'section_id' :'101', 'section_id2': '258'}
    page =1
    params_base = {**params_base, 'page': page}
    response = requests.get(base_url, params = params_base)
    #print(response)
    soup = bs(response.text, 'html.parser')
    articlesubject_list = soup.select('.articleSubject')
    #print(len(articlesubject_list))
    #print(articlesubject_list[0])
    #print(articlesubject_list[0].select_one('a').get_text(strip=True))
    '''
    for i in articlesubject_list:
        a_tag = i.select_one('a')
        if a_tag is None: # a 태그 없으면 건너뜀
            continue 
        
        title = a_tag.get_text(strip= True)
        href = 'http://finance.naver.com' + a_tag.get('href', '')
        #print(title)
        #print(href)
        #print()
        
   
        #print('http://finance.naver.com'+i.select_one('a').get("href",""))
    #articleSummary_list = soup.select('.articleSummary')# 리스의 리스트로 되어서 로컬에서 작동이 안됨
    
    #print(articleSummary_list[0])

    for item in articleSummary_list:
        press_tag = item.select_one('.press')
        name = press_tag.get_text(strip= True)
        #print(name)
    for i , item in enumerate(articlesubject_list):
        a_tag = item.select_one('a')
        title = a_tag.get_text(strip= True)
        href = 'http://finance.naver.com' + a_tag.get('href',"")
        press = articleSummary_list[i].select('.press').get_text(strip =True)          
        #print(title)
        #print(href)
        #print(press)
        #print()  
        dummy_dict = {'제목': title, 'URL': href, '페이지': page}          
        #print(dummy_dict)   
    '''
    articleSummary_list = soup.select('.articleSummary')
    articles =[]
    for i, item in enumerate(articlesubject_list):
        a_tag = item.select_one('a')
        title = a_tag.get_text(strip=True)
        href = 'http://finance.naver.com' + a_tag.get("href", "")
        press = articleSummary_list[i].select_one('.press').get_text(strip=True)
        dummy_dict = {'제목': title, 'URL': href, '페이지': page, '언론사': press}
        articles.append(dummy_dict)
        #print(articles)
    df = finance_news(4)
    print(df)

def N_tag():
    url ="https://en.wikipedia.org/wiki/List_of_American_exchange-traded_funds"
    headers = {'User-Agent': 'Mozilla/5.0'} #크롤링 전에 User-Agent를 보여준다. 사람이도록 표시
    response = requests.get(url, headers=headers)
    #print(response)
    soup = bs(response.text ,'lxml')
    #print(soup)
    rows = soup.select('div>ul>li')
    #print(len(rows))
    #print(rows[0])
    real_rows = rows[47:]
    #for row in real_rows[-30]:
        #print(row.text)
        
# soup에서 body 태그 영역
#우리가 원하는 데이터는 대체로 li 태그에 있음
    soup.body.find_all('li')  #모든 곳에서의 li를 찾아줌     
    print(soup.body.find_all('li'))

def html():
    html = """
<html>
<body>
  <div id="main">
    <h1 class="title">뉴스 제목</h1>
    <div class="articleSummary">
      <a class="articleSubject" href="/news/001">기사 제목 1</a>
      <span class="press">조선일보</span>
      <span class="date">2024-01-01</span>
    </div>
    <div class="articleSummary">
      <a class="articleSubject" href="/news/002">기사 제목 2</a>
      <span class="press">한겨레</span>
      <span class="date">2024-01-02</span>
    </div>
  </div>
</body>
</html>
"""

    soup_2nd = bs(html,'html.parser')
    #print(soup_2nd.find('h1'))  #h1테그값 조회
    #print(soup_2nd.find_all('span'))
    soup_2nd.select('.articleSummary') # '.' -> class 이름
    divs = soup_2nd.find('div', class_='articleSummary')
    #print(divs)
    #print(divs.children) # div 안에 있는것만 선택됨
    print(divs.parent)# 부모테그(div)까지 다 보여줌
    print(divs.find_next_sibling('div')) #div형제들 중에 div가 있는지 찾기

def api():
    url = "https://openapi.gg.go.kr/Publtolt?key=f027225fa8d34b66a6fab025670941a3&Type=json&pIndex=1&pSize=100"
    resp = requests.get(url)
    result = resp.json()
    #print(result)
    #print(type(result))
    #print(result.keys())
    #print(type(result['Publtolt']))
    #print(result['Publtolt'][1])
    result['Publtolt'][1].keys()
    



