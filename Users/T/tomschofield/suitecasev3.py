import scraperwiki

# Blank Python

#!/usr/bin/env python
import pprint 
import json
import socket
import csv  
from bs4 import BeautifulSoup
import urllib2
data = scraperwiki.scrape("http://fieldventures.org/IT.txt")
         
f = csv.reader(data.splitlines())
#f = open('http://fieldventures.org/IT_ipranges.txt', 'r')

pp = pprint.PrettyPrinter()

try:
    domain = socket.gethostbyaddr("2.16.71.255")
    print domain[0]

except:    
    print "balls" 
        
def loopOverRange( startAddress , endAddress ):
    "iterates over a given ip range"
    starts = startAddress.split(".")
    ends = endAddress.split(".")

    start1 = int(starts[0])
    start2 = int(starts[1])
    start3 = int(starts[2])
    start4 = int(starts[3])

    end1 = int(ends[0])
    end2 = int(ends[1])
    end3 = int(ends[2])
    end4 = int(ends[3])

    inc = 0
    diff=end1-start1
    
    for i in range(start1, end1+1):
        for j in range(start2, end2+1):
            for k in range(start3, end3+1):
                for l in range(start4, end4+1):
                    address = str(i)+"."+str(j)+"."+str(k)+"."+str(l)
                    val=0
                    try:
                        domain = socket.gethostbyaddr(address)
                        
                        #OK SO NOW WE ARE AT THE PAGE LETS TEST IT

                        #print domain[0]
                        #scraperwiki.sqlite.save(unique_keys=["a"], data={"a":inc, "b":domain[0], "c":address})
                        url = "http://"+domain[0]
                        #html = scraperwiki.scrape(url)
                        #root = lxml.html.fromstring(html)
                        #for el in lxml.html.iterlinks(html):
                        #    print el
                        print url
                        page = urllib2.urlopen(url)
                        soup = BeautifulSoup(page)
                        pp.pprint(soup.get_text())
                        #for link in soup.find_all('a'):
                         #   print(link.get('href'))
                        inc += 1
                    except:
                        #print address
                        val + 1
    return
  
for row in f:
        #print line
        addresses = row[0].split("-")
        #trim whitespace
        firstAddress=addresses[0].strip()
        secondAddress=addresses[1].strip()
        loopOverRange(firstAddress, secondAddress)
        #print secondAddress
        
#loopOverRange(  "2.16.70.0" , "2.16.71.255" )
