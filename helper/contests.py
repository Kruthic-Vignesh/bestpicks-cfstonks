#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 19 16:31:09 2022

@author: kruthic
"""

import requests
import json

url = "https://codeforces.com/api/contest.list"

r = requests.get(url)
contests_cont = r.content
contests_json = json.loads(contests_cont)
