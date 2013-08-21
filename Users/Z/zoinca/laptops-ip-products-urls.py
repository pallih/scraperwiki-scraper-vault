import scraperwiki

# Blank Python
import urllib2
import re

scraperwiki.sqlite.attach('laptops-ib-pages-results','urls')
list_urls = scraperwiki.sqlite.select('* from urls.swdata')

for dict_url in list_urls:
 url = dict_url['url']
 print url
 
 open = urllib2.urlopen(url)
 page = str(open.readlines())
 
 urlcount = 1
 matches = re.findall(r'(ContentPlaceHolder1_SpecificValuesHolder_ctl00_dlBrowseView_HyperLink2_.{5,100}href=")(/[\w\d-]+.htm)(">)',page)
 for match in matches:
  pagelink = 'http://www.indiaplaza.com'+match[1]
  urlcount = urlcount + 1
  scraperwiki.sqlite.save(['url'],data={'url':pagelink})
 print urlcount

print urlcount

#<a id="ContentPlaceHolder1_SpecificValuesHolder_ctl00_dlBrowseView_HyperLink2_1" title="HP Pavilion G4 - 1200TX" href="/hp-pavilion-g4-1200tx-pc-pcs31122011hp15-10.htm">HP Pavilion G4 - 1200TX</a>
