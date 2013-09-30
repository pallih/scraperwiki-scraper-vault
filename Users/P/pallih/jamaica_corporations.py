# -*- coding: utf-8 -*-

# jamaica - opencorporates

import scraperwiki
import string
import lxml.html
import time 
import re

regex = re.compile("page=(\d+)")

# http://www.orcjamaica.com/search/showresults2.asp?searchtype=company&search=advanced&stype=1&busname=%25&cnum=&fname=&lname=&recs=30&srch=Search

if scraperwiki.sqlite.get_var('last_page'):
    starturl = 'http://www.orcjamaica.com/search/showresults2.asp?searchtype=company&search=advanced&stype=1&busname=%25&cnum=&fname=&lname=&recs=300&srch=Search&page=' + scraperwiki.sqlite.get_var('last_page')  #300 per page
else:
    starturl = 'http://www.orcjamaica.com/search/showresults2.asp?searchtype=company&search=advanced&stype=1&busname=%25&cnum=&fname=&lname=&recs=300&srch=Search'



def process(html):
    root = lxml.html.fromstring(html)
    content = root.xpath ('//div[@align="center"]/table/tr/td/table/tr[2]')
    data = []
    for x in content:
        record = {}
        record['number'] = x[0][0][0].text
        record['name'] = x[1][0][0].text
        record['type'] = x[1][2][0].text
        record['location'] = x[1][2][2].text
        record['status'] = x[1][2][4].text
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        data.append(record)
    scraperwiki.sqlite.save(['number'], data=data, table_name='jamaica_corporations')

def scrape(url):
    html = scraperwiki.scrape(url)
    process(html)
    root = lxml.html.fromstring(html)
    nextfind = root.xpath('//*[contains(text(),"Next")]')
    if nextfind:
        try:
            next = regex.findall(root.xpath('//*[contains(text(),"Next")]')[0].attrib['href'])
            print 'NEXT PAGE: ', next[0]
            scraperwiki.sqlite.save_var('last_page', next[0])           
            scrape('http://www.orcjamaica.com' + root.xpath('//*[contains(text(),"Next")]')[0].attrib['href'])
        except:
    #else:
            print ' DONE '   
            scraperwiki.sqlite.save_var('last_page', 0) 
scrape(starturl)





# -*- coding: utf-8 -*-

# jamaica - opencorporates

import scraperwiki
import string
import lxml.html
import time 
import re

regex = re.compile("page=(\d+)")

# http://www.orcjamaica.com/search/showresults2.asp?searchtype=company&search=advanced&stype=1&busname=%25&cnum=&fname=&lname=&recs=30&srch=Search

if scraperwiki.sqlite.get_var('last_page'):
    starturl = 'http://www.orcjamaica.com/search/showresults2.asp?searchtype=company&search=advanced&stype=1&busname=%25&cnum=&fname=&lname=&recs=300&srch=Search&page=' + scraperwiki.sqlite.get_var('last_page')  #300 per page
else:
    starturl = 'http://www.orcjamaica.com/search/showresults2.asp?searchtype=company&search=advanced&stype=1&busname=%25&cnum=&fname=&lname=&recs=300&srch=Search'



def process(html):
    root = lxml.html.fromstring(html)
    content = root.xpath ('//div[@align="center"]/table/tr/td/table/tr[2]')
    data = []
    for x in content:
        record = {}
        record['number'] = x[0][0][0].text
        record['name'] = x[1][0][0].text
        record['type'] = x[1][2][0].text
        record['location'] = x[1][2][2].text
        record['status'] = x[1][2][4].text
        record['date_time'] = time.strftime("%a %b %e %T %z %Y", time.gmtime())
        data.append(record)
    scraperwiki.sqlite.save(['number'], data=data, table_name='jamaica_corporations')

def scrape(url):
    html = scraperwiki.scrape(url)
    process(html)
    root = lxml.html.fromstring(html)
    nextfind = root.xpath('//*[contains(text(),"Next")]')
    if nextfind:
        try:
            next = regex.findall(root.xpath('//*[contains(text(),"Next")]')[0].attrib['href'])
            print 'NEXT PAGE: ', next[0]
            scraperwiki.sqlite.save_var('last_page', next[0])           
            scrape('http://www.orcjamaica.com' + root.xpath('//*[contains(text(),"Next")]')[0].attrib['href'])
        except:
    #else:
            print ' DONE '   
            scraperwiki.sqlite.save_var('last_page', 0) 
scrape(starturl)





