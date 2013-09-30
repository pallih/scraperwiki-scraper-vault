# Reads information from FOI request and loads into datastore

import xlrd    

import re
import string
import scraperwiki
import dateutil.parser
import datetime
import sys
import json

import urllib2

def put_data(data):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request('http://couchdb.flourish.org/testeroo', data=json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    try:
        url = opener.open(request)
    except urllib2.URLError, e:
        print "PUT to couchdb failed"
        print e
        sys.exit()

url= 'http://www.whatdotheyknow.com/request/30484/response/78880/attach/5/96071%20Ctax%20Empty%20Properties.xls'
book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# We can find out information about the workbook - number of sheets
print "Workbook has %s sheet(s)" % book.nsheets

firstSheet = book.sheet_by_index(0)
                      
# You can loop over all the cells in the worksheet
for row in range(0,firstSheet.nrows): # for each row
    data = {}
    data['ctax_prop_ref'] = firstSheet.cell(row,0).value                     
    if data['ctax_prop_ref'] == u'CTAX_PROP_REF':
        continue
    
    data['address1'] = firstSheet.cell(row, 1).value
    data['address2'] = firstSheet.cell(row, 2).value
    data['postcode'] = firstSheet.cell(row, 3).value
    data['band'] = firstSheet.cell(row, 4).value
    data['per_start'] =  xlrd.xldate_as_tuple(firstSheet.cell(row, 5).value, book.datemode)

    lat_lng = scraperwiki.geo.gb_postcode_to_latlng(data['postcode'])
    #data['parsed_date'] = datetime.date(data['per_start'][0], data['per_start'][1], data['per_start'][2])
    data['lat'] = lat_lng[0]
    data['lng'] = lat_lng[1]

    #data['_id'] = data['ctax_prop_ref']
    #data['_rev'] = data['ctax_prop_ref']

    #scraperwiki.datastore.save(['ctax_prop_ref'], data=data, date=parsed_date, latlng=lat_lng)
    put_data(data)
    sys.exit()
# Reads information from FOI request and loads into datastore

import xlrd    

import re
import string
import scraperwiki
import dateutil.parser
import datetime
import sys
import json

import urllib2

def put_data(data):
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request('http://couchdb.flourish.org/testeroo', data=json.dumps(data))
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    try:
        url = opener.open(request)
    except urllib2.URLError, e:
        print "PUT to couchdb failed"
        print e
        sys.exit()

url= 'http://www.whatdotheyknow.com/request/30484/response/78880/attach/5/96071%20Ctax%20Empty%20Properties.xls'
book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# We can find out information about the workbook - number of sheets
print "Workbook has %s sheet(s)" % book.nsheets

firstSheet = book.sheet_by_index(0)
                      
# You can loop over all the cells in the worksheet
for row in range(0,firstSheet.nrows): # for each row
    data = {}
    data['ctax_prop_ref'] = firstSheet.cell(row,0).value                     
    if data['ctax_prop_ref'] == u'CTAX_PROP_REF':
        continue
    
    data['address1'] = firstSheet.cell(row, 1).value
    data['address2'] = firstSheet.cell(row, 2).value
    data['postcode'] = firstSheet.cell(row, 3).value
    data['band'] = firstSheet.cell(row, 4).value
    data['per_start'] =  xlrd.xldate_as_tuple(firstSheet.cell(row, 5).value, book.datemode)

    lat_lng = scraperwiki.geo.gb_postcode_to_latlng(data['postcode'])
    #data['parsed_date'] = datetime.date(data['per_start'][0], data['per_start'][1], data['per_start'][2])
    data['lat'] = lat_lng[0]
    data['lng'] = lat_lng[1]

    #data['_id'] = data['ctax_prop_ref']
    #data['_rev'] = data['ctax_prop_ref']

    #scraperwiki.datastore.save(['ctax_prop_ref'], data=data, date=parsed_date, latlng=lat_lng)
    put_data(data)
    sys.exit()
