#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 14:10:54 2022

@author: kruthic
"""

from bs4 import BeautifulSoup
from selenium import webdriver

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
    
f = open("users.txt", "w")
for user in users:
    f.write(user)
    f.write('\n')
    print(user)