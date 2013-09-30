# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import lxml, lxml.html
#import pprint
import re
import json
import urllib
import urllib2
import simplejson
import time
import random
#import demjson
import HTMLParser
import mechanize
import cookielib
from cookielib import CookieJar

h = HTMLParser.HTMLParser()

i=1
def process_table(trs_list):
    global i
    for b in trs_list:
        if len(b.attrib) == 0 or len(b.xpath('td[1]/a[1]'))==0: 
            #print lxml.html.tostring(b)
            continue
        #print b.attrib
        #print b.text_content()
        #
        if b.attrib['class'] == 'region_section':
            el = b.xpath('td[1]/a[1]')
            #print el
            #print el[0]
            #print el[0].text_content()
            region_name = el[0].text_content()
    
        if b.attrib['class'] == 'current_city' :
            el = b.xpath('td[1]/a[1]')
            
            city_name = el[0].xpath('span[1]')
            if len(city_name) > 0 :
                city_name = city_name[0].text_content()
            else:
                city_name = el[0].text_content()
            
            link = el[0].attrib['href']
    
            print region_name, ",", city_name, ",", link
            scraperwiki.sqlite.save(unique_keys=['id'], data={'id': i, 'region': region_name, 'city': city_name, 'link': link}, table_name="regions")
            i+=1

def get_regions():
    html = scraperwiki.scrape("http://www.openbank.ru/ru/about/office/")
    root = lxml.html.document_fromstring(html)
    
    trs = root.xpath('//*[@id="navigation_city_panel"]/table/tr')
    big_cities = trs[0].xpath('td[1]/table/tr')
    process_table(big_cities)
    
    
    regions = trs[2].xpath('td/table/tr')
    process_table(regions)
    #print r.text_content()


def scrape2(url, city_id):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'user_city=23'))
    f = opener.open(url)

    #req = urllib2.Request(url, data=data, headers=headers)
    #f = urllib2.urlopen(req)

    text = f.read()
    f.close()
    
    return text

def scrape3(url):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # input-type values from the html form
    #formdata = { "username" : username, "password": password, "form-id" : "1234" }
    #data_encoded = urllib.urlencode(formdata)
    response = opener.open(url)

    #response = opener.open("http://www.openbank.ru/ru/about/office/")
    content = response.read()
    return content


#br = mechanize.Browser()
# Cookie Jar
#cj = cookielib.LWPCookieJar()
#br.set_cookiejar(cj)
#br.set_handle_robots(False)

#process regions
data = scraperwiki.sqlite.execute("select * from regions")
i=1
for d in data['data']:

    #response = br.open("http://www.openbank.ru/ru/about/office/" + d[2])
    #html = response.read()
    #html = scrape2("http://www.openbank.ru/ru/about/office/", '2')
    #html = scrape3("http://www.openbank.ru/ru/about/office/" + d[2])
    html = scraperwiki.scrape("http://www.openbank.ru/ru/about/office/" + d[2])

    #new_url = re.findall(r'<meta http-equiv="Refresh" content="0; URL=(.+?)"', html, re.I|re.U|re.S)[0]

    #html = scraperwiki.scrape(new_url)
    html = html.decode('windows-1251').encode('utf-8')

    #print html
    #root = lxml.html.document_fromstring(html)
    #el = root.xpath('//*[@id="wrapper"]/table/tbody/tr[3]/td[2]/div[3]/table/tbody/tr[1]/td[1]/h4')
    #print html

    coords = re.findall(r'createObject\("Placemark", new YMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\),.*?".*?",.*?"(.+?)"', html, re.U|re.I|re.S)
    table=re.findall(r'<table class="grey">(.+?)</table', html, re.I|re.U|re.S)[0]
    branches = re.findall(r'<th style="text-align: center;" colspan="3">(.+?)</.*?<td>(.+?)</td', html, re.I|re.U|re.S)

    if branches == []:
        branches = re.findall(r'<tr>.*?<td>.*?<h4>(.+?)</h4>.*?<td>(.+?)</td', html, re.I|re.U|re.S)
    

    data = []
    for b in branches:
        branch = {'name': b[0], 'address': b[1], 'lat': '', 'lng':''}
        for c in coords:
            if branch['name'].find(c[2]) != -1:
                branch['lat'] = c[1]
                branch['lng'] = c[0]
                break
        data.append(branch)
        


    print data
    exit()
    for tr in root.xpath('//*[@class="body_sec"]/table/tbody/tr'):
        print tr
        title = tr.xpath('td[1]/h4[1]')
        if len(title)>0:
            title = title[0].text_content()
            address = tr.xpath('td[2]')[0].text_content()
            
            print title, address
    exit()



# -*- coding: utf-8 -*-

