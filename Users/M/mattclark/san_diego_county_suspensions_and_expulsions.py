import scraperwiki
import time
import csv
import urllib2
import re
from BeautifulSoup import BeautifulSoup

url = "http://dq.cde.ca.gov/dataquest/Expulsion/ExpReports/CountyExp.aspx?cCounty=37,SAN,DIEGO&cYear=2010-11&cChoice=CoEpx1&Pageno=1"

# get page
try:
    page = scraperwiki.scrape(url)
except:
    time.sleep(4)
    page = scraperwiki.scrape(url)

# load page into Beautiful soup
soup = BeautifulSoup(page)

#get all the anchor tags that have district names inside of them
districts = soup.findAll('a')

#get all the td tags with the data
districtdata = soup.findAll('td', {'class' : 'smaller_right'})

#determine number of districts on page
numdistricts = len(districts)

#regular expression for capturing data within returned strings
matcher = re.compile(r'\w+,*.* *\w*%*')

#counter used to advance through the districtdata object
tdcounter = 0

#dictionary for storing data before saving it in database
output = {}

#for each district
for district in range(0,numdistricts):
    
    #first pull district name
    if matcher.search(districts[district].string):
        output['District_name'] = matcher.search(districts[district].string).group()
    #if no name, then save blankness
    else:
        output['District_name'] = ""
    
    if matcher.search(districtdata[tdcounter].string):
        output['CD_code'] = matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['CD_code'] = ""
        tdcounter += 1

    #skip school row
    tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Enrollment'] = matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Enrollment'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Number_tardy'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Number_tardy'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Truancy_rate'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Truancy_rate'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['VD_expulsions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['VD_expulsions'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['VD_suspensions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['VD_suspensions'] = ""
        tdcounter += 1   

    if matcher.search(districtdata[tdcounter].string):
        output['Dangerous_expulsions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Dangerous_expulsions'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Non-student_firearms'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Non-student_firearms'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Expulsions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Expulsions'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Suspensions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Suspensions'] = ""
        tdcounter += 1    

    #save everything to the datastore
    scraperwiki.sqlite.save(unique_keys=['CD_code'], data=output)







"""
#BEGINNING OF SCRAPER

# load parcels into list

data = scraperwiki.scrape("http://www.reportermattclark.com/SCRAPER/PNsWithNoLocation.csv")
parcels = csv.reader(data.splitlines())

# for each parcel in list

parcels.next()

for currentPN in list(parcels):

    # load url into a variable by slicing the parcel string
    url = "http://arcc.co.san-diego.ca.us/services/rollsearch/search.aspx?PB=" + currentPN[0][0:3] + "&PP=" + currentPN[0][3:6] + "&PN=" + currentPN[0][6:8] + "&PI=" + currentPN[0][8:10]

    # grab page
    #maybe do a try/except here or a loop
    try:
        page = scraperwiki.scrape(url)
    except:
        time.sleep(4)
        page = scraperwiki.scrape(url)

    # load the page into soup
    soup = BeautifulSoup(page)

    # load location into variable using soup
    location = soup.find('span', id="ctl00_ContentPlaceHolder1_lblLocation").string

    # put location into database
    if location is None:
        location = "No location listed"
    print  location + ", " + currentPN[0] + ", " + url
    scraperwiki.sqlite.save(unique_keys=["PN"], data={"PN":currentPN[0], "Address":location, "URL":url})

    # pause for 2 seconds
    time.sleep(4)

# done!

"""
import scraperwiki
import time
import csv
import urllib2
import re
from BeautifulSoup import BeautifulSoup

url = "http://dq.cde.ca.gov/dataquest/Expulsion/ExpReports/CountyExp.aspx?cCounty=37,SAN,DIEGO&cYear=2010-11&cChoice=CoEpx1&Pageno=1"

# get page
try:
    page = scraperwiki.scrape(url)
except:
    time.sleep(4)
    page = scraperwiki.scrape(url)

# load page into Beautiful soup
soup = BeautifulSoup(page)

#get all the anchor tags that have district names inside of them
districts = soup.findAll('a')

#get all the td tags with the data
districtdata = soup.findAll('td', {'class' : 'smaller_right'})

#determine number of districts on page
numdistricts = len(districts)

#regular expression for capturing data within returned strings
matcher = re.compile(r'\w+,*.* *\w*%*')

#counter used to advance through the districtdata object
tdcounter = 0

#dictionary for storing data before saving it in database
output = {}

#for each district
for district in range(0,numdistricts):
    
    #first pull district name
    if matcher.search(districts[district].string):
        output['District_name'] = matcher.search(districts[district].string).group()
    #if no name, then save blankness
    else:
        output['District_name'] = ""
    
    if matcher.search(districtdata[tdcounter].string):
        output['CD_code'] = matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['CD_code'] = ""
        tdcounter += 1

    #skip school row
    tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Enrollment'] = matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Enrollment'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Number_tardy'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Number_tardy'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Truancy_rate'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Truancy_rate'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['VD_expulsions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['VD_expulsions'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['VD_suspensions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['VD_suspensions'] = ""
        tdcounter += 1   

    if matcher.search(districtdata[tdcounter].string):
        output['Dangerous_expulsions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Dangerous_expulsions'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Non-student_firearms'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Non-student_firearms'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Expulsions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Expulsions'] = ""
        tdcounter += 1

    if matcher.search(districtdata[tdcounter].string):
        output['Suspensions'] =  matcher.search(districtdata[tdcounter].string).group()
        tdcounter += 1
    else:
        output['Suspensions'] = ""
        tdcounter += 1    

    #save everything to the datastore
    scraperwiki.sqlite.save(unique_keys=['CD_code'], data=output)







"""
#BEGINNING OF SCRAPER

# load parcels into list

data = scraperwiki.scrape("http://www.reportermattclark.com/SCRAPER/PNsWithNoLocation.csv")
parcels = csv.reader(data.splitlines())

# for each parcel in list

parcels.next()

for currentPN in list(parcels):

    # load url into a variable by slicing the parcel string
    url = "http://arcc.co.san-diego.ca.us/services/rollsearch/search.aspx?PB=" + currentPN[0][0:3] + "&PP=" + currentPN[0][3:6] + "&PN=" + currentPN[0][6:8] + "&PI=" + currentPN[0][8:10]

    # grab page
    #maybe do a try/except here or a loop
    try:
        page = scraperwiki.scrape(url)
    except:
        time.sleep(4)
        page = scraperwiki.scrape(url)

    # load the page into soup
    soup = BeautifulSoup(page)

    # load location into variable using soup
    location = soup.find('span', id="ctl00_ContentPlaceHolder1_lblLocation").string

    # put location into database
    if location is None:
        location = "No location listed"
    print  location + ", " + currentPN[0] + ", " + url
    scraperwiki.sqlite.save(unique_keys=["PN"], data={"PN":currentPN[0], "Address":location, "URL":url})

    # pause for 2 seconds
    time.sleep(4)

# done!

"""
