from urllib import urlopen
from BeautifulSoup import BeautifulSoup 
import re
import scraperwiki

#open and read webpage
webpage = urlopen("http://feeds.huffingtonpost.com/huffingtonpost/raw_feed").read()

#locate article title
title = re.compile('<title>(.*)</title>')

#locate article link
link = re.compile("<link rel.*href=(.*)/>")

#search for article title
findtitle = re.findall(title, webpage)

#search for article link
findlink = re.findall(link, webpage)

#determine what to titles / links to grab (2nd through 16th)
listiterator = []
listiterator[:] = range(2,16)

for i in listiterator:
    data = {}
    data["Title"] = findtitle[i]
    data["Link"] = findlink[i]
    
    scraperwiki.sqlite.save(["Title"], data) 
