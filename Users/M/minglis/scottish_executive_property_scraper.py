# Scaper to parse scottish exec property pages
# these are found at http://scottish-property.gov.uk

import scraperwiki
import urlparse
import lxml.html
import lxml.etree
import mechanize
import re
import simplejson, urllib

ROOT_URL = 'http://scottish-property.gov.uk'
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false'

def geocode(address,sensor=False, **geo_args):
    geo_args.update({
        'address': address,
        'region': 'uk'
    })

    url = GEOCODE_BASE_URL + '&' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    print result
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    return lat, lng

def strip_empty_array_elements(nasty_array):
    new_list = [];
    for bit in nasty_array:
        if(len(bit) > 0 or not bit.isspace()):
            stripped = bit.strip().rstrip().replace('\n','').replace('\t','').lstrip().replace(' ','').replace('&#13;','').replace('<','').replace('>','').replace('/','')

            if(stripped.find('div') != -1):
                new_list.append(stripped[0:stripped.find('div')])
            else:
                new_list.append(stripped)
    return new_list

def get_usage(row):
    usage = row.cssselect('table tr td')

    if(len(usage) > 100 ):
         property['use_type'] = usage[0].text.strip()
         property['use_type_detail'] = usage[1].text.strip()
         property['size'] = usage[3].text.strip()
         property['lease'] = usage[4].text.strip()
         property['lease_status'] = usage[5].text.strip()
         property['finance'] = usage[6].text.strip()
         property['cost'] = usage[7].text.strip()

def get_image(row):
    img = row.cssselect('img')
    if(len(img) > 0):
        return ROOT_URL + img[0].get('src')
    else:
        return "";

def get_link(row):
    link = row.cssselect('a.searchresults')
    if(len(link) > 0):    
        return ROOT_URL + '/search/' + row.cssselect('a.searchresults')[0].get('href')
    else:
        return ""

def get_address(row):
    left = lxml.etree.tostring(row).find('<br/>')
    right = lxml.etree.tostring(row).rfind('<br/>')

    chunk = lxml.etree.tostring(row)[left:right]

    end = chunk.find('td')

    final_bit = chunk[:end]

    address_chunks = strip_empty_array_elements(final_bit.split('<br/>'))

    final_address = []
    
    for bit in address_chunks:
        if (len(bit) > 0 and bit.find('Fax') == -1 and bit.find('Tel') == -1):
            final_address.append(bit)   
    return ", ".join(final_address)

def is_good_row(property):
    return property['address'] != '' and not property['address'].startswith('EMail')


# fix me - reduced data set for development
URL = 'http://scottish-property.gov.uk/search/index.cfm?search=QuickSearch%2Ecfm&FUSEACTION=QuickPropertySearch&ADDRESS=&PROPERTYTYPE=&QPSSIZE=&startrow=1&endrow=100'

html = scraperwiki.scrape(URL)

print html

root = lxml.html.fromstring(html)
rows = root.cssselect('table[bgcolor=ffffff] > tr')

i = 0;
print len(rows)

for row in rows:
    i += 1

    property = {}    

    print "here" + lxml.etree.tostring(row)

    #property['image'] = get_image(row)
    #property['moreDetails'] = get_link(row)    
    #property['address'] = get_address(row)  


    #property['lat'],property['long'] = geocode(final_address[4])

    #if is_good_row(property):
    #    property['id'] = i
    #    scraperwiki.datastore.save(["id"], property)
    #    print 'saving'


# Scaper to parse scottish exec property pages
# these are found at http://scottish-property.gov.uk

import scraperwiki
import urlparse
import lxml.html
import lxml.etree
import mechanize
import re
import simplejson, urllib

ROOT_URL = 'http://scottish-property.gov.uk'
GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false'

def geocode(address,sensor=False, **geo_args):
    geo_args.update({
        'address': address,
        'region': 'uk'
    })

    url = GEOCODE_BASE_URL + '&' + urllib.urlencode(geo_args)
    result = simplejson.load(urllib.urlopen(url))
    print result
    lat = result['results'][0]['geometry']['location']['lat']
    lng = result['results'][0]['geometry']['location']['lng']
    return lat, lng

def strip_empty_array_elements(nasty_array):
    new_list = [];
    for bit in nasty_array:
        if(len(bit) > 0 or not bit.isspace()):
            stripped = bit.strip().rstrip().replace('\n','').replace('\t','').lstrip().replace(' ','').replace('&#13;','').replace('<','').replace('>','').replace('/','')

            if(stripped.find('div') != -1):
                new_list.append(stripped[0:stripped.find('div')])
            else:
                new_list.append(stripped)
    return new_list

def get_usage(row):
    usage = row.cssselect('table tr td')

    if(len(usage) > 100 ):
         property['use_type'] = usage[0].text.strip()
         property['use_type_detail'] = usage[1].text.strip()
         property['size'] = usage[3].text.strip()
         property['lease'] = usage[4].text.strip()
         property['lease_status'] = usage[5].text.strip()
         property['finance'] = usage[6].text.strip()
         property['cost'] = usage[7].text.strip()

def get_image(row):
    img = row.cssselect('img')
    if(len(img) > 0):
        return ROOT_URL + img[0].get('src')
    else:
        return "";

def get_link(row):
    link = row.cssselect('a.searchresults')
    if(len(link) > 0):    
        return ROOT_URL + '/search/' + row.cssselect('a.searchresults')[0].get('href')
    else:
        return ""

def get_address(row):
    left = lxml.etree.tostring(row).find('<br/>')
    right = lxml.etree.tostring(row).rfind('<br/>')

    chunk = lxml.etree.tostring(row)[left:right]

    end = chunk.find('td')

    final_bit = chunk[:end]

    address_chunks = strip_empty_array_elements(final_bit.split('<br/>'))

    final_address = []
    
    for bit in address_chunks:
        if (len(bit) > 0 and bit.find('Fax') == -1 and bit.find('Tel') == -1):
            final_address.append(bit)   
    return ", ".join(final_address)

def is_good_row(property):
    return property['address'] != '' and not property['address'].startswith('EMail')


# fix me - reduced data set for development
URL = 'http://scottish-property.gov.uk/search/index.cfm?search=QuickSearch%2Ecfm&FUSEACTION=QuickPropertySearch&ADDRESS=&PROPERTYTYPE=&QPSSIZE=&startrow=1&endrow=100'

html = scraperwiki.scrape(URL)

print html

root = lxml.html.fromstring(html)
rows = root.cssselect('table[bgcolor=ffffff] > tr')

i = 0;
print len(rows)

for row in rows:
    i += 1

    property = {}    

    print "here" + lxml.etree.tostring(row)

    #property['image'] = get_image(row)
    #property['moreDetails'] = get_link(row)    
    #property['address'] = get_address(row)  


    #property['lat'],property['long'] = geocode(final_address[4])

    #if is_good_row(property):
    #    property['id'] = i
    #    scraperwiki.datastore.save(["id"], property)
    #    print 'saving'


