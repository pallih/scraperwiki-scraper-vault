import scraperwiki

from scraperwiki import sqlite
from BeautifulSoup import BeautifulStoneSoup

import urllib2
import urllib

_postcodesURL = "http://www.nhs.uk/NHSCWS/Services/ServicesSearch.aspx?user=Hackday.2&pwd=WOdaJaGc&type=5&q=%20"
_servicesURL = "http://www.nhs.uk/NHSCWS/Services/ServicesSearch.aspx?user=Hackday.2&pwd=WOdaJaGc&type=5&PageSize=100&"

# see if postcodes have already been retrieved and stored

try:
    postcodes = sqlite.select("* from postcodes where retrieved == '0'")

# if not, retrieve and store them

except sqlite.SqliteError, e:
    print "Postcodes table does not exist, retrieving postcodes"

    postcodesRaw = scraperwiki.scrape(_postcodesURL)
    postcodesTree = BeautifulStoneSoup(postcodesRaw)
    postcodesList = []

    locations = postcodesTree.findAll('location')

    i = 1
    j = len(locations)

    for location in locations:
        postcode = location.value.string.strip().split(',')[-1][:-1].strip()
        postcodesList.append(postcode)

        print str(int((float(i) / float(j)) * 100)) + "%"
        i += 1

    postcodesList = list(set(postcodesList))

    for postcode in postcodesList:
        sqlite.save(unique_keys=['postcode'], data={'postcode':postcode, 'retrieved':False}, table_name="postcodes")

    postcodes = sqlite.select("* from postcodes")

try:
    k = 0
    for postcode in postcodes:
        if postcode['retrieved'] == "0":
            print " "
            print "*** Retrieving services for " + postcode['postcode']

            servicesURL = _servicesURL + urllib.urlencode({'q': postcode['postcode']})
            servicesRaw = scraperwiki.scrape(servicesURL)
            servicesTree = BeautifulStoneSoup(servicesRaw, selfClosingTags=[
                'coords',
                'code1',
                'code2',
                'address1',
                'address2',
                'address3',
                'address4',
                ])
            
            for service in servicesTree.findAll('service'):
                data = {}
                
                data['code1'] = service.code1.string
        
                data['code2'] = service.code2.string
                
                data['name'] = service.find('name').string
                data['type'] = service.type.string
                data['address1'] = service.address1.string
                data['address2'] = service.address2.string
                data['address3'] = service.address3.string
                data['address4'] = service.address4.string
                data['address5'] = service.address5.string
                data['postcode'] = service.postcode.string
        
                data['telephone'] = service.telephone.string
                data['website'] = service.website.string
        
                data['northing'] = service.northing.string
                data['easting'] = service.easting.string
                data['latitude'] = float(service.latitude.string)
                data['longitude'] = float(service.longitude.string)
                data['coords'] = service.coords
                
                data['hasaande'] = service.hasaande.string
                data['category'] = service.category.string
                data['organisationcommentcount'] = service.organisationcommentcount.string
                data['providerprofilepageurl'] = service.providerprofilepageurl.string

                print "- " + data['name']

                sqlite.save(unique_keys=['name'], data=data, table_name="services")

            sqlite.execute("update postcodes set retrieved = ? where postcode = ?", [True, postcode['postcode']])
            
        #    k += 1
        #    if k == 10:
        #        print " "
        #        print "*** Reached safe processing limit, run again to continue"
        #
        #        break
    
        else:
            print " "
            print "*** " + postcode['postcode'] + " has already been retrieved, skipping"

except scraperwiki.CPUTimeExceededError:
    print " "
    print "*** CPU exception caught"
    print "    You should be able to just run again and start from where you left off"import scraperwiki

from scraperwiki import sqlite
from BeautifulSoup import BeautifulStoneSoup

import urllib2
import urllib

_postcodesURL = "http://www.nhs.uk/NHSCWS/Services/ServicesSearch.aspx?user=Hackday.2&pwd=WOdaJaGc&type=5&q=%20"
_servicesURL = "http://www.nhs.uk/NHSCWS/Services/ServicesSearch.aspx?user=Hackday.2&pwd=WOdaJaGc&type=5&PageSize=100&"

# see if postcodes have already been retrieved and stored

try:
    postcodes = sqlite.select("* from postcodes where retrieved == '0'")

# if not, retrieve and store them

except sqlite.SqliteError, e:
    print "Postcodes table does not exist, retrieving postcodes"

    postcodesRaw = scraperwiki.scrape(_postcodesURL)
    postcodesTree = BeautifulStoneSoup(postcodesRaw)
    postcodesList = []

    locations = postcodesTree.findAll('location')

    i = 1
    j = len(locations)

    for location in locations:
        postcode = location.value.string.strip().split(',')[-1][:-1].strip()
        postcodesList.append(postcode)

        print str(int((float(i) / float(j)) * 100)) + "%"
        i += 1

    postcodesList = list(set(postcodesList))

    for postcode in postcodesList:
        sqlite.save(unique_keys=['postcode'], data={'postcode':postcode, 'retrieved':False}, table_name="postcodes")

    postcodes = sqlite.select("* from postcodes")

try:
    k = 0
    for postcode in postcodes:
        if postcode['retrieved'] == "0":
            print " "
            print "*** Retrieving services for " + postcode['postcode']

            servicesURL = _servicesURL + urllib.urlencode({'q': postcode['postcode']})
            servicesRaw = scraperwiki.scrape(servicesURL)
            servicesTree = BeautifulStoneSoup(servicesRaw, selfClosingTags=[
                'coords',
                'code1',
                'code2',
                'address1',
                'address2',
                'address3',
                'address4',
                ])
            
            for service in servicesTree.findAll('service'):
                data = {}
                
                data['code1'] = service.code1.string
        
                data['code2'] = service.code2.string
                
                data['name'] = service.find('name').string
                data['type'] = service.type.string
                data['address1'] = service.address1.string
                data['address2'] = service.address2.string
                data['address3'] = service.address3.string
                data['address4'] = service.address4.string
                data['address5'] = service.address5.string
                data['postcode'] = service.postcode.string
        
                data['telephone'] = service.telephone.string
                data['website'] = service.website.string
        
                data['northing'] = service.northing.string
                data['easting'] = service.easting.string
                data['latitude'] = float(service.latitude.string)
                data['longitude'] = float(service.longitude.string)
                data['coords'] = service.coords
                
                data['hasaande'] = service.hasaande.string
                data['category'] = service.category.string
                data['organisationcommentcount'] = service.organisationcommentcount.string
                data['providerprofilepageurl'] = service.providerprofilepageurl.string

                print "- " + data['name']

                sqlite.save(unique_keys=['name'], data=data, table_name="services")

            sqlite.execute("update postcodes set retrieved = ? where postcode = ?", [True, postcode['postcode']])
            
        #    k += 1
        #    if k == 10:
        #        print " "
        #        print "*** Reached safe processing limit, run again to continue"
        #
        #        break
    
        else:
            print " "
            print "*** " + postcode['postcode'] + " has already been retrieved, skipping"

except scraperwiki.CPUTimeExceededError:
    print " "
    print "*** CPU exception caught"
    print "    You should be able to just run again and start from where you left off"