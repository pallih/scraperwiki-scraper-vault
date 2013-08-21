###############################################################################
# Gazeta.pl - WARSZAWA NA EURO2012 SCRAPER
# MARCIN JAKUSZKO - S6712@PJWSTK.EDU.PL
# WARSZAWA NA EURO2012 - BACHELOR PROJECT
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from matplotlib.dates import date2num
from datetime import datetime
import re
import string
import tidylib
import lxml.html

base_url = 'http://uefaeuro2012.um.warszawa.pl'

def univdate(d):
    d = string.replace(d, unicode('grudzień', 'utf-8'), "12")
    d = string.replace(d, "listopad", "11")
    d = string.replace(d, unicode('październik', 'utf-8'), "10")
    d = string.replace(d, unicode('wrzesień', 'utf-8'), "09")
    d = string.replace(d, unicode('sierpień', 'utf-8'), "08")
    d = string.replace(d, "lipiec", "07")
    d = string.replace(d, "czerwiec", "06")
    d = string.replace(d, "maj", "05")
    d = string.replace(d, unicode('kwiecień', 'utf-8'), "04")
    d = string.replace(d, "marzec", "03")
    d = string.replace(d, "luty", "02")
    d = string.replace(d, unicode('styczeń', 'utf-8'), "01")    
    return d


def scrape_news(bodyDiv):
    li = bodyDiv.findAll("dl", { "class" : "Short"})
    for l in li:
        news = {}
        title = l.dt.a.text #news title
        link = base_url + l.dt.a['href'] #link to full news content
        imgUrl = ''
        #if l.find("img"):
        #    imgUrl = l.find("img")['src'] 

        datePub = l.find("span", { "class" : "date-display-single" }).text
        content = l.find("dd", {"class" : "Desc"}).p.text
        source = "Urząd Miasta Warszawa"
        
        print title
        print link
        print datePub
        print content
        print source

        #date = time.strptime(datePub,"%d-%m-%Y %H:%M")
        #print time.strftime("%d-%m-%Y %H:%M",date)
        #dt = datetime.fromtimestamp(date)
        #print date2num(dt)
        
        #date = datetime.strptime(datePub,"%d-%m-%Y %H:%M")
        #print scraperwiki.sqlite.execute("select max(iDate) from 'swdata'")  
        #news['iDate'] = date2num(date) 
        #news['title'] = title
        #news['link'] = link
        #news['imgUrl'] = imgUrl
        #news['datePub'] = datePub
        #news['content'] = content
        #news['source'] = source

        #scraperwiki.sqlite.save(['iDate', 'title', 'datePub', 'content'], news)
        print "Saved!"
        #print title
        #print datePub
        #print imgUrl
        #print link
        #print content
        #print source
        #print '\n'  
        #print '\n'


def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    
    html = lxml.html.fromstring(html)
    html = lxml.html.tostring(html)
    print html
    

    #html = html.decode('utf-8')
    #html = html.encode('utf-8')
    html = BeautifulSoup(html)
    bodyDiv = html.find("body")
    print bodyDiv
    scrape_news(bodyDiv)
    
    #next_link = html.find("a", { "class" : "next" })
    #if next_link:
    #    next_link = base_url + next_link['href']
    #    #print '************\n\n\n' + next_link + '\n\n\n'
    #    scrape_and_look_for_next_link(next_link)
    #    #print '************\n\n\n' + next_link + '\n\n\n'



starting_url = base_url + '/aktualnosci'
#print starting_url
scrape_and_look_for_next_link(starting_url)



