# Blank Python
import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://dawn.com/'
        
html = urllib2.urlopen(site).read()
print html

everyheadline = re.findall('<div class="stories"*?>.*?</div>', html, re.DOTALL)
#print everyheadline
#print len(everyheadline)

data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]+?)"[^>]*>(?P<story>.+?)(?:<img.*?>\s)?</a>', headline, re.DOTALL)
    #print headlines 
    #assert headlines, headline
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story')
    print story
    #print link.strip()
    #print story.strip()
    #assert link.strip() and story.strip()
    data['headline'] = story.strip()
    data['URL'] = link.strip()
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    



