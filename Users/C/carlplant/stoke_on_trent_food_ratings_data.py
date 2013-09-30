import scraperwiki
from BeautifulSoup import BeautifulStoneSoup
import urllib2

starting_url = 'http://ratings.food.gov.uk/OpenDataFiles/FHRS880en-GB.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)
#print soup

items = soup.findAll('establishmentdetail') 
#print items
for item in items:
    record = {}
    for bus_name in item.findAll("businessname"):
        #titles.append(bus_name.text)
        name = item.businessname.text
        #print name
    for bus_type in item.findAll("businesstype"):
        #titles.append(bus_type.text)
        business_type = item.businesstype.text
        #print business_type
    for rating in item.findAll("ratingvalue"):
        #titles.append(rating.text)
        rating_value = item.ratingvalue.text
    for ratingDate in item.findAll("ratingdate"):
        #titles.append(ratingDate.text)
        ratingdate = item.ratingdate.text
    for Add2 in item.findAll("addressline2"):
        address2 = item.addressline2.text
    for Add3 in item.findAll("addressline3"):
        address3 = item.addressline3.text
    for Add4 in item.findAll("addressline4"):
        address4 = item.addressline4.text
    for postCode in item.findAll("postcode"):
        postcode = item.postcode.text
    for lng in item.findAll("longitude"):
        #titles.append(lng.text)
        longitude = item.longitude.text
    for lat in item.findAll("latitude"):
       
        latitude = item.latitude.text
        #print latitude
        scraperwiki.sqlite.save(unique_keys=[], data={'BusinessName':name,'BusinessType':business_type,'Rating':rating_value,'RatingDate':ratingdate,'Address2':address2,'Address3':address3,'address4':address4,'Postcode':postcode,'lat':latitude,'lng':longitude}) 

import scraperwiki
from BeautifulSoup import BeautifulStoneSoup
import urllib2

starting_url = 'http://ratings.food.gov.uk/OpenDataFiles/FHRS880en-GB.xml'
xml = scraperwiki.scrape(starting_url)
soup = BeautifulStoneSoup(xml)
#print soup

items = soup.findAll('establishmentdetail') 
#print items
for item in items:
    record = {}
    for bus_name in item.findAll("businessname"):
        #titles.append(bus_name.text)
        name = item.businessname.text
        #print name
    for bus_type in item.findAll("businesstype"):
        #titles.append(bus_type.text)
        business_type = item.businesstype.text
        #print business_type
    for rating in item.findAll("ratingvalue"):
        #titles.append(rating.text)
        rating_value = item.ratingvalue.text
    for ratingDate in item.findAll("ratingdate"):
        #titles.append(ratingDate.text)
        ratingdate = item.ratingdate.text
    for Add2 in item.findAll("addressline2"):
        address2 = item.addressline2.text
    for Add3 in item.findAll("addressline3"):
        address3 = item.addressline3.text
    for Add4 in item.findAll("addressline4"):
        address4 = item.addressline4.text
    for postCode in item.findAll("postcode"):
        postcode = item.postcode.text
    for lng in item.findAll("longitude"):
        #titles.append(lng.text)
        longitude = item.longitude.text
    for lat in item.findAll("latitude"):
       
        latitude = item.latitude.text
        #print latitude
        scraperwiki.sqlite.save(unique_keys=[], data={'BusinessName':name,'BusinessType':business_type,'Rating':rating_value,'RatingDate':ratingdate,'Address2':address2,'Address3':address3,'address4':address4,'Postcode':postcode,'lat':latitude,'lng':longitude}) 

