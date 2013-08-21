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



def scrape_news(bodyDiv):
    
    li = bodyDiv.findAll("li", { "class" : re.compile("article")})
    for l in li:
        news = {}
        title = l.h2.text #news title
        link = l.h2.a['href'] #link to full news content
        imgUrl = ''
        if l.find("img"):
            imgUrl = l.find("img")['src'] 

        datePub = l.find("span", { "class" : "when" }).text
        content = l.find("p", {"class" : "lead"}).text
        source = "Gazeta.pl"

        #date = time.strptime(datePub,"%d-%m-%Y %H:%M")
        #print time.strftime("%d-%m-%Y %H:%M",date)
        #dt = datetime.fromtimestamp(date)
        #print date2num(dt)
        
        date = datetime.strptime(datePub,"%d-%m-%Y %H:%M")
        #print scraperwiki.sqlite.execute("select max(iDate) from 'swdata'")  
        news['iDate'] = date2num(date) 
        news['title'] = title
        news['link'] = link
        news['imgUrl'] = imgUrl
        news['datePub'] = datePub
        news['content'] = content
        news['source'] = source

        scraperwiki.sqlite.save(['iDate', 'title', 'datePub', 'content'], news)
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
    html = html.decode('iso-8859-2')
    html = html.encode('utf-8')
    html = BeautifulSoup(html)
    bodyDiv = html.find("div", { "class" : "body" })
    scrape_news(bodyDiv)
    next_link = html.find("a", { "class" : "next" })
    if next_link:
        next_link = base_url + next_link['href']
        #print '************\n\n\n' + next_link + '\n\n\n'
        scrape_and_look_for_next_link(next_link)
        #print '************\n\n\n' + next_link + '\n\n\n'


base_url = 'http://warszawa.gazeta.pl/'
starting_url = base_url + 'warszawa/0,80197.html'
#print starting_url
scrape_and_look_for_next_link(starting_url)



