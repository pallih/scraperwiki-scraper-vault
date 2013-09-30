###############################################################################
# Gazeta.pl - WARSZAWA NA EURO2012 SCRAPER
# MARCIN JAKUSZKO - S6712@PJWSTK.EDU.PL
# WARSZAWA NA EURO2012 - BACHELOR PROJECT
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from matplotlib.dates import date2num
from datetime import datetime
import re, copy
import string
import htmllib

base_url = 'http://www.tvnwarszawa.pl'

hexentityMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
# replace hexadecimal character reference by decimal one
hexentityMassage += [(re.compile('&#x([^;]+);'), 
                     lambda m: '&#%d;' % int(m.group(1), 16))]

def convert(html):
    return BeautifulSoup(html,
        convertEntities=BeautifulSoup.HTML_ENTITIES,
        markupMassage=hexentityMassage).contents[0].string


def scrape_news(bodyDiv):
    
    global base_url    

    li = bodyDiv.findAll("li", { "class" : re.compile("item")})
    for l in li:
        news = {}

        h2 = l.find("div", {"class" : "heading"})
        title = h2.a['title'] #news title
        link =  base_url + h2.a['href'] #link to full news content
        imgUrl = ''
        if l.find("img"):
            imgUrl = l.find("img")['src'] 

        datePub = l.find("p", { "class" : "date" }).text
        content = l.find("div", {"class" : "content"}).p
        a = content.find("a")
        a.extract()
        if content.text !='':
            print 'CONVERT!'
            content = convert(content.text)
        
        source = "TVN Warszawa"

        #date = time.strptime(datePub,"%d-%m-%Y %H:%M")
        #print time.strftime("%d-%m-%Y %H:%M",date)
        #dt = datetime.fromtimestamp(date)
        #print date2num(dt)
        
        date = datetime.strptime(datePub,"%d.%m.%Y %H:%M")
        
        news['iDate'] = date2num(date) 
        news['title'] = title
        news['link'] = link
        news['imgUrl'] = imgUrl
        news['datePub'] = datePub
        news['content'] = content
        news['source'] = source

        scraperwiki.sqlite.save(news.keys(), news)
        print "Saved!"
        #print news['iDate']
        #print title
        #print datePub
        #print imgUrl
        #print link
        #print content
        #print source
        #print '\n'  
        #print '\n'

def scrape_and_look_for_next_link(url):
    url = string.replace(url,' ', '%20');
    html = scraperwiki.scrape(url)
    html = html.decode('utf-8')
    html = html.encode('utf-8')
    html = BeautifulSoup(html)
    bodyDiv = html.find("ul", { "class" : "newsList search" })
    scrape_news(bodyDiv)
    next_link = html.find("a", { "class" : "next" })
    if next_link:
        next_link = base_url + next_link['href']
        #print '************\n\n\n' + next_link + '\n\n\n'
        scrape_and_look_for_next_link(next_link)
        #print '************\n\n\n' + next_link + '\n\n\n'



starting_url = base_url + '/search,all.html?q=euro%26%262012&internal_search=1'
#print starting_url
scrape_and_look_for_next_link(starting_url)



###############################################################################
# Gazeta.pl - WARSZAWA NA EURO2012 SCRAPER
# MARCIN JAKUSZKO - S6712@PJWSTK.EDU.PL
# WARSZAWA NA EURO2012 - BACHELOR PROJECT
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from matplotlib.dates import date2num
from datetime import datetime
import re, copy
import string
import htmllib

base_url = 'http://www.tvnwarszawa.pl'

hexentityMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
# replace hexadecimal character reference by decimal one
hexentityMassage += [(re.compile('&#x([^;]+);'), 
                     lambda m: '&#%d;' % int(m.group(1), 16))]

def convert(html):
    return BeautifulSoup(html,
        convertEntities=BeautifulSoup.HTML_ENTITIES,
        markupMassage=hexentityMassage).contents[0].string


def scrape_news(bodyDiv):
    
    global base_url    

    li = bodyDiv.findAll("li", { "class" : re.compile("item")})
    for l in li:
        news = {}

        h2 = l.find("div", {"class" : "heading"})
        title = h2.a['title'] #news title
        link =  base_url + h2.a['href'] #link to full news content
        imgUrl = ''
        if l.find("img"):
            imgUrl = l.find("img")['src'] 

        datePub = l.find("p", { "class" : "date" }).text
        content = l.find("div", {"class" : "content"}).p
        a = content.find("a")
        a.extract()
        if content.text !='':
            print 'CONVERT!'
            content = convert(content.text)
        
        source = "TVN Warszawa"

        #date = time.strptime(datePub,"%d-%m-%Y %H:%M")
        #print time.strftime("%d-%m-%Y %H:%M",date)
        #dt = datetime.fromtimestamp(date)
        #print date2num(dt)
        
        date = datetime.strptime(datePub,"%d.%m.%Y %H:%M")
        
        news['iDate'] = date2num(date) 
        news['title'] = title
        news['link'] = link
        news['imgUrl'] = imgUrl
        news['datePub'] = datePub
        news['content'] = content
        news['source'] = source

        scraperwiki.sqlite.save(news.keys(), news)
        print "Saved!"
        #print news['iDate']
        #print title
        #print datePub
        #print imgUrl
        #print link
        #print content
        #print source
        #print '\n'  
        #print '\n'

def scrape_and_look_for_next_link(url):
    url = string.replace(url,' ', '%20');
    html = scraperwiki.scrape(url)
    html = html.decode('utf-8')
    html = html.encode('utf-8')
    html = BeautifulSoup(html)
    bodyDiv = html.find("ul", { "class" : "newsList search" })
    scrape_news(bodyDiv)
    next_link = html.find("a", { "class" : "next" })
    if next_link:
        next_link = base_url + next_link['href']
        #print '************\n\n\n' + next_link + '\n\n\n'
        scrape_and_look_for_next_link(next_link)
        #print '************\n\n\n' + next_link + '\n\n\n'



starting_url = base_url + '/search,all.html?q=euro%26%262012&internal_search=1'
#print starting_url
scrape_and_look_for_next_link(starting_url)



