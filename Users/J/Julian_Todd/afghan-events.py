import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
import scraperwiki
import xlrd
import urllib
import datetime

url = "http://image.guardian.co.uk/sys-files/Guardian/documents/2010/07/25/Afghanevents1.xls"
contents = urllib.urlopen(url).read()
#scraperwiki.metadata.save("Afghanevents1", contents)

book = xlrd.open_workbook(file_contents=contents)

assert book.nsheets == 1, book.nsheets
sheet = book.sheet_by_index(0)
                      
headers = [ sheet.cell(1, column).value  for column in range(sheet.ncols) ]
assert headers == [u'reportkey', u'Guardian incident url', u'lat', u'long', u'bundle', u'Guardian headline', 
                  u'dateoccurred', u'type', u'category', u'Guardian edited category', u'trackingnumber', 
                  u'title', u'summary', u'region', u'attackon', u'complexattack', 
                  u'reportingunit', u'unitname', u'typeofunit', u'friendlywia', u'friendlykia', u'hostnationwia', 
                  u'hostnationkia', u'civilianwia', u'civiliankia', u'enemywia', u'enemykia', u'enemydetained', u'mgrs', 
                  u'latitude', u'longitude', u'originatorgroup', u'updatedbygroup', u'ccir', u'sigact', u'affiliation', u'dcolor'], headers

def ConvertCell(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        d = xlrd.xldate_as_tuple(cell.value, 0)
        return datetime.date(d[0], d[1], d[2])
    return cell.value

for row in range(2, sheet.nrows): 
    rowvals = [ ConvertCell(sheet.cell(row, column)) for column in range(sheet.ncols) ]
    data = dict(zip(headers, rowvals))
    
    lat, lng = data.pop('lat'), data.pop('long')
    latitude, longitude = data.pop('latitude'), data.pop('longitude')
    if 20 < latitude < 60 and 30 < longitude < 100:
        latlng = [latitude, longitude]
        assert max(abs(latitude - lat), abs(longitude - lng)) < 0.0001, (lat, lng, latitude, longitude)
        data["latlng_lat"] = latitude
        data["latlng_lng"] = longitude
            
    scraperwiki.sqlite.save(unique_keys=['reportkey'], data=data)
    
                      
