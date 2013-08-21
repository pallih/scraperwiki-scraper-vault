#import scraperwiki
#import requests

import urllib2
from lxml.html import etree, fromstring, tostring

result = urllib2.urlopen("http://mgaleg.maryland.gov/webmga/frmmain.aspx?pid=legisrpage&tab=subject6")
html = result.read()
doc = fromstring(html)

senators = doc.cssselect ('#ContentPlaceHolder1_div_01 td:nth-child(1) a')
districts = doc.cssselect  ('#ContentPlaceHolder1_div_01 td:nth-child(2)')
rows = doc.cssselect  ('#ContentPlaceHolder1_div_01 tr:nth-child(3)')

#for row in rows:
#    print row[0].text

for senator in senators:
   print senator.text

#for district in districts:
#   print district.text

#for text in doc.cssselect('a'):
 #   print text
#import scraperwiki
#import requests

import urllib2
from lxml.html import etree, fromstring, tostring

result = urllib2.urlopen("http://mgaleg.maryland.gov/webmga/frmmain.aspx?pid=legisrpage&tab=subject6")
html = result.read()
doc = fromstring(html)

senators = doc.cssselect ('#ContentPlaceHolder1_div_01 td:nth-child(1) a')
districts = doc.cssselect  ('#ContentPlaceHolder1_div_01 td:nth-child(2)')
rows = doc.cssselect  ('#ContentPlaceHolder1_div_01 tr:nth-child(3)')

#for row in rows:
#    print row[0].text

for senator in senators:
   print senator.text

#for district in districts:
#   print district.text

#for text in doc.cssselect('a'):
 #   print text
