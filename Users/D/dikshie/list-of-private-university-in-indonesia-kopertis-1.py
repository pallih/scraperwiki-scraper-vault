import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import sqlite3,os
import time

mech = Browser()
for i in (0,25,50,75,100,125,150,175,200,225,250,275,300):  #make it static for page numbers
    url = "http://www.dikti.go.id/index.php?option=com_qcontacts&view=category&catid=56&Itemid=198&limitstart="
    url = url + str(i)
    page1 = mech.open(url)
    html1 = page1.read()
    root = html.fromstring(html1)  
    print i
    for tr in root.cssselect("tbody tr.sectiontableentry1"):
        tds = tr.cssselect("td")
        data={'name': tds[0].text_content() , 'telp': tds[2].text_content(), 'area': tds[3].text_content()}
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
    for tr in root.cssselect("tbody tr.sectiontableentry2"):
        tds = tr.cssselect("td")
        data={'name': tds[0].text_content() , 'telp': tds[2].text_content(), 'area': tds[3].text_content()}
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)import scraperwiki
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from lxml import html
import sqlite3,os
import time

mech = Browser()
for i in (0,25,50,75,100,125,150,175,200,225,250,275,300):  #make it static for page numbers
    url = "http://www.dikti.go.id/index.php?option=com_qcontacts&view=category&catid=56&Itemid=198&limitstart="
    url = url + str(i)
    page1 = mech.open(url)
    html1 = page1.read()
    root = html.fromstring(html1)  
    print i
    for tr in root.cssselect("tbody tr.sectiontableentry1"):
        tds = tr.cssselect("td")
        data={'name': tds[0].text_content() , 'telp': tds[2].text_content(), 'area': tds[3].text_content()}
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)
    for tr in root.cssselect("tbody tr.sectiontableentry2"):
        tds = tr.cssselect("td")
        data={'name': tds[0].text_content() , 'telp': tds[2].text_content(), 'area': tds[3].text_content()}
        scraperwiki.sqlite.save(unique_keys=['name'], data=data)