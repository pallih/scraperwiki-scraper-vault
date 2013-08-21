#!/usr/bin/env python

import scraperwiki
import requests
import json
from bs4 import BeautifulSoup
import nltk

html = requests.get("http://www.theyworkforyou.com/api/getMPS?key=AzxEgwDtdDoPAW9T4gDFrwFN&output=js")
MPs_list = html.content.decode("latin-1").encode('utf-8')
MPs_json = json.loads(MPs_list)
for person in MPs_json:
    MP_id = person["person_id"]
    interests_html = requests.get("http://www.theyworkforyou.com/api/getMPsInfo?key=AzxEgwDtdDoPAW9T4gDFrwFN&id=" + MP_id + "&fields=register_member_interests_html&output=js")
    interests_list = interests_html.content.decode("latin-1").encode('utf-8')
    interests_json = json.loads(interests_list)
    soup = BeautifulSoup(interests_json[MP_id]["register_member_interests_html"])
    all_text = soup.get_text()
    tokens = nltk.word_tokenize(all_text)
    tagged = nltk.pos_tag(tokens)
    old_orgs = tagged[:]
    companies = []
    for i, v in enumerate(tagged[:]):
        if v[0] == 'Ltd':
             tagged[i-i] = (tagged[i-1][0] + " " + v[0], "NNP")
             companies.append(tagged[i-1][0] + " " + v[0])

    orgs = filter(lambda x: x[0] != 'Ltd', tagged)
    
    print companies
    #print old_orgs
    #print orgs
    #print "----"


    #x = filter(lambda x: x[0] != 'Ltd', tagged)
    #print x
# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
