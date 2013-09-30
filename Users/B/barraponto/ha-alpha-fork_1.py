from urlparse import urljoin
import scraperwiki
from lxml.html import parse
import urllib
import csv

# fill in the input file here
url = "http://www.express-yourself.com/Book2aiTest.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

images2 = []

for row in clist[:1016]:
    data= dict(zip(headers, row))
    #save to database
    #unique_keys = headers # Change this to the fields that uniquely identify a row
    #scraperwiki.sqlite.save(unique_keys, data, table_name='alpha')
    images = [] # start with an empty list
    url=data['ha_url'] # the url of the page to grab images from
    print '*',url,'*'
    if url=='': continue # no url
    try:
        document = parse(url).getroot()
        document.make_links_absolute() # resolve the relative paths
        for i,img in enumerate(document.cssselect('img')): # for each <img>...
            if img.get('src'): # not all img have src
                images.append(img.get('src')) # put the URL of that image, the src attribute, into the list
                images2.append({'ha_url': url, 'logo_url': img.get('src'), 'id': i})
        scraperwiki.sqlite.save(unique_keys=["logo_url"], data={"ha_url": url, "logo_url": images}, table_name='img')
    except IOError: # servers might be offline 
        pass
scraperwiki.sqlite.save(unique_keys=['ha_url', 'id'], data=images2, table_name='imgs')from urlparse import urljoin
import scraperwiki
from lxml.html import parse
import urllib
import csv

# fill in the input file here
url = "http://www.express-yourself.com/Book2aiTest.csv"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines))

headers = clist.pop(0)
print "There are %d columns and %d rows" % (len(headers), len(clist))
print "Headers:", headers

images2 = []

for row in clist[:1016]:
    data= dict(zip(headers, row))
    #save to database
    #unique_keys = headers # Change this to the fields that uniquely identify a row
    #scraperwiki.sqlite.save(unique_keys, data, table_name='alpha')
    images = [] # start with an empty list
    url=data['ha_url'] # the url of the page to grab images from
    print '*',url,'*'
    if url=='': continue # no url
    try:
        document = parse(url).getroot()
        document.make_links_absolute() # resolve the relative paths
        for i,img in enumerate(document.cssselect('img')): # for each <img>...
            if img.get('src'): # not all img have src
                images.append(img.get('src')) # put the URL of that image, the src attribute, into the list
                images2.append({'ha_url': url, 'logo_url': img.get('src'), 'id': i})
        scraperwiki.sqlite.save(unique_keys=["logo_url"], data={"ha_url": url, "logo_url": images}, table_name='img')
    except IOError: # servers might be offline 
        pass
scraperwiki.sqlite.save(unique_keys=['ha_url', 'id'], data=images2, table_name='imgs')