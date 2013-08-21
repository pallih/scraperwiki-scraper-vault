# Sampad Mailing List Postcodes

# We first download the zip file, extract the xls file, and save it to disk
# Then we read the xls file and save its contents to the datastore
# And because we're awesome, we also geocode the postcodes

import scraperwiki
from geopy import geocoders
import xlrd
import os

# handy function for working with excel cells
def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

def geocode_postcode(postcode, provider='geonames'):
    import urllib2, json

    if provider=='geonames':
        resp = scraperwiki.scrape('http://api.geonames.org/postalCodeSearchJSON?postalcode=%s&maxRows=1&username=scraperwiki' % urllib2.quote(postcode))
        obj = json.loads(resp)
        if len(obj['postalCodes']):
            return (obj['postalCodes'][0]['lat'], obj['postalCodes'][0]['lng'])
        else:
            return (None,None)

    elif provider=='mapit':
        try:
            resp = scraperwiki.scrape('http://mapit.mysociety.org/postcode/%s.json' % urllib2.quote(postcode))
        except urllib2.HTTPError:
            return (None, None)
        else:
            obj = json.loads(resp)
            if obj['wgs84_lat'] and obj['wgs84_lon']:
                return (obj['wgs84_lat'], obj['wgs84_lon'])
            else:
                return (None,None)

    elif provider=='jamiethompson':
        import requests
        try:
            resp = requests.get('http://geo.jamiethompson.co.uk/%s.json' % postcode.replace(' ',''), timeout=5).text
        except:
            return (None,None)
        else:
            obj = json.loads(resp)
            if 'geo' in obj and obj['geo']['lat'] and obj['geo']['lng']:
                return (obj['geo']['lat'], obj['geo']['lng'])
            else:
                return (None,None)

    else:
        return(None, None)

def main():
    scraperwiki.scrape('http://www.sampad.org.uk/') # get pretty screenshot
    #extract_data_from_xls('http://files.zarino.co.uk/scraperwiki/sampad_postcodesJune12.xls')
    geocode()


def extract_data_from_xls(url):
    print 'Downloading xls file:', url
    bin = scraperwiki.scrape(url)
    print 'Extracting data from xls file'
    print '-- reading xls file'
    book = xlrd.open_workbook(file_contents=bin)

    print '-- workbook contains', len(book.sheets()), 'sheets'
    for n, s in enumerate(book.sheets()):
        print "-- sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

    extract_data_from_sheet(book, 0, 'subscriber')


def extract_data_from_sheet(book, num, name):
    print '-- extracting ' + name + ' postcodes and geocoding'
    sheet = book.sheet_by_index(num)

    i = 0
    postcodes = []
    for n in range(0, sheet.nrows):
        postcode = cellval(sheet.row(n)[0], book.datemode)
        tmp = {
            'postcode': postcode,
            'lat': None,
            'lng': None
        }
        postcodes.append(tmp)
        i += 1

    scraperwiki.sqlite.save(['postcode'], postcodes, 'postcodes')
    print '-- saved',  i, ' rows to database'


def geocode():
    print 'Geocoding postcodes...'
    try:
        rows = scraperwiki.sqlite.select('* FROM postcodes WHERE lat IS NULL')
    except:
        rows = scraperwiki.sqlite.select('* FROM postcodes')
    print '-- ' + str(len(rows)) + ' postcodes to geocode'

    i = 0
    total_geocoded = 0
    tmp = []
    for row in rows:
        (lat,lng) = geocode_postcode(row['postcode'], 'jamiethompson')
        tmp.append({
            'postcode': row['postcode'],
            'lat': lat,
            'lng': lng
        })
        if len(tmp)==10 or i==len(rows)-1:
            scraperwiki.sqlite.save(['postcode'], tmp, 'postcodes')
            total_geocoded += len(tmp)
            print total_geocoded, ' postcodes geocoded'
            tmp = []
        i += 1

main()