import scraperwiki
import mechanize
import lxml, lxml.html
#import pprint
import re
import json
import urllib
import urllib2
import simplejson
import time
import random
#import demjson
import HTMLParser
import mechanize
import cookielib
from cookielib import CookieJar

h = HTMLParser.HTMLParser()

i=1
def process_table(trs_list):
    global i
    for b in trs_list:
        if len(b.attrib) == 0 or len(b.xpath('td[1]/a[1]'))==0: 
            #print lxml.html.tostring(b)
            continue
        #print b.attrib
        #print b.text_content()
        #
        if b.attrib['class'] == 'region_section':
            el = b.xpath('td[1]/a[1]')
            #print el
            #print el[0]
            #print el[0].text_content()
            region_name = el[0].text_content()
    
        if b.attrib['class'] == 'current_city' :
            el = b.xpath('td[1]/a[1]')
            
            city_name = el[0].xpath('span[1]')
            if len(city_name) > 0 :
                city_name = city_name[0].text_content()
            else:
                city_name = el[0].text_content()
            
            link = el[0].attrib['href']
    
            print region_name, ",", city_name, ",", link
            scraperwiki.sqlite.save(unique_keys=['id'], data={'id': i, 'region': region_name, 'city': city_name, 'link': link}, table_name="regions")
            i+=1

def get_regions():
    html = scraperwiki.scrape("http://www.openbank.ru/ru/about/office/")
    root = lxml.html.document_fromstring(html)
    
    trs = root.xpath('//*[@id="navigation_city_panel"]/table/tr')
    big_cities = trs[0].xpath('td[1]/table/tr')
    process_table(big_cities)
    
    
    regions = trs[2].xpath('td/table/tr')
    process_table(regions)
    #print r.text_content()


def scrape2(url, city_id):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'user_city=23'))
    f = opener.open(url)

    #req = urllib2.Request(url, data=data, headers=headers)
    #f = urllib2.urlopen(req)

    text = f.read()
    f.close()
    
    return text

def scrape3(url):
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # input-type values from the html form
    #formdata = { "username" : username, "password": password, "form-id" : "1234" }
    #data_encoded = urllib.urlencode(formdata)
    response = opener.open(url)

    #response = opener.open("http://www.openbank.ru/ru/about/office/")
    content = response.read()
    return content


#br = mechanize.Browser()
# Cookie Jar
#cj = cookielib.LWPCookieJar()
#br.set_cookiejar(cj)
#br.set_handle_robots(False)

#process regions
data = scraperwiki.sqlite.execute("select * from regions")
i=1
for d in data['data']:

    #response = br.open("http://www.openbank.ru/ru/about/office/" + d[2])
    #html = response.read()
    #html = scrape2("http://www.openbank.ru/ru/about/office/", '2')
    #html = scrape3("http://www.openbank.ru/ru/about/office/" + d[2])
    html = scraperwiki.scrape("http://www.openbank.ru/ru/about/office/" + d[2])

    #new_url = re.findall(r'<meta http-equiv="Refresh" content="0; URL=(.+?)"', html, re.I|re.U|re.S)[0]

    #html = scraperwiki.scrape(new_url)
    html = html.decode('windows-1251').encode('utf-8')

    #print html
    #root = lxml.html.document_fromstring(html)
    #el = root.xpath('//*[@id="wrapper"]/table/tbody/tr[3]/td[2]/div[3]/table/tbody/tr[1]/td[1]/h4')
    #print html

    coords = re.findall(r'createObject\("Placemark", new YMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\),.*?".*?",.*?"(.+?)"', html, re.U|re.I|re.S)
    table=re.findall(r'<table class="grey">(.+?)</table', html, re.I|re.U|re.S)[0]
    branches = re.findall(r'<th style="text-align: center;" colspan="3">(.+?)</.*?<td>(.+?)</td', html, re.I|re.U|re.S)

    if branches == []:
        branches = re.findall(r'<tr>.*?<td>.*?<h4>(.+?)</h4>.*?<td>(.+?)</td', html, re.I|re.U|re.S)
    

    data = []
    for b in branches:
        branch = {'name': b[0], 'address': b[1], 'lat': '', 'lng':''}
        for c in coords:
            if branch['name'].find(c[2]) != -1:
                branch['lat'] = c[1]
                branch['lng'] = c[0]
                break
        data.append(branch)
        


    print data
    exit()
    for tr in root.xpath('//*[@class="body_sec"]/table/tbody/tr'):
        print tr
        title = tr.xpath('td[1]/h4[1]')
        if len(title)>0:
            title = title[0].text_content()
            address = tr.xpath('td[2]')[0].text_content()
            
            print title, address
    exit()



