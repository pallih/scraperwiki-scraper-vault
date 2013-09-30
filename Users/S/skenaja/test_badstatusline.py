import scraperwiki
import urllib2
from time import clock, time

url = "https://delecorp.delaware.gov/tin/GINameSearch.jsp" + str(time())
#r = requests.get(url)
#print r.status_code

request = urllib2.Request(url)
response = urllib2.urlopen(request)
print str(response.code)

import scraperwiki
import urllib2
from time import clock, time

url = "https://delecorp.delaware.gov/tin/GINameSearch.jsp" + str(time())
#r = requests.get(url)
#print r.status_code

request = urllib2.Request(url)
response = urllib2.urlopen(request)
print str(response.code)

