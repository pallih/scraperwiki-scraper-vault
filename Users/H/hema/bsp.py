import scraperwiki

# Blank Python

import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime


#def strip_tags(html):
 #return ' '.join(html.findAll(text=True))

sources  = ['http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dab&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daf&max=90&links=preserve&exc=&submit=Create+Feed']
for i in range(len(sources)):       


    source = sources[i]
   
html = scraperwiki.scrape(source)        

soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) 

items = soup.findAll('item')             
print type(items) 

article = {}
for item in items:
        article['title'] = item.find('title').text
        article['url'] = item.find('link').next # wow, this worked!
        article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
        article['now'] = datetime.now()
        print article
        # the sensfull thing here would be to build a func to scrape the url form here.
        scraperwiki.sqlite.save(['title'], article)
import scraperwiki

# Blank Python

import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime


#def strip_tags(html):
 #return ' '.join(html.findAll(text=True))

sources  = ['http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dab&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daf&max=90&links=preserve&exc=&submit=Create+Feed']
for i in range(len(sources)):       


    source = sources[i]
   
html = scraperwiki.scrape(source)        

soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) 

items = soup.findAll('item')             
print type(items) 

article = {}
for item in items:
        article['title'] = item.find('title').text
        article['url'] = item.find('link').next # wow, this worked!
        article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
        article['now'] = datetime.now()
        print article
        # the sensfull thing here would be to build a func to scrape the url form here.
        scraperwiki.sqlite.save(['title'], article)
