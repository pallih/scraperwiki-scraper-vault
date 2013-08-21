import scraperwiki  
import lxml.html 
import simplejson
import urllib2
import re
import time
import BeautifulSoup
        
after = 't3_15s9s1'
page = -25
count = 0

while page < 500:
    page += 25
    url = 'http://www.reddit.com/r/wheredidthesodago/?count=%s&after=%s' % (page, after)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    try:    
        for el in root.cssselect("p.title > a"):    
            if el.attrib['href'].find(".com") > 0 and count < 24:
                data = {
                    'title' : el.text,
                    'url' : el.attrib['href']
                }
                count += 1
                scraperwiki.sqlite.save(unique_keys=['url'], data=data)
            else:
                count = 0
                time.sleep(5)
                html_page = urllib2.urlopen(url)
                soup = BeautifulSoup(html_page)
                for link in soup.findAll('next'):
                    print link.get('href')
                time.sleep(5)
    except:
        print 'Failed!'