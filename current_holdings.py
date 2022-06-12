#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:22:57 2022

@author: kruthic
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

url = "https://codetiger.me/project/StonksCF/explore.html?username=kruthic"  

driver = webdriver.Chrome()
driver.get(url)

page = driver.page_source

soup = BeautifulSoup(page, 'html.parser')

all_tables = soup.find_all('tbody', {'id': 'holdings'})

user_list = []

for table in all_tables:
    entries = table.find_all('td')
    new_user = []
    for entry in entries:
        new_user.append(entry.get_text())
        if len(new_user) == 4:
            new_user[1] = (float)(new_user[1][1:])
            new_user[2] = (float)(new_user[2][1:])
            new_user[3] = (int)(new_user[3])
            user_list.append(new_user)
            new_user = []
            
net = 46118.06
holdings = pd.DataFrame(user_list, columns = ["username", "cur price", "buy price", "qty"])
amount = []
for i in range(len(holdings)):
    amount.append(holdings.loc[i]['buy price'] * holdings.loc[i]['qty'])

holdings['amt'] = amount