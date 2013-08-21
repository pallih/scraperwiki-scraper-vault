from urlparse import urljoin
import scraperwiki
from bs4 import BeautifulSoup
import urllib
import csv

# fill in the input file here
url = "http://www.express-yourself.com/Book2.csv"

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
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    for i,imgtag in enumerate(soup.find_all('img')): # for each <img>...
        try:
            images.append(imgtag['src']) # put the URL of that image, the src attribute, into the list
            ujoin=urljoin(url, imgtag['src'])
            images2.append({'ha_url':url, 'logo_url':ujoin, 'id':i})
        except KeyError:
            pass # not all img tags have src...
    scraperwiki.sqlite.save(unique_keys=["logo_url"], data={"ha_url": url,"logo_url": images}, table_name='img')
scraperwiki.sqlite.save(unique_keys=['ha_url','id'], data=images2, table_name='imgs')

#verbage = []
#verbage2 = []
#url=data['ha_url']
#print '*',url,'*'
#if url=='': continue
#if url=='': continue
#html = urllib.urlopen(url).read()
#soup = BeautifulSoup(html)
#soup.prettify()
#for i,divTag in enumerate(soup.find_all('div')):
#    try:
#        verbage.append(divTag.contents)
#        verbage2.append({'ha_url':url, 'about_us':verbage, 'id':i})
#    except KeyError:
#        pass
#scraperwiki.sqlite.save(unique_keys=["about_us"], data={"ha_url": url,"about_us": verbage}, table_name='verbage1')
#scraperwiki.sqlite.save(unique_keys=['ha_url','id'], data=verbage2, table_name='verbage2')
