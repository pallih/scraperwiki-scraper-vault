import scraperwiki

import re
import urllib2

url = "http://www.indiaplaza.com/laptops-pc-1.htm"
open = urllib2.urlopen(url)
page = str(open.readlines())

urlcount = 1
matches = re.findall(r'(ContentPlaceHolder1_SpecificValuesHolder_ctl00_dlBrowseView_HyperLink2_.{5,100}href=")(/[\w\d-]+.htm)(">)',page)
for match in matches:
 pagelink = 'http://www.indiaplaza.com'+match[1]
 urlcount = urlcount + 1
 scraperwiki.sqlite.save(['url'],data={'url':pagelink})
print urlcount
import scraperwiki

import re
import urllib2

url = "http://www.indiaplaza.com/laptops-pc-1.htm"
open = urllib2.urlopen(url)
page = str(open.readlines())

urlcount = 1
matches = re.findall(r'(ContentPlaceHolder1_SpecificValuesHolder_ctl00_dlBrowseView_HyperLink2_.{5,100}href=")(/[\w\d-]+.htm)(">)',page)
for match in matches:
 pagelink = 'http://www.indiaplaza.com'+match[1]
 urlcount = urlcount + 1
 scraperwiki.sqlite.save(['url'],data={'url':pagelink})
print urlcount
