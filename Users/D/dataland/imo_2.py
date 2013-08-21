import scraperwiki
import lxml.html
import urllib2
import datetime
import json
import string
import random
from BeautifulSoup import BeautifulSoup
import random

# Token can be a capital letter or a number 0-9
def urlfortoken(token,pagenum):
    return 'http://www.imonumber.com/ships/{token}?Vessel_page={pagenum}'.format(token=token,pagenum=pagenum)

# Build array of capital letters (A:Z)
let_list = map(chr, range(65, 91))

# Add to array
let_list.append("9")

# Step 1: Build list of total page counts for each letter/number partition of data,
# and build the detail urls based on a loop that counts to that limit
def urlformain(pagenum):
    return "http://www.imonumber.com/ships/{pagenum}".format(pagenum=pagenum)

try:
    curr_index = scraperwiki.sqlite.get_var("index_next_run",0)
except NameError:
    curr_index = 0

url = urlformain(let_list[curr_index])
text = urllib2.urlopen(url).read()
soup = BeautifulSoup(text)
# Get row that contains the count of records for letter
data = soup.findAll('li',attrs={'class':'last'})
o = str(data)
letterpos = (o.index("?")-1)
letter = o[34]
pagestart = (o.index("_page=")+6)
pagefinish = (o.index(">Last")-1)
last = int(o[pagestart:pagefinish])
for p in range(1,last+1):
    pageid = urlfortoken(letter,p)
    text2 = urllib2.urlopen(pageid).read()
    soup2 = BeautifulSoup(text2)
    data2 = soup2.findAll('a',attrs={'class':'imo-block'})
    for n in data2:      
        raw = str(n)
        linkstart = (raw.index("href=")+6)
        linkfinish = (raw.index("<img")-3)
        link = raw[linkstart:linkfinish]
        now = datetime.datetime.now()
        data3 = {"tmsp_scraped":str(now), "detail_page":link, "list_page":pageid, "index":let_list[curr_index]}
        scraperwiki.sqlite.save(unique_keys=["detail_page"], data=data3, table_name = "smtb_links")
    print "Finished Index "+letter+ " Page "+str(p)

if curr_index < 36:
    next_index = curr_index + 1
else:
    next_index = 0
scraperwiki.sqlite.save_var("index_next_run",next_index)
print ""
print "Index value for next run will be "+str(let_list[next_index])
