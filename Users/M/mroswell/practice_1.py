####!usr/bin/python

import urllib2
#from lxml import etree, fromstring, tostring
#from lxml.cssselect import CSSSelector
from lxml.html import etree, fromstring, tostring
import requests
#import StringIO
#from scraperwiki.sqlite import save
#import datetime

result = urllib2.urlopen("http://mgaleg.maryland.gov/webmga/frmmain.aspx?pid=legisrpage&tab=subject6")
html = result.read()

doc = fromstring(html)
#senators = doc.cssselect('#ContentPlaceHolder1_div_01 :nth-child(3) .grid td:nth-child(1)')
senators = doc.cssselect ('#ContentPlaceHolder1_div_01 td:nth-child(1) a')

print senators

#for senator in senators:
#    print senator.text_content():

for senator in senators:
    print senator.text

#parser = etree.HTMLParser()
#tree   = etree.parse(StringIO.StringIO(html), parser)


#xpath = "//table[@class='grid']/tbody[position()>1]/td[position()=2]/a/child::text()"
#filtered_html = tree.xpath(xpath)

#filter_html = 
#print filtered_html