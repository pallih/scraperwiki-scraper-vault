# scrape a twitter screen_name

url = "http://api.twitter.com/1/statuses/user_timeline.xml?screen_name=%s&page=%d"

import urllib2
from lxml import etree
import re
import scraperwiki

ids = {}

def parseTwitterStatus(stat):
    global ids
    interesting_tags = ['created_at', 'text', 'source', 'id']
    
    record = { }
    for t in interesting_tags:
        m = re.findall('.*<%s>(.*?)</%s>' % (t, t), stat, flags=re.DOTALL)
        assert len(m) == 1, m
        record[t] = m[-1]
        if t == 'id':
            if m[-1] not in ids:
                ids[m[-1]] = 0
            ids[m[-1]] += 1
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
                     
        

def main():
    screen_name = "gmp24_1"
    
    statuses = [ ]
    for p in [5]:
        x = urllib2.urlopen(url % (screen_name, p)).read()
        # split into 'status' elements
        statuses.extend(re.findall('<status>(.*?)</status>', x, flags=re.DOTALL))
        
    i = 0
    for s in statuses:
        i += 1
        parseTwitterStatus(s)

        
        
main()
# scrape a twitter screen_name

url = "http://api.twitter.com/1/statuses/user_timeline.xml?screen_name=%s&page=%d"

import urllib2
from lxml import etree
import re
import scraperwiki

ids = {}

def parseTwitterStatus(stat):
    global ids
    interesting_tags = ['created_at', 'text', 'source', 'id']
    
    record = { }
    for t in interesting_tags:
        m = re.findall('.*<%s>(.*?)</%s>' % (t, t), stat, flags=re.DOTALL)
        assert len(m) == 1, m
        record[t] = m[-1]
        if t == 'id':
            if m[-1] not in ids:
                ids[m[-1]] = 0
            ids[m[-1]] += 1
    scraperwiki.sqlite.save(unique_keys=["id"], data=record)
                     
        

def main():
    screen_name = "gmp24_1"
    
    statuses = [ ]
    for p in [5]:
        x = urllib2.urlopen(url % (screen_name, p)).read()
        # split into 'status' elements
        statuses.extend(re.findall('<status>(.*?)</status>', x, flags=re.DOTALL))
        
    i = 0
    for s in statuses:
        i += 1
        parseTwitterStatus(s)

        
        
main()
