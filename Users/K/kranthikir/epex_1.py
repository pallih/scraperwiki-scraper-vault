import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time
start = time.time()
# Find EPEX Price
rawEPEXData= urllib2.urlopen("http://www.epexspot.com/en/market-data/intraday/").read()
EpexSoup = BeautifulSoup(rawEPEXData)
epex = EpexSoup .findAll('tr')[20]
epexPrice = float(re.search(re.compile (r"\d+\.\d*"),str(epex.contents)).group(0))
# Compile for display
print " "
print " EPEX ($/MWh)"
print " EPEX : %.2f" %(epexPrice)
print " "
# Write to files
OutputPath = "C:\\Test\\"
open(OutputPath+"EPEX.txt","wb").write("%.2f" %(epexPrice))
print "\n"import scraperwiki

# Blank Python

from BeautifulSoup import BeautifulSoup
import urllib2,re, time
start = time.time()
# Find EPEX Price
rawEPEXData= urllib2.urlopen("http://www.epexspot.com/en/market-data/intraday/").read()
EpexSoup = BeautifulSoup(rawEPEXData)
epex = EpexSoup .findAll('tr')[20]
epexPrice = float(re.search(re.compile (r"\d+\.\d*"),str(epex.contents)).group(0))
# Compile for display
print " "
print " EPEX ($/MWh)"
print " EPEX : %.2f" %(epexPrice)
print " "
# Write to files
OutputPath = "C:\\Test\\"
open(OutputPath+"EPEX.txt","wb").write("%.2f" %(epexPrice))
print "\n"