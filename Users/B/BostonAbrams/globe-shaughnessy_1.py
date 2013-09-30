import scraperwiki
from bs4 import BeautifulSoup
import datetime 
 

def getSummary(url):
    storyHtml = scraperwiki.scrape(url+"?camp=scraper")
    storySoup = BeautifulSoup(storyHtml)
    title = storySoup.title.text.split(' - ')
    storyMeta = storySoup('meta')
    print storyMeta
    for meta in storyMeta:
        if (str(meta).find('name="description"') > 1):
            summary = str(meta).split('"')[1]
            return [summary,title[0]]
    return [title[0],title[0]]

def checkUrl(url,fragment):
    try:
        z = url.find(fragment)
        
        if (z > 0):
            print "match"
            if ((url.find('story.html') > 1) and (url.find('pinterest') < 1)):
                print "it's a story"
                return True
            else:
                print "not a story or its pinterest"
                return False
    except:
        print "no match"
        return False

html = scraperwiki.scrape("http://www.boston.com/ae/restaurants/YKDzsi0HansLF45C2MryiJ/gallery.html")

soup = BeautifulSoup(html)
links = soup.find_all("a")
print links

for a in links:
    z = a.get('href')
    print z
    if checkUrl(z,'/lifestyle/food/2012') or checkUrl(z,'/ae/restaurants/2012'):
        description = getSummary(z)
        print description

        data = {
                'link' : z,
                'title' : description[1], 
                'description': description[0],
                'pubDate':datetime.datetime.today()
                
#'pubDate':time.strftime('%m/%d/%y',time.localtime())
            }
        print data    
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
        break 

import scraperwiki
from bs4 import BeautifulSoup
import datetime 
 

def getSummary(url):
    storyHtml = scraperwiki.scrape(url+"?camp=scraper")
    storySoup = BeautifulSoup(storyHtml)
    title = storySoup.title.text.split(' - ')
    storyMeta = storySoup('meta')
    print storyMeta
    for meta in storyMeta:
        if (str(meta).find('name="description"') > 1):
            summary = str(meta).split('"')[1]
            return [summary,title[0]]
    return [title[0],title[0]]

def checkUrl(url,fragment):
    try:
        z = url.find(fragment)
        
        if (z > 0):
            print "match"
            if ((url.find('story.html') > 1) and (url.find('pinterest') < 1)):
                print "it's a story"
                return True
            else:
                print "not a story or its pinterest"
                return False
    except:
        print "no match"
        return False

html = scraperwiki.scrape("http://www.boston.com/ae/restaurants/YKDzsi0HansLF45C2MryiJ/gallery.html")

soup = BeautifulSoup(html)
links = soup.find_all("a")
print links

for a in links:
    z = a.get('href')
    print z
    if checkUrl(z,'/lifestyle/food/2012') or checkUrl(z,'/ae/restaurants/2012'):
        description = getSummary(z)
        print description

        data = {
                'link' : z,
                'title' : description[1], 
                'description': description[0],
                'pubDate':datetime.datetime.today()
                
#'pubDate':time.strftime('%m/%d/%y',time.localtime())
            }
        print data    
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)
        break 

