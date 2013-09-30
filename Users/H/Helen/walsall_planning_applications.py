import scraperwiki
import BeautifulSoup
import re
import urllib2

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www2.walsall.gov.uk/dcaccess/headway/weeklylist.asp')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
table = page.findAll("table", { "class" : "MISresults" })
for table in table:
    row = table.findAll('tr')[1:]
    for row in row:
        appNo = row.findAll('td')[0].find("input", { "name" : "AppNumber" })['value']
        appID = row.findAll('td')[0].find("input", { "name" : "AppID" })['value']
        UPRN = row.findAll('td')[0].find("input", { "name" : "UPRN" })['value']
        ward = row.findAll('td')[1].string
        validDate = row.findAll('td')[2].string
        description = row.findAll('td')[3].string
        address = row.findAll('td')[4].string
        if re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b', address.split(',')[-1]):
            postcode = address.split(',')[-1]
            url = 'http://www.uk-postcodes.com/postcode/'+ postcode.replace(' ', '') +'.csv'
            try:
                ukpostcodes = urllib2.urlopen(url)
                latlng = ukpostcodes.read().split(',')
                lat = latlng[1]
                lng = latlng[2]
            except:
                lat = ''
                lng = ''
        else:
            postcode = ''
            lat = ''
            lng = ''
        recievedDate = row.findAll('td')[5].string
        
        data = {'Application Number':appNo, 'Ward':ward, 'Validated':validDate,
                'Description':description,'Address':address,'Postcode':postcode, 
                'Latitude':lat, 'Longitude':lng, 'Date Recieved':recievedDate,
                'appID':appID, 'UPRN':UPRN}
        latlng = lat and lng and (float(lat), float(lng)) or None
        datastore.save(['Application Number'], data, latlng=latlng)


import scraperwiki
import BeautifulSoup
import re
import urllib2

from scraperwiki import datastore

# Hello World Example #

#scrape page
html = scraperwiki.scrape('http://www2.walsall.gov.uk/dcaccess/headway/weeklylist.asp')
page = BeautifulSoup.BeautifulSoup(html)

#find rows
table = page.findAll("table", { "class" : "MISresults" })
for table in table:
    row = table.findAll('tr')[1:]
    for row in row:
        appNo = row.findAll('td')[0].find("input", { "name" : "AppNumber" })['value']
        appID = row.findAll('td')[0].find("input", { "name" : "AppID" })['value']
        UPRN = row.findAll('td')[0].find("input", { "name" : "UPRN" })['value']
        ward = row.findAll('td')[1].string
        validDate = row.findAll('td')[2].string
        description = row.findAll('td')[3].string
        address = row.findAll('td')[4].string
        if re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b', address.split(',')[-1]):
            postcode = address.split(',')[-1]
            url = 'http://www.uk-postcodes.com/postcode/'+ postcode.replace(' ', '') +'.csv'
            try:
                ukpostcodes = urllib2.urlopen(url)
                latlng = ukpostcodes.read().split(',')
                lat = latlng[1]
                lng = latlng[2]
            except:
                lat = ''
                lng = ''
        else:
            postcode = ''
            lat = ''
            lng = ''
        recievedDate = row.findAll('td')[5].string
        
        data = {'Application Number':appNo, 'Ward':ward, 'Validated':validDate,
                'Description':description,'Address':address,'Postcode':postcode, 
                'Latitude':lat, 'Longitude':lng, 'Date Recieved':recievedDate,
                'appID':appID, 'UPRN':UPRN}
        latlng = lat and lng and (float(lat), float(lng)) or None
        datastore.save(['Application Number'], data, latlng=latlng)


