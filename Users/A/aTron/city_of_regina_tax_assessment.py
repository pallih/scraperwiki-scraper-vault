import scraperwiki
import urllib2

# Blank Python

url = 'http://tax.regina.ca/summary.jsp?account=10037196'
page = urllib2.urlopen(url)
print page