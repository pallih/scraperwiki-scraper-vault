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
import locale


base_url = 'http://www.2012.org.pl'

hexentityMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
# replace hexadecimal character reference by decimal one
hexentityMassage += [(re.compile('&#x([^;]+);'), 
                     lambda m: '&#%d;' % int(m.group(1), 16))]

def convert(html):
    return BeautifulSoup(html,
        convertEntities=BeautifulSoup.HTML_ENTITIES,
        markupMassage=hexentityMassage).contents[0].string

def univdate(d):
    d = string.replace(d, "grudnia", "12")
    d = string.replace(d, "listopada", "11")
    d = string.replace(d, unicode('października', 'utf-8'), "10")
    d = string.replace(d, unicode('września', 'utf-8'), "09")
    d = string.replace(d, "sierpnia", "08")
    d = string.replace(d, "lipca", "07")
    d = string.replace(d, "czerwca", "06")
    d = string.replace(d, "maja", "05")
    d = string.replace(d, "kwietnia", "04")
    d = string.replace(d, "marca", "03")
    d = string.replace(d, "lutego", "02")
    d = string.replace(d, "stycznia", "01")    
    return d

def scrape_news(bodyDiv):
    
    global base_url    

    li = bodyDiv.findAll("div", { "class" : re.compile("contentpaneopen")})
    for l in li:
        news = {}

        h2 = l.h2
        title = h2.text
        print title
        link=''
        newlink=''
        if l.find("p", { "class" : "readmore"}): # news bez sekcji read more
            try:
                newlink = l.p.a['href']
                link =  base_url + newlink  #link to full news content
            except TypeError:
                print "TypeErrorOccured!"# user put something non-numeric in, tell them off
                

        imgUrl = ''
        div = l.find("div", { "class" : "article-content"})

        if div.find("img"):  #bo sa newsy ktore nie maja zdjecia
            imgTmpUrl = div.find("img")['src']
            imgUrl = base_url + imgTmpUrl 

        datePub = l.find("dd", { "class" : "create" }).text
        content = l.find("div", {"class" : "article-content"}).text     
        
        source = "PL.2012"

        #date = time.strptime(datePub,"%d-%m-%Y %H:%M")
        #print time.strftime("%d-%m-%Y %H:%M",date)
        #dt = datetime.fromtimestamp(date)
        #print date2num(dt)
        
        #locale.setlocale(locale.LC_ALL, 'pl_PL')
        #print locale.getlocale()
        
        date = univdate(datePub)
        #print date
        date = datetime.strptime(date,"%d %m %Y %H:%M")
        
        news['iDate'] = date2num(date) 
        news['title'] = title
        news['link'] = link
        news['imgUrl'] = imgUrl
        news['datePub'] = datePub
        news['content'] = content
        news['source'] = source

        scraperwiki.sqlite.save(['iDate', 'title', 'datePub', 'content'], news)
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
    scrape_news(html)
    next_link = html.find("li", { "class" : "pagination-next" })
    if next_link:
        next_link = base_url + next_link.strong.a['href']
        print '************\n\n\n' + next_link + '\n\n\n'
        #scrape_and_look_for_next_link(next_link)        
        #print '************\n\n\n' + next_link + '\n\n\n'
        next_link = string.replace(next_link,' ','%20');
        html1 = scraperwiki.scrape(next_link)
        html1.decode('utf-8')
        #html1.encode('utf-8')
        html1 = BeautifulSoup(html1)
        scrape_news(html1)





starting_url = base_url + '/pl/aktualnosci/miasta/warszawa-3.html'
#print starting_url
scrape_and_look_for_next_link(starting_url)



