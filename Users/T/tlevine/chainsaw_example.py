#Load Chainsaw
from scraperwiki.utils import swimport
chainsaw=swimport('chainsaw')

#Load other stuff
from urllib2 import urlopen
from lxml.html import fromstring
xml=fromstring(urlopen('http://scraperwiki.com').read())

def example_htmltable2matrix():
  table=xml.xpath('//table')[0]
  print chainsaw.htmltable2matrix(table)

def main():
  example_htmltable2matrix()

main()