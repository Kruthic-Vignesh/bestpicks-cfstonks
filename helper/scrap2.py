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
        print(row.get_text())
