#import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time
start = time.time()
# Find EPEX Price
rawEPEXData= urllib2.urlopen("http://www.epexspot.com/en/market-data/intraday/intraday-table/2013-02-13/FR/").read()
EpexSoup = BeautifulSoup(rawEPEXData)
epex = EpexSoup.findAll('tr')[20]
tempx=epex.contents
temp1 = epex.findAll(
print (tempx)
epexPrice = float(re.search(re.compile (r"\d+\.\d*"),str(epex.contents)).group(0))
print str(epex.contents)
# Compile for display
print " EPEX ($/MWh)"
print " EPEX : %.2f" %(epexPrice)
# Write to files
OutputPath = "C:\\Test\\"
open(OutputPath+"EPEX.txt","wb").write("%.2f" %(epexPrice))
print "\n"#import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time
start = time.time()
# Find EPEX Price
rawEPEXData= urllib2.urlopen("http://www.epexspot.com/en/market-data/intraday/intraday-table/2013-02-13/FR/").read()
EpexSoup = BeautifulSoup(rawEPEXData)
epex = EpexSoup.findAll('tr')[20]
tempx=epex.contents
temp1 = epex.findAll(
print (tempx)
epexPrice = float(re.search(re.compile (r"\d+\.\d*"),str(epex.contents)).group(0))
print str(epex.contents)
# Compile for display
print " EPEX ($/MWh)"
print " EPEX : %.2f" %(epexPrice)
# Write to files
OutputPath = "C:\\Test\\"
open(OutputPath+"EPEX.txt","wb").write("%.2f" %(epexPrice))
print "\n"