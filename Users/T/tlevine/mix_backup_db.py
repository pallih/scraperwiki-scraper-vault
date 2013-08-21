'''
Making a file from scraperwiki is way too hard...
'''
from lxml.html import fromstring
from time import time
from urllib2 import urlopen

html = fromstring(urlopen('https://views.scraperwiki.com/run/mix_scraper_spreadsheets/?date='+str(time())).read())
slugs = set([href.split('/')[-2] for href in html.xpath('//td[position()=1]/a/@href')])

print slugs