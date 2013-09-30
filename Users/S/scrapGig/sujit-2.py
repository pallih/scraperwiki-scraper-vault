# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import urllib2
import urllib
import lxml.html
import BeautifulSoup as bs
import re    
import xml.etree.ElementTree as ET

# Blank Python
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib

import re

totalLinks =[]
for i in range(21)[1:]:
    strAddr = "http://codingtrying.herobo.com/"+str(i)+".html"
    html = urllib.urlopen(strAddr)
    html = html.read()
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    mainContent = tree.xpath("//th[@class='rowA']/a/@href")
    for content in mainContent:
        if content !="http://www.dlapiper.com/us/people/#":
            totalLinks.append(content)




i=0;
for url in totalLinks:
    if i<=481:
        i=i+1
        continue
    try:           
        page = scraperwiki.scrape(url)
        html = bs.BeautifulSoup(page)
        lawer_name = html.findAll('h1')
        lawer_post = html.findAll('h2')
        root = lxml.html.fromstring(page)
        links = root.cssselect("div.bio a")
        contact = root.cssselect("div.bio td")
        data = {'name':lawer_name[4].getText(), 'post' : lawer_post[3].getText(), 'email' : links[0].text, 'contact':contact[0].text_content(),'id':i}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        i=i+1
    except:
        pass
                                
    
    
    
    
# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import urllib2
import urllib
import lxml.html
import BeautifulSoup as bs
import re    
import xml.etree.ElementTree as ET

# Blank Python
#import json #for json decoding
from lxml import etree     
from cStringIO import StringIO
import urllib

import re

totalLinks =[]
for i in range(21)[1:]:
    strAddr = "http://codingtrying.herobo.com/"+str(i)+".html"
    html = urllib.urlopen(strAddr)
    html = html.read()
    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(html), parser)
    mainContent = tree.xpath("//th[@class='rowA']/a/@href")
    for content in mainContent:
        if content !="http://www.dlapiper.com/us/people/#":
            totalLinks.append(content)




i=0;
for url in totalLinks:
    if i<=481:
        i=i+1
        continue
    try:           
        page = scraperwiki.scrape(url)
        html = bs.BeautifulSoup(page)
        lawer_name = html.findAll('h1')
        lawer_post = html.findAll('h2')
        root = lxml.html.fromstring(page)
        links = root.cssselect("div.bio a")
        contact = root.cssselect("div.bio td")
        data = {'name':lawer_name[4].getText(), 'post' : lawer_post[3].getText(), 'email' : links[0].text, 'contact':contact[0].text_content(),'id':i}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
        i=i+1
    except:
        pass
                                
    
    
    
    
