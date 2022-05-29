#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 21:51:41 2022

@author: kruthic
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import json
from selenium import webdriver
import pandas as pd
from functools import cmp_to_key
import time

url = "https://codetiger.me/project/StonksCF/explore.html?username=kruthic"

driver = webdriver.Chrome()
driver.get(url)
driver.find_element_by_css_selector('.btn.btn-lg.btn-outline-secondary').click()


page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')
all_tables = soup.find_all('table', {'class': 'table leaderboard'})

users = []

for table in all_tables:
    rows = table.find_all('a')
    for row in rows:
        users.append(row.get_text())

api_url = "https://codeforces.com/api/user.info?handles="
first_fetch = api_url
for i in range(700):
    first_fetch += users[i]
    first_fetch += ';'
    
first_user_info = requests.get(first_fetch)
first_user_content = first_user_info.content

second_fetch = api_url
for i in range(700, len(users)):
    second_fetch += users[i]+';'
    
second_user_info = requests.get(second_fetch)
second_user_content = second_user_info.content

dic1 = json.loads(first_user_content)
req_dic1 = dic1['result']

dic2 = json.loads(second_user_content)
req_dic2 = dic2['result']

n = len(req_dic1)

all_content = []    # min distance to ranges(mi), maxRating  - rating, rating, user

ranges = [1200, 1400, 1600, 1900, 2100, 2300, 2400, 2700, 3000, 10000]
check_str = 'rating'

cur_time = time.time()

for ele in req_dic1:    # ele is a dict containing 1 user's data
    if check_str in ele and (cur_time - ele['lastOnlineTimeSeconds'] < 200000):
        cur_rating = ele['rating']
        
        mi = 4000
        for x in ranges:
            if x > cur_rating:
                mi = min(mi, x-cur_rating)
            
        high_low = ele['maxRating'] - ele['rating']
        user = ele['handle']
        all_content.append([mi, high_low, cur_rating, user])
    
def comparator(p, q):
    if p[0] != q[0]:
        return p[0] - q[0]
    if p[1] != q[1]:
        return q[1] - p[1]
    return q[2] - p[1]

cmp_func = cmp_to_key(comparator)

best = sorted(all_content, key = cmp_func, reverse = False)


