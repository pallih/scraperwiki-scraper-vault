import scraperwiki
import urllib2
from bs4 import BeautifulSoup
import datetime

opener = urllib2.build_opener()
opener.addheaders = [('http-referrer', 'http://www.facebook.com')]
opener.addheaders.append(('Cookie', 'pathAuth=33b75135-c62e-45df-9064-96c640d4f949'))


def getSummary(url):
    f=opener.open(url)
    storyHtml = f.read()
    # storyHtml = scraperwiki.scrape(url+"?camp=scraper2")
    storySoup = BeautifulSoup(storyHtml)
    storyMeta = storySoup('meta')
    print storyMeta
    for meta in storyMeta:
        # print str(meta).find('name="description"')
        if (str(meta).find('name="description"') > 1):
            summary = str(meta).split('"')[1]
            print summary
            return summary
    return ""

def checkForValidUrl(url):
    z = url.find('/specials/insiders/20')
        
    if (z > 0):
        print "match"
        return "archive gallery"
    z = url.find('story.html')
        
    if (z > 0):
        print "story"
        return "story"
    return False

def dateStart(url):
    if (url.find('20') > 0):
        return url.find('20')
    else:
        return url.find('19')

f=opener.open("http://www.bostonglobe.com/specials/insiders/fromthearchives?camp=scraper")
html = f.read()
# scraperwiki.scrape("http://www.bostonglobe.com/specials/insiders/fromthearchives?camp=scraper")

soup = BeautifulSoup(html)
links = soup.find_all("a")
print links

for story in links:
    link = story.get('href')
    print link
    if ((link is not None) and (checkForValidUrl(link))):
        if (link.find('bostonglobe.com') < 0):
             link = 'http://www.bostonglobe.com'+link

        description = getSummary(link)
        headline = story.text.strip()
        
        datestring= link[dateStart(link):dateStart(link)+10] + ' 14:00'
        data = {
          'link' : link,
          'title' : headline, 
          'description': description,
          'pubDate':datestring,
          'foundDate':datetime.datetime.today(),
          'linkType':checkForValidUrl(link)
        }
    
        print data
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)

scraperwiki.sqlite.execute("delete from swdata where foundDate is null")import scraperwiki
import urllib2
from bs4 import BeautifulSoup
import datetime

opener = urllib2.build_opener()
opener.addheaders = [('http-referrer', 'http://www.facebook.com')]
opener.addheaders.append(('Cookie', 'pathAuth=33b75135-c62e-45df-9064-96c640d4f949'))


def getSummary(url):
    f=opener.open(url)
    storyHtml = f.read()
    # storyHtml = scraperwiki.scrape(url+"?camp=scraper2")
    storySoup = BeautifulSoup(storyHtml)
    storyMeta = storySoup('meta')
    print storyMeta
    for meta in storyMeta:
        # print str(meta).find('name="description"')
        if (str(meta).find('name="description"') > 1):
            summary = str(meta).split('"')[1]
            print summary
            return summary
    return ""

def checkForValidUrl(url):
    z = url.find('/specials/insiders/20')
        
    if (z > 0):
        print "match"
        return "archive gallery"
    z = url.find('story.html')
        
    if (z > 0):
        print "story"
        return "story"
    return False

def dateStart(url):
    if (url.find('20') > 0):
        return url.find('20')
    else:
        return url.find('19')

f=opener.open("http://www.bostonglobe.com/specials/insiders/fromthearchives?camp=scraper")
html = f.read()
# scraperwiki.scrape("http://www.bostonglobe.com/specials/insiders/fromthearchives?camp=scraper")

soup = BeautifulSoup(html)
links = soup.find_all("a")
print links

for story in links:
    link = story.get('href')
    print link
    if ((link is not None) and (checkForValidUrl(link))):
        if (link.find('bostonglobe.com') < 0):
             link = 'http://www.bostonglobe.com'+link

        description = getSummary(link)
        headline = story.text.strip()
        
        datestring= link[dateStart(link):dateStart(link)+10] + ' 14:00'
        data = {
          'link' : link,
          'title' : headline, 
          'description': description,
          'pubDate':datestring,
          'foundDate':datetime.datetime.today(),
          'linkType':checkForValidUrl(link)
        }
    
        print data
        scraperwiki.sqlite.save(unique_keys=['link'], data=data)

scraperwiki.sqlite.execute("delete from swdata where foundDate is null")