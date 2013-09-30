import scraperwiki
import lxml.html
import urllib
import datetime
import random

# Multi-Value Replace in string
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# Passes street_name into URL returning RPC Numbers (folio numbers)
# Cannot use street types because the value 'ST' overflows website limit
def urlforstreetname(street_name):
    return "http://arlingtonva.us/Departments/RealEstate/reassessments/scripts/SearchResults.asp?ParcelID=&StrtNum=&StrtName={street_name}&StrtType=&StrtDir=&UnitNum=&Tradename=&EconUnit=".format(street_name=street_name)

# Dictionary of replacements for two/three word street_names
reps = {
'ARLINGTON MILL':'ARLINGTON+MILL', 
'ARLINGTON RIDGE':'ARLINGTON+RIDGE',
'ARMY NAVY':'ARMY+NAVY',
'BOUNDARY CHANNEL':'BOUNDARY+CHANNEL', # Boundary Channel only has one record, goes straight to detail page
'CARLIN SPRINGS':'CARLIN+SPRINGS',
'CHAIN BRIDGE':'CHAIN+BRIDGE',
'FORT MYER':'FORT+MYER',
'FORT SCOTT':'FORT+SCOTT',
'FOUR MILE RUN':'FOUR+MILE+RUN',
'GEORGE MASON':'GEORGE+MASON',
'GEORGE WASHINGTON':'GEORGE+WASHINGTON',
'JEFFERSON DAVIS':'JEFFERSON+DAVIS',
'NELLY CUSTIS':'NELLY+CUSTIS',
'JOHN MARSHALL':'JOHN+MARSHALL',
'OLD DOMINION':'OLD+DOMINION',
'OLD GLEBE':'OLD+GLEBE',
'OLD JEFFERSON DAVIS':'OLD+JEFFERSON+DAVIS',
'PATRICK HENRY':'PATRICK+HENRY',
'ROBERT WALKER':'ROBERT+WALKER',
'ROCK SPRING':'ROCK+SPRING',
'ROUND HILL':'ROUND+HILL',
'VAN BUREN':'VAN+BUREN',
'WALTER REED':'WALTER+REED',
'LITTLE FALLS':'LITTLE+FALLS'}

# Main Property Record Search Page. Data we want isn't here, but list of values that will help us get it is.
html = scraperwiki.scrape("http://www.arlingtonva.us/departments/realestate/reassessments/scripts/dreadefault.asp")
root = lxml.html.fromstring(html)

# Need to pull the list of street values to use in subsequent scrape step for RPC Numbers
for count, tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if count == 3:
        rawdata = row[2]
        # Execute replacement of multi-word values & split by spaces once cleaned up
        multiwordfixed = replace_all(rawdata,reps).split()
        random.shuffle(multiwordfixed)
        print multiwordfixed
        for v in multiwordfixed:
            street_name = v
            print "Running for street name: {street_name}".format(street_name=street_name)
            url = urlforstreetname(street_name)
            # Extract link to detail record
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for count, tr in enumerate(root.cssselect('tr')):
                row = [td.text_content() for td in tr.cssselect('td')]
                if len(row)>=1:
                    if row[0] == "START NEW SEARCH":
                        break                    
                    else:                         
                        for ahref in tr.cssselect('a'):
                            detailink = ahref.attrib['href']
                            now2 = datetime.datetime.now()
                            data2={"tmsp_queried":str(now2), "street_name":street_name, "detail_link":detailink, "parcel_id":row[0], "address":row[2]}
                            scraperwiki.sqlite.save(unique_keys=["street_name", "detail_link", "address"], data=data2, table_name="s_detail_link")
            # Save street_name and record count iterated through just for good measure
            now = datetime.datetime.now()
            data={"tmsp_queried":str(now), "street_name":v, "record_count":count}
            scraperwiki.sqlite.save(unique_keys=["street_name"],data=data,table_name="smtb_street_name")
            # Print summary of records scraped for this street to console
            print "Street Name: {street_name} Record Count: {count}".format(street_name=street_name,count=count)
import scraperwiki
import lxml.html
import urllib
import datetime
import random

