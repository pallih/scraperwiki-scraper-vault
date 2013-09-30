import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time
start = time.time()
# Find Bloomberg Brent Price
rawBloomData = urllib2.urlopen("http://www.bloomberg.com/energy/").read()
BloomSoup = BeautifulSoup(rawBloomData)
brent = BloomSoup.findAll('tr')[14]
BloomPrice = float(re.search(re.compile (r"\d+\.\d*"),str(brent.contents)).group())
# Compile for display
print " "
print " Brent Crude ($/Brl)"
print " Bloomberg : %.2f" %(BloomPrice)
print " "
# Write to files
OutputPath = "C:\\Test\\"
open(OutputPath+"Bloomberg.txt","wb").write("%.2f" %(BloomPrice))
print "\n"
import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time
start = time.time()
# Find Bloomberg Brent Price
rawBloomData = urllib2.urlopen("http://www.bloomberg.com/energy/").read()
BloomSoup = BeautifulSoup(rawBloomData)
brent = BloomSoup.findAll('tr')[14]
BloomPrice = float(re.search(re.compile (r"\d+\.\d*"),str(brent.contents)).group())
# Compile for display
print " "
print " Brent Crude ($/Brl)"
print " Bloomberg : %.2f" %(BloomPrice)
print " "
# Write to files
OutputPath = "C:\\Test\\"
open(OutputPath+"Bloomberg.txt","wb").write("%.2f" %(BloomPrice))
print "\n"
