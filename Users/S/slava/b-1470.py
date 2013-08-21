# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson
import demjson
# Blank Python

#

def fix_json(text):
    text = text.replace("\n","").replace("\t","").replace("  "," ")
    text = re.sub("'(\d+)': {", r' "\1":{', text, 0,  re.I | re.U | re.S)
    text = re.sub("\s*(\w+)\s*:", r"'\1':", text, 0,  re.I | re.U | re.S)
    #text = re.sub(":\s*'(.+?)'\s*(,|})\s*", r': "\1"\2', text,0,  re.I | re.U | re.S)
    return text

def get_field(regexp, text):
    r = re.findall(regexp,text)
    if len(r)>0:
        r = r[0]
    else:
        r = ''
    return r

def get_branch_data(html=''):
    branch_name = get_field(r'class="colBox">.*?<h1>(.+?)</h1',html)
    address = get_field(r'photoArchive-inner">.*?<p>.*?<strong>(.+?)</strong',html)
    latlon = get_field(r"ll=(.+?)&",html)

    if latlon != "": 
        lat = latlon.split(",")[0]
        lon = latlon.split(",")[1]
    else:
        lat = ''
        lon = ''

    return {'lat':lat,'lon':lon, 'branch_name':branch_name , 'address': address }


# get HTML code of the page
html = scraperwiki.scrape("http://www.sviaz-bank.ru/filials/bank-regions/")

cities = re.findall(r'id="blckCities">(.+?)</div', html, re.I | re.U | re.S)
city_links = re.findall(r'href="(.+?)">(.+?)</a', cities[0], re.I | re.U | re.S)
#branches = re.findall(r'class="officeBox">(.+?)</div', html, re.I|re.U|re.S)


i=0
for city_link in city_links:
    #print city_link
    html = scraperwiki.scrape("http://www.sviaz-bank.ru" + city_link[0])

    coords_html = re.findall(r'var items = {(.+)};.*?var map', html, re.I|re.U|re.S)
    #print coords_html
    coords = demjson.decode("{"+coords_html[0]+"}")
    #print coords
    
    for c in coords:
        print c
        print coords[c]
        if coords[c]['ptype_id']!="4": continue

        branch_name = coords[c]['prod_title']
        branch_url = coords[c]['prod_link']
        address = coords[c]['prod_addr']
        
        i+=1
        data = {'id':i, 'lat':coords[c]['prod_lat'], 'lon':coords[c]['prod_lng'],  \
            'branch_url': branch_url, 'branch_name': branch_name , 'address':address }
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="swdata_process")


