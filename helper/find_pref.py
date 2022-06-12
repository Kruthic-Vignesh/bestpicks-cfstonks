# Gathering users' rating using Codeforces API

import requests
import json
from functools import cmp_to_key


users = ['Kruthic', 'AdC_AB2', 'Hemesh_DJ', 'rainboy', 'Errichto']
ranges = [1200, 1400, 1600, 1900, 2100, 2200, 2400, 2700, 3000]
ratings = []    # tuples: <closest range, rating, user_id>

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
