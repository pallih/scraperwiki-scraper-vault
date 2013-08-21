import scraperwiki
from BeautifulSoup import BeautifulSoup,NavigableString
import urllib2,sys

address = "http://www.bbc.co.uk/news/world/"

html = urllib2.urlopen(address).read()

soup = BeautifulSoup(html)

def printText(tags):
        for tag in tags:
                if tag.__class__ == NavigableString:
                        print tag,
                else:
                        printText(tag)
        print ""

printText(soup.findAll("p"))