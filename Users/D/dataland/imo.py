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
    return 'http://www.shiplist.net/ships?alpha={token}&Vessel_page={pagenum}'.format(token=token,pagenum=pagenum)

# This is for the detail page
def urlforimo(imo):
    return 'http://www.shiplist.net/ship/imo/{imo}'.format(imo=imo)

# Step 1: Build list of total page counts for each letter/number partition of data
# A:Z and 0:9
def urlformain(pagenum):
    return "http://www.shiplist.net/ships/{pagenum}".format(pagenum=pagenum)

# Build array of capital letters (A:Z)
let_list = map(chr, range(65, 91))
# Build array of number (0:9)
num_list = map(int, range(0,10))
# Fuse arrays
for i in num_list:
    let_list.append(num_list[i])

#Loop through 1st page for letter in array, get page count at the bottom of the page
for i in let_list:
    url = urlformain(i)
    text = urllib2.urlopen(url).read()
    soup = BeautifulSoup(text)
    # Get row that contains the count of records for letter
    data = soup.findAll('div',attrs={'class':'summary'})
    for n in data:
        o = str(n)
        start = (o.index("of")+3)
        finish = (o.index("result(s)")-1)
        # Get just the count 
        rec_count = o[start:finish]
        # 10 records per page, so modulus the value to see if you need more pages
        if (int(rec_count)%10)>0:
            pages = (int(rec_count)/10)+1
        else:
            pages = (int(rec_count)/10)
        for p in range(1,pages+1):
            # Build urls for all the pages in site for a particular token
            pageid = urlfortoken(i,p)
            html = scraperwiki.scrape(pageid)
            root = lxml.html.fromstring(html)
            # Get all the data off each row
            for count, tr in enumerate(root.cssselect('tr')):
                row = [unicode(td.text_content()).encode('utf-8') for td in tr.cssselect('td')]
                if len(row)>0:
                    imo = row[0]
                    vessel_type = row[2]
                    gross_tonnage = row[3]
                    year_built = row[4]
                    final_page = urlforimo(row[0])
                    text = urllib2.urlopen(final_page).read()
                    soup = BeautifulSoup(text)                    
                    # Get General Information Table values
                    data = soup.findAll('div',attrs={'class':'span5'})
                    # Get Vessel Name
                    o = str(data[1])
                    start = (o.index(">")+1)
                    finish = (o.index("/")-2)
                    vessel_name = o[start:finish]
                    # Get Flag
                    o = str(data[2])
                    start =  (o.index("title=")+7)
                    finish = (o.index("src")-2)
                    flag = o[start:finish].replace('&amp;','and')   
                    # Get Callsign
                    o = str(data[3])
                    start =  (o.index(">")+1)
                    finish = (o.index("/")-1)
                    callsign = o[start:finish]
                    # Get Port of Registry
                    o = str(data[5])
                    start =  (o.index(">")+1)
                    finish = (o.index("/")-1)
                    port_registry = o[start:finish]
                    # Get Builder
                    o = str(data[6])
                    start =  (o.index(">")+1)
                    finish = (o.index("/")-1)
                    builder = o[start:finish]
                    # Get Service Speed
                    o = str(data[7])
                    start =  (o.index(">")+1)
                    finish = (o.index("/")-1)
                    service_speed = o[start:finish] 
                    # Save the Record
                    now = datetime.datetime.now()
                    data = {"tmsp_scraped":str(now),"imo":imo,"vessel_type":vessel_type,"gross_tonnage":gross_tonnage,"year_built":year_built,
                            "vessel_name":vessel_name,"flag":flag,"callsign":callsign,"Port of Registry":port_registry,"builder":builder,
                            "service_speed":service_speed}
                    scraperwiki.sqlite.save(unique_keys=["imo"], data=data, table_name="s_vessel")
                    print "Finished: " + imo + ", " + vessel_name
