# -*- coding: utf-8 -*-

import scraperwiki
import lxml, lxml.html
import pprint
import re
import json
import simplejson


address_re = re.compile(""".*?<strong>(.+?)</strong>.*?<br.*?>(.+?)</""", re.I | re.U | re.S )
branches_re = re.compile("""<script.+?arBranches.+?\[(.+?)\].+?</script>""", re.I | re.U | re.S )
branches_re1 = re.compile("""arBranches.+?\[(.+?)\]""", re.I | re.U | re.S )

items_re = re.compile('<tbody.*?class="adr-list">(.+?)</tbody>', re.I | re.U | re.S )
item_re1 = re.compile("""<td.*?<a.*?href="(.+?)".*?>(.+?)<\/a>.*?<td.*?>(.+?)<\/td""", re.I | re.U | re.S )

item_re2 = re.compile("""<td.*?</td>.*?<td.*?>(.+?)<\/td""", re.I | re.U | re.S )

# get links

html = scraperwiki.scrape("http://www.vtb.ru/group/contacts/geography/russia/")
root = lxml.html.fromstring(html)


i=0
for el in root.cssselect("div.points li.item a.dot"):
    url = "http://www.vtb.ru" + el.attrib.get('href')
    print "Scraping: " + url

    b_html = scraperwiki.scrape(url)

    cnt = int(re.findall("arBranches.+?\((\d+?)\s", b_html)[0])

    if cnt>0:
        branches = branches_re.findall(b_html)
        for branch in branches:
            
            points = simplejson.loads("["+branch+"]")
            for point in points:
                i+=1
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id': i, 'url': url, 'lat': point['USRLTD'], 'lon': point['USRLNG'], \
                    'name': point['NAME'], 'address': point['ADDRESS'], 'detail_page_url': point['DETAIL_PAGE_URL']})

    else:
        #b_root = lxml.html.fromstring(b_html)
        m = items_re.findall(b_html)
        m1 = item_re1.findall(m[0])
    
        #if len(m1) == 0: m1 = item_re2.findall(m[0])
    
        if len(m1)>1:
            for t in m1:
                if len(t)>1:
                    branch_name =  t[1]
                    branch_url = t[0]
                    address = t[2]
                else:
                    branch_name =  ''
                    branch_url = ''
                    address = t[0]                    
                i+=1
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id': i, 'url': url, 'lat': '', 'lon': '', \
                    'name': branch_name, 'address': address , 'detail_page_url': branch_url})

