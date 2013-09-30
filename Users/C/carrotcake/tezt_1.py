import scraperwiki  
import lxml.html 
import simplejson
import urllib2
import re
import time
import BeautifulSoup

# Blank Python
#html_page = urllib2.urlopen("http://www.reddit.com/r/all/")
#soup = BeautifulSoup.BeautifulSoup(html_page)
#a_string = soup.find(text="next")
#print (a_string)
#for link in soup.findAll('href'):
#   print link.get('href')
    #x = link.get('href')
    #y = re.search('.*after=.*', x)
    #z = 'None'
    #if y != z:
        #print (x)
#print 'done'

url = 'http://www.reddit.com/r/all/'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):
    if el.attrib['href'].find(".com") > 0:
                data = {
                    'url' : el.attrib['href']
                }

import scraperwiki  
import lxml.html 
import simplejson
import urllib2
import re
import time
import BeautifulSoup

# Blank Python
#html_page = urllib2.urlopen("http://www.reddit.com/r/all/")
#soup = BeautifulSoup.BeautifulSoup(html_page)
#a_string = soup.find(text="next")
#print (a_string)
#for link in soup.findAll('href'):
#   print link.get('href')
    #x = link.get('href')
    #y = re.search('.*after=.*', x)
    #z = 'None'
    #if y != z:
        #print (x)
#print 'done'

url = 'http://www.reddit.com/r/all/'
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for el in root.cssselect("a"):
    if el.attrib['href'].find(".com") > 0:
                data = {
                    'url' : el.attrib['href']
                }

