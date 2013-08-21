import scraperwiki
import urllib2 

url1 = 'http://example.org/url%20example'
url2 = 'http://example.org/url example'
record = {}
record['URI'] = url1
record['URL2'] = url2
scraperwiki.sqlite.save(['URI'], data=record)




response = urllib2.urlopen('http://193.178.1.87/ePlan41/SearchListing.aspx')
html = response.read()

print(html)