# Multi-Value Replace in string
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

# Passes street_name into URL returning RPC Numbers (folio numbers)
# Cannot use street types because the value 'ST' overflows website limit
def urlforstreetname(street_name):
    return "http://arlingtonva.us/Departments/RealEstate/reassessments/scripts/SearchResults.asp?ParcelID=&StrtNum=&StrtName={street_name}&StrtType=&StrtDir=&UnitNum=&Tradename=&EconUnit=".format(street_name=street_name)

# Dictionary of replacements for two/three word street_names
reps = {
'ARLINGTON MILL':'ARLINGTON+MILL', 
'ARLINGTON RIDGE':'ARLINGTON+RIDGE',
'ARMY NAVY':'ARMY+NAVY',
'BOUNDARY CHANNEL':'BOUNDARY+CHANNEL', # Boundary Channel only has one record, goes straight to detail page
'CARLIN SPRINGS':'CARLIN+SPRINGS',
'CHAIN BRIDGE':'CHAIN+BRIDGE',
'FORT MYER':'FORT+MYER',
'FORT SCOTT':'FORT+SCOTT',
'FOUR MILE RUN':'FOUR+MILE+RUN',
'GEORGE MASON':'GEORGE+MASON',
'GEORGE WASHINGTON':'GEORGE+WASHINGTON',
'JEFFERSON DAVIS':'JEFFERSON+DAVIS',
'NELLY CUSTIS':'NELLY+CUSTIS',
'JOHN MARSHALL':'JOHN+MARSHALL',
'OLD DOMINION':'OLD+DOMINION',
'OLD GLEBE':'OLD+GLEBE',
'OLD JEFFERSON DAVIS':'OLD+JEFFERSON+DAVIS',
'PATRICK HENRY':'PATRICK+HENRY',
'ROBERT WALKER':'ROBERT+WALKER',
'ROCK SPRING':'ROCK+SPRING',
'ROUND HILL':'ROUND+HILL',
'VAN BUREN':'VAN+BUREN',
'WALTER REED':'WALTER+REED',
'LITTLE FALLS':'LITTLE+FALLS'}

# Main Property Record Search Page. Data we want isn't here, but list of values that will help us get it is.
html = scraperwiki.scrape("http://www.arlingtonva.us/departments/realestate/reassessments/scripts/dreadefault.asp")
root = lxml.html.fromstring(html)

# Need to pull the list of street values to use in subsequent scrape step for RPC Numbers
for count, tr in enumerate(root.cssselect('tr')):
    row = [td.text_content() for td in tr.cssselect('td')]
    if count == 3:
        rawdata = row[2]
        # Execute replacement of multi-word values & split by spaces once cleaned up
        multiwordfixed = replace_all(rawdata,reps).split()
        random.shuffle(multiwordfixed)
        print multiwordfixed
        for v in multiwordfixed:
            street_name = v
            print "Running for street name: {street_name}".format(street_name=street_name)
            url = urlforstreetname(street_name)
            # Extract link to detail record
            html = scraperwiki.scrape(url)
            root = lxml.html.fromstring(html)
            for count, tr in enumerate(root.cssselect('tr')):
                row = [td.text_content() for td in tr.cssselect('td')]
                if len(row)>=1:
                    if row[0] == "START NEW SEARCH":
                        break                    
                    else:                         
                        for ahref in tr.cssselect('a'):
                            detailink = ahref.attrib['href']
                            now2 = datetime.datetime.now()
                            data2={"tmsp_queried":str(now2), "street_name":street_name, "detail_link":detailink, "parcel_id":row[0], "address":row[2]}
                            scraperwiki.sqlite.save(unique_keys=["street_name", "detail_link", "address"], data=data2, table_name="s_detail_link")
            # Save street_name and record count iterated through just for good measure
            now = datetime.datetime.now()
            data={"tmsp_queried":str(now), "street_name":v, "record_count":count}
            scraperwiki.sqlite.save(unique_keys=["street_name"],data=data,table_name="smtb_street_name")
            # Print summary of records scraped for this street to console
            print "Street Name: {street_name} Record Count: {count}".format(street_name=street_name,count=count)
