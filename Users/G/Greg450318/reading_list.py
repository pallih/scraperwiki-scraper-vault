import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://www.guardian.co.uk//'
        
html = urllib2.urlopen(site).read()
print html
indiv = re.search("""<div\s*class="\s*component b5 nf-main\s*">.*?<div\s*id="keycontent"\s*class="\s*component nf-main\s*">""", html, re.DOTALL).group(0)

everyheadline = re.findall('<h[13]>.*?</h[13]>', indiv, re.DOTALL)


data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]*?)".*>(?P<story>.+?)</a>', headline, re.DOTALL)
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story').replace("&#039;", "'")
    print link
    print story
    data['headline'] = story
    data['URL'] = link
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    
import scraperwiki
import urllib2
import urlparse
import re
import datetime

site = 'http://www.guardian.co.uk//'
        
html = urllib2.urlopen(site).read()
print html
indiv = re.search("""<div\s*class="\s*component b5 nf-main\s*">.*?<div\s*id="keycontent"\s*class="\s*component nf-main\s*">""", html, re.DOTALL).group(0)

everyheadline = re.findall('<h[13]>.*?</h[13]>', indiv, re.DOTALL)


data = {}

for headline in everyheadline:
    headlines = re.search('<a[^>]*?href="(?P<link>[^"]*?)".*>(?P<story>.+?)</a>', headline, re.DOTALL)
    link = urlparse.urljoin(site, headlines.group('link'))
    story = headlines.group('story').replace("&#039;", "'")
    print link
    print story
    data['headline'] = story
    data['URL'] = link
    data['date'] = datetime.datetime.today().ctime()
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)    
