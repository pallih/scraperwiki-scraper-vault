# ScraperWiki library pdftoxml scrapes PDFs

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://resources.motogp.com/files/results/2012/NED/MotoGP/RAC/worldstanding.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s.prettify()

name = None
all = []
data = {}
state = None
l = []

#for page in s.findAll('text'):
#    if t.text != " ": 
#        print t
#        print t.text
    
#this bit saves the data in the scraperwiki datastore
#for a in t.text:
 #    record = { "a" : t.text } # column name and value
 #    scraperwiki.datastore.save(["a"], record) # save the records one by one
# ScraperWiki library pdftoxml scrapes PDFs

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://resources.motogp.com/files/results/2012/NED/MotoGP/RAC/worldstanding.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s.prettify()

name = None
all = []
data = {}
state = None
l = []

#for page in s.findAll('text'):
#    if t.text != " ": 
#        print t
#        print t.text
    
#this bit saves the data in the scraperwiki datastore
#for a in t.text:
 #    record = { "a" : t.text } # column name and value
 #    scraperwiki.datastore.save(["a"], record) # save the records one by one
# ScraperWiki library pdftoxml scrapes PDFs

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://resources.motogp.com/files/results/2012/NED/MotoGP/RAC/worldstanding.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s.prettify()

name = None
all = []
data = {}
state = None
l = []

#for page in s.findAll('text'):
#    if t.text != " ": 
#        print t
#        print t.text
    
#this bit saves the data in the scraperwiki datastore
#for a in t.text:
 #    record = { "a" : t.text } # column name and value
 #    scraperwiki.datastore.save(["a"], record) # save the records one by one
# ScraperWiki library pdftoxml scrapes PDFs

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://resources.motogp.com/files/results/2012/NED/MotoGP/RAC/worldstanding.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s.prettify()

name = None
all = []
data = {}
state = None
l = []

#for page in s.findAll('text'):
#    if t.text != " ": 
#        print t
#        print t.text
    
#this bit saves the data in the scraperwiki datastore
#for a in t.text:
 #    record = { "a" : t.text } # column name and value
 #    scraperwiki.datastore.save(["a"], record) # save the records one by one
# ScraperWiki library pdftoxml scrapes PDFs

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://resources.motogp.com/files/results/2012/NED/MotoGP/RAC/worldstanding.pdf"
a = scraperwiki.scrape(pdfurl)
s = BeautifulSoup(scraperwiki.pdftoxml(a))
print s.prettify()

name = None
all = []
data = {}
state = None
l = []

#for page in s.findAll('text'):
#    if t.text != " ": 
#        print t
#        print t.text
    
#this bit saves the data in the scraperwiki datastore
#for a in t.text:
 #    record = { "a" : t.text } # column name and value
 #    scraperwiki.datastore.save(["a"], record) # save the records one by one
