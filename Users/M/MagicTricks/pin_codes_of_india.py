import scraperwiki

# Blank Python

import re
import mechanize
from bs4 import BeautifulSoup
import csv
import time

br = mechanize.Browser()
data={}
for i in xrange(1050,1504):
    br.open("http://www.pincodedatabase.com/pin-code/index/%s" % i)
    html = br.response().read()
    soup = BeautifulSoup(html)
    table = soup.find_all(id="datatable")
    allrows = soup.find_all("tr")
    j = 1
    for row in allrows:
        cols = row.find_all("div")
        if cols:
            data['srno'] = "'"+str(i)+"."+str(j)
            data['area'] = cols[0].text 
            data['Pin']  = cols[1].text 
            data['City'] = cols[2].text
            scraperwiki.sqlite.save(unique_keys=['srno'], data=data)
            j=j+1
    time.sleep(0.2)        

