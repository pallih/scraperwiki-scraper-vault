import scraperwiki

# testing
# Blank Python
import scraperwiki
import lxml.html

import urllib
from lxml import etree
import StringIO

#result = urllib.urlopen("http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx")
result = urllib.urlopen("http://http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita")

html = result.read()

parser = etree.HTMLParser()
tree   = etree.parse(StringIO.StringIO(html), parser)

#xpath = #"//table[@id='ctl00_ContPlaceHolderMain_Alphabaticallist1_dg1']/tr[position()>1]/td[position()=2]/a/child::text()"
#filtered_html = tree.xpath(xpath)

xpath = "//*[@id="mw-content-text"]/table[3]/tbody/tr[1]/td[2]/a/child::text()"
filtered_html = tree.xpath(xpath)

print filtered_html


#tree = lxml.html.parse("http://http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita")

#for a in tree.xpath('//td'):
#    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href'] })


#url = "http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx"


#root = lxml.html.parse(url).getroot()
#print lxml.html.tostring(root)

import scraperwiki

# testing
# Blank Python
import scraperwiki
import lxml.html

import urllib
from lxml import etree
import StringIO

#result = urllib.urlopen("http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx")
result = urllib.urlopen("http://http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita")

html = result.read()

parser = etree.HTMLParser()
tree   = etree.parse(StringIO.StringIO(html), parser)

#xpath = #"//table[@id='ctl00_ContPlaceHolderMain_Alphabaticallist1_dg1']/tr[position()>1]/td[position()=2]/a/child::text()"
#filtered_html = tree.xpath(xpath)

xpath = "//*[@id="mw-content-text"]/table[3]/tbody/tr[1]/td[2]/a/child::text()"
filtered_html = tree.xpath(xpath)

print filtered_html


#tree = lxml.html.parse("http://http://en.wikipedia.org/wiki/List_of_Chinese_municipalities_and_prefecture-level_divisions_by_GDP_per_capita")

#for a in tree.xpath('//td'):
#    scraperwiki.sqlite.save(['url'], {'name': a.text, 'url': 'http://en.wikipedia.org%s' % a.attrib['href'] })


#url = "http://164.100.47.132/LssNew/Members/Alphabaticallist.aspx"


#root = lxml.html.parse(url).getroot()
#print lxml.html.tostring(root)

