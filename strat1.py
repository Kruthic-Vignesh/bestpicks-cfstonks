#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 15:56:26 2022

@author: kruthic
"""

import requests
import json
from functools import cmp_to_key
import time

users = []
f = open("users.txt", "r")

for line in f:
    for word in line.split():
        users.append(word)

# Using CodeForces API to get user info
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
users_info = dic1['result']

dic2 = json.loads(second_user_content)
users_info += dic2['result']

all_content = []    # min distance to ranges(mi), maxRating  - rating, rating, user

ranges = [1200, 1400, 1600, 1900, 2100, 2300, 2400, 2700, 3000, 10000]
check_str = 'rating'

cur_time = time.time()

for ele in users_info:    # ele is a dict containing 1 user's data
    if check_str in ele and (cur_time - ele['lastOnlineTimeSeconds'] < 200000): # user should've been online in the last 2e5 (~2 days)
        cur_rating = ele['rating']
        
        mi = 4000
        for x in ranges:
            if x > cur_rating:
                mi = min(mi, x-cur_rating)
            
        high_low = ele['maxRating'] - ele['rating']
        user = ele['handle']
        all_content.append([mi, high_low, cur_rating, user])

def comparator(p, q):   # Closest to range > Max difference in maxrating - cur_rating
    if p[0] != q[0]:
        return p[0] - q[0]
    if p[1] != q[1]:
        return q[1] - p[1]
    return q[2] - p[1]

cmp_func = cmp_to_key(comparator)

best = sorted(all_content, key = cmp_func, reverse = False)