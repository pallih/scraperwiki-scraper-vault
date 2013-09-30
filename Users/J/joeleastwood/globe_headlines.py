import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://www.cbc.ca/news/'
        
html = urllib2.urlopen(site).read()
# print html

everyheadline = re.findall('<h3[^>]*?>[\s]*?<a name="clearfix".*?>.*?</h3>', html, re.DOTALL)
print len(everyheadline)

data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]*?)".*>(?P<story>.+?)(<img.*/>.*?)?</a>', headline, re.DOTALL)
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story').replace("&#039;", "'")
    data['headline'] = story
    data['URL'] = link
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    


import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://www.cbc.ca/news/'
        
html = urllib2.urlopen(site).read()
# print html

everyheadline = re.findall('<h3[^>]*?>[\s]*?<a name="clearfix".*?>.*?</h3>', html, re.DOTALL)
print len(everyheadline)

data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]*?)".*>(?P<story>.+?)(<img.*/>.*?)?</a>', headline, re.DOTALL)
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story').replace("&#039;", "'")
    data['headline'] = story
    data['URL'] = link
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    


