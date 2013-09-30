import urllib
import xlrd
import zipfile
import scraperwiki
from StringIO import StringIO

url = "http://www.whatdotheyknow.com/request/18787/response/47082/attach/3/temps20091002.zip"

# Open the zipfile and squirt the contents into an xlrd document.
fin = urllib.urlopen(url)
zipxl = fin.read()

zipxlin = StringIO(zipxl)
zipxlf = zipfile.ZipFile(zipxlin)
xlbytes = zipxlf.read(zipxlf.namelist()[0])

xl = xlrd.open_workbook(file_contents=xlbytes)

sheet = xl.sheet_by_index(0)

for i in range(1, sheet.nrows): # use sheet.nrows
    row = sheet.row(i)
    stationname = row[0].value
    date_tuple = xlrd.xldate_as_tuple(row[1].value, xl.datemode)
    date_string = "%04d-%02d-%02d" % date_tuple[:3]
    if date_string.endswith('-01'):
        print date_string, stationname
    stationid = 'uk_' + stationname.replace(' ', '').lower()
    # Data is written to the store so that each row represents all the data
    # for a single meteorological element (tmin, tmax, etc) for a single station.
    # Each day's data appears under a new key.  Thus the "row" will have hundreds of keys.
    for element,idx in [('tmaxD',2), ('tminD',3), ('tmeanD',4)]:
        try:
            value = float(row[idx].value)
            d = dict(element=element, id=stationid, date=date_string, value=value)
            print d
            scraperwiki.sqlite.save(unique_keys=['id', 'element'], data=d)
        except ValueError:
            break
import urllib
import xlrd
import zipfile
import scraperwiki
from StringIO import StringIO

url = "http://www.whatdotheyknow.com/request/18787/response/47082/attach/3/temps20091002.zip"

# Open the zipfile and squirt the contents into an xlrd document.
fin = urllib.urlopen(url)
zipxl = fin.read()

zipxlin = StringIO(zipxl)
zipxlf = zipfile.ZipFile(zipxlin)
xlbytes = zipxlf.read(zipxlf.namelist()[0])

xl = xlrd.open_workbook(file_contents=xlbytes)

sheet = xl.sheet_by_index(0)

for i in range(1, sheet.nrows): # use sheet.nrows
    row = sheet.row(i)
    stationname = row[0].value
    date_tuple = xlrd.xldate_as_tuple(row[1].value, xl.datemode)
    date_string = "%04d-%02d-%02d" % date_tuple[:3]
    if date_string.endswith('-01'):
        print date_string, stationname
    stationid = 'uk_' + stationname.replace(' ', '').lower()
    # Data is written to the store so that each row represents all the data
    # for a single meteorological element (tmin, tmax, etc) for a single station.
    # Each day's data appears under a new key.  Thus the "row" will have hundreds of keys.
    for element,idx in [('tmaxD',2), ('tminD',3), ('tmeanD',4)]:
        try:
            value = float(row[idx].value)
            d = dict(element=element, id=stationid, date=date_string, value=value)
            print d
            scraperwiki.sqlite.save(unique_keys=['id', 'element'], data=d)
        except ValueError:
            break
