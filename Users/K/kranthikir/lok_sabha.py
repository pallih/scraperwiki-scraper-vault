import scraperwiki

# Blank Python

import urllib
from lxml import etree
import StringIO
 
url = "http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx"
result = urllib.urlopen(url)
html = result.read()
 
parser = etree.HTMLParser()
tree   = etree.parse(StringIO.StringIO(html), parser)
 
xpath = "//table[@id='ctl00_ContPlaceHolderMain_Alphabaticallist1_dg1']/tr[position()>1]/td[position()=2]/a/child::text()"
filtered_html = tree.xpath(xpath)
 
print filtered_htmlimport scraperwiki

# Blank Python

import urllib
from lxml import etree
import StringIO
 
url = "http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx"
result = urllib.urlopen(url)
html = result.read()
 
parser = etree.HTMLParser()
tree   = etree.parse(StringIO.StringIO(html), parser)
 
xpath = "//table[@id='ctl00_ContPlaceHolderMain_Alphabaticallist1_dg1']/tr[position()>1]/td[position()=2]/a/child::text()"
filtered_html = tree.xpath(xpath)
 
print filtered_html