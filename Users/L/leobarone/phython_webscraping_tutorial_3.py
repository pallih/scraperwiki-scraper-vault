import urllib
import re


companieslist = ("aapl","spy","goog","nflx")

i=0

while i<len(companieslist):
    url = "http://finance.yahoo.com/q?s="+companieslist[i]+"&ql=1"
    htmlfile = urllib.urlopen(url)
    htmltext = htmlfile.read()
    regex = '<span id="yfs_l84_' + companieslist[i] + '">(.+?)</span>'
    pattern = re.compile(regex)
    price = re.findall(pattern,htmltext)
    print "the price of",companieslist[i],"is",price
    i+=1
print price
