import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://www.theglobeandmail.com/'
        
html = urllib2.urlopen(site).read()
print html

everyheadline = re.findall('<h2 class="f.*?>.*?</h2>', html, re.DOTALL)
print everyheadline
print len(everyheadline)

data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]*?)".*>(?P<story>.+?)</a>', headline, re.DOTALL)
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story').replace("&#8216;", "'").replace("&#8217;", "'")
    print link
    print story.strip()
    data['headline'] = story
    data['URL'] = link
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    
