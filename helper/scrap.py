#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 21:51:41 2022

@author: kruthic
"""

import requests
import json
from functools import cmp_to_key
import requests
from bs4 import BeautifulSoup
import numpy as np
import json
from selenium import webdriver
import pandas as pd

users = []
ranges = [1200, 1400, 1600, 1900, 2100, 2200, 2400, 2700, 3000]
ratings = []    # tuples: <closest range, rating, user_id>

url = "https://codetiger.me/project/StonksCF/explore.html?username=kruthic"

driver = webdriver.Chrome()
driver.get(url)
driver.find_element_by_css_selector('.btn.btn-lg.btn-outline-secondary').click()


page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')
all_a = soup.find_all('a')
all_tables = soup.find_all('table', {'class': 'table leaderboard'})

for table in all_tables:
    rows = table.find_all('a')
    for row in rows:
        users.append(row.get_text())
        
        
def get_rating(user):
    url = "https://codeforces.com/api/user.rating?handle={}".format(user)
    r = requests.get(url)
    info = r.content
    dic = json.loads(info)
    req_dic = dic['result']
    n = len(req_dic)
    rating = req_dic[n-1]['newRating']
    mi = 4000
    for x in ranges:
        mi = min(mi, abs(x-rating))
    ratings.append([mi, rating, user])

def comparator(p, q):
    if p[0] == q[0]:
        return q[1] - p[1]
    else:
        return p[0] - q[0]

func = cmp_to_key(comparator)


for user in users:
    get_rating(user)
    
liss = sorted(ratings, key = func, reverse = False)
