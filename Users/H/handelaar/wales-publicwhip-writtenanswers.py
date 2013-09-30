import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.assemblywales.org/bus-home/bus-chamber/bus-chamber-third-assembly-written/waq20101105-e.pdf"

a = scraperwiki.scrape(pdfurl)
d = scraperwiki.pdftoxml(a)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

#print d

for page in s.findAll('page'):
    if int(page['number']) > 1:
        print page['number']

#name = None
#all = []
#data = {}
#state = None
#l = []

#for t in s.findAll('text'):
#    if t.text != " ":
#        print t
#        print t.tex#=t
import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re
import json
from BeautifulSoup import BeautifulSoup

pdfurl = "http://www.assemblywales.org/bus-home/bus-chamber/bus-chamber-third-assembly-written/waq20101105-e.pdf"

a = scraperwiki.scrape(pdfurl)
d = scraperwiki.pdftoxml(a)
s = BeautifulSoup(scraperwiki.pdftoxml(a))

#print d

for page in s.findAll('page'):
    if int(page['number']) > 1:
        print page['number']

#name = None
#all = []
#data = {}
#state = None
#l = []

#for t in s.findAll('text'):
#    if t.text != " ":
#        print t
#        print t.tex#=t
