import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://uk.reuters.com/'
        
html = urllib2.urlopen(site).read()
print html
indiv = re.search("""<div class="column1 gridPanel grid8">.*?<div class="column2 gridPanel grid4">""", html, re.DOTALL).group(0)

everyheadline = re.findall('<h2>.*?</h2>', indiv, re.DOTALL)
print everyheadline
print len(everyheadline)

data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]*?)".*>(?P<story>.+?)</a>', headline, re.DOTALL)
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story')
    print link
    print story
    data['headline'] = story
    data['URL'] = link
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    


