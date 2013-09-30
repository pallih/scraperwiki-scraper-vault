#!/usr/bin/env python

import scraperwiki
import requests
from StringIO import StringIO
from bs4 import BeautifulSoup
import re

p=1311
while p <= 1313:
    html = requests.get("http://www.acecqa.gov.au/NQAITS/SearchServices.aspx?vm=1&keywords=se&pn=%s&ps=10"%(p))
    g = StringIO(html.content)
    soup = BeautifulSoup(g)
    names = soup.find_all("h3")
    geos = soup.find(text=re.compile("LatLng"))
    lc = 0
    firstendll = 0
    while lc < 10:
        firstll = geos.string.find("-",firstendll)
        if firstll == None:
            break
        #print firstll
        firstendll = geos.string.find(",",firstll)
        #print firstendll
        #firstendlon = geos.string.find(")",firstendll)
        #print firstendlon
        try:
            int(geos.string[firstll:firstendll][1])
            each = soup.find(id="cphMain_ctlList_rptServices_pnlApprovedPlaces_%s"%(lc))
            print names[lc].string.strip(),each.contents[3].string.strip(),geos.string[firstll:firstll+9],geos.string[firstendll+1:firstendll+10]
            unique_keys = [ 'name','lat','lon' ]
            data = { 'name':names[lc].string.strip(), 'places':each.contents[3].string.strip(), 'lat':geos.string[firstll:firstll+9], 'lon':geos.string[firstendll+1:firstendll+10] }
            scraperwiki.sqlite.save(unique_keys, data)
            lc+=1
            
        except Exception, e:
            print e
            pass
            
        firstendll=firstendll+10

    scraperwiki.sqlite.save_var('lastpage', "http://www.acecqa.gov.au/NQAITS/SearchServices.aspx?vm=1&keywords=se&pn=%s&ps=100"%(p))
    p+=1
    

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
#!/usr/bin/env python

import scraperwiki
import requests
from StringIO import StringIO
from bs4 import BeautifulSoup
import re

p=1311
while p <= 1313:
    html = requests.get("http://www.acecqa.gov.au/NQAITS/SearchServices.aspx?vm=1&keywords=se&pn=%s&ps=10"%(p))
    g = StringIO(html.content)
    soup = BeautifulSoup(g)
    names = soup.find_all("h3")
    geos = soup.find(text=re.compile("LatLng"))
    lc = 0
    firstendll = 0
    while lc < 10:
        firstll = geos.string.find("-",firstendll)
        if firstll == None:
            break
        #print firstll
        firstendll = geos.string.find(",",firstll)
        #print firstendll
        #firstendlon = geos.string.find(")",firstendll)
        #print firstendlon
        try:
            int(geos.string[firstll:firstendll][1])
            each = soup.find(id="cphMain_ctlList_rptServices_pnlApprovedPlaces_%s"%(lc))
            print names[lc].string.strip(),each.contents[3].string.strip(),geos.string[firstll:firstll+9],geos.string[firstendll+1:firstendll+10]
            unique_keys = [ 'name','lat','lon' ]
            data = { 'name':names[lc].string.strip(), 'places':each.contents[3].string.strip(), 'lat':geos.string[firstll:firstll+9], 'lon':geos.string[firstendll+1:firstendll+10] }
            scraperwiki.sqlite.save(unique_keys, data)
            lc+=1
            
        except Exception, e:
            print e
            pass
            
        firstendll=firstendll+10

    scraperwiki.sqlite.save_var('lastpage', "http://www.acecqa.gov.au/NQAITS/SearchServices.aspx?vm=1&keywords=se&pn=%s&ps=100"%(p))
    p+=1
    

# Saving data:
# unique_keys = [ 'id' ]
# data = { 'id':12, 'name':'violet', 'age':7 }
# scraperwiki.sql.save(unique_keys, data)
