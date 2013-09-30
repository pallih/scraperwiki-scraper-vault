# Liverpool Schools Data

# Data provided by TATE Liverpool for academic use only:
# http://www.ljmu.ac.uk/MAS/Openlabs/OpenLabs_Docs/TATE_LIVERPOOL_EXHIBITIONS_ENTA_DATA.zip

# We first download the zip file, extract the xls file, and save it to disk
# Then we read the xls file and save its contents to the datastore
# And because we're awesome, we also geocode the postcodes


import scraperwiki
import tempfile, zipfile
import urllib
import base64
import xlrd
import os
import datetime

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


def main():
    """# get pretty screenshot
    scraperwiki.scrape('http://www.ljmu.ac.uk/aps/openlabs/')

    # Check whether file exists
    print 'Q: I CAN HAZ XLS?'
    try:
        open(os.getcwd() + '/TATE_LIVERPOOL_EXHIBITIONS_ENTA DATA.xls', 'r')
        print 'A: COMPUTER SAYS YES!'
    except:
        print 'A: COMPUTER SAYS NO :-('
        download_xls()
    
    extract_data_from_xls()
    geocode()"""
    postcode_district()


def download_xls():
    print 'Downloading zip file from ljmu.ac.uk...'
    print '-- creating temp file'
    t = tempfile.NamedTemporaryFile(suffix=".zip")
    
    print '-- downloading zip'
    t.write(urllib.urlopen('http://www.ljmu.ac.uk/MAS/Openlabs/OpenLabs_Docs/TATE_LIVERPOOL_EXHIBITIONS_ENTA_DATA.zip').read())
    t.seek(0)
    
    print '-- unzipping'
    z = zipfile.ZipFile(t.name)

    print '-- unzipped!'
    contents = z.namelist()

    print '-- saving file "' + contents[0] + '" to local storage'
    z.extract('TATE_LIVERPOOL_EXHIBITIONS_ENTA DATA.xls')
    print '-- file saved!'



def extract_data_from_xls():
    print 'Extracting data from xls file...'
    print '-- reading xls file'
    bin = open(os.getcwd() + '/TATE_LIVERPOOL_EXHIBITIONS_ENTA DATA.xls', 'r').read()
    book = xlrd.open_workbook(file_contents=bin)
    for n, s in enumerate(book.sheets()):
        print "-- sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

    extract_data_from_sheet(book, 1, 'Magritte')
    extract_data_from_sheet(book, 2, 'Alice')



def extract_data_from_sheet(book, num, name):
    print '-- extracting ' + name + ' data'
    sheet = book.sheet_by_index(num)

    keys = []
    for key in sheet.row_values(0):
        keys.append(key.replace(' ', '_').lower())

    i = 0
    for n in range(1, sheet.nrows):
        values = [ cellval(c, book.datemode) for c in sheet.row(n) ]
        data = dict(zip(keys, values))
        scraperwiki.sqlite.save([keys[0]], data)
        i = i + 1
    print '-- saved ' + str(i) + ' rows to database'



def geocode():
    print 'Geocoding postcodes...'
    try:
        rows = scraperwiki.sqlite.select('* FROM swdata WHERE postcode IS NOT NULL and lat IS NULL')
    except:
        rows = scraperwiki.sqlite.select('* FROM swdata WHERE postcode IS NOT NULL')
    print '-- ' + str(len(rows)) + ' postcodes to geocode'

    scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', 'p')

    for row in rows:
        lres = scraperwiki.sqlite.select('Northings, Eastings from p.swdata where Postcode like ? limit 1', row['postcode'].replace(' ', ''))
        if lres:
            loc = scraperwiki.geo.os_easting_northing_to_latlng(lres[0]['Eastings'], lres[0]['Northings'], grid='GB')
            row['lat'] = loc[0]
            row['long'] = loc[1]
            scraperwiki.sqlite.save(['booking_reference_number'], row)
        else:
            print '!! could not geocode ' + str(row['postcode']) + ' (booking_reference_number ' + str(int(row['booking_reference_number'])) + ')'

        #loc = scraperwiki.geo.gb_postcode_to_latlng( row['postcode'].replace(' ', '') )
        #if loc:
        #    row['lat'] = loc[0]
        #    row['long'] = loc[1]
        #    scraperwiki.sqlite.save(['booking_reference_number'], row)
        #else:
        #    print '!! could not geocode ' + str(row['postcode']) + ' (booking_reference_number ' + str(int(row['booking_reference_number'])) + ')'



def postcode_district():
    rows = scraperwiki.sqlite.select('* FROM swdata WHERE postcode IS NOT NULL and postcode_district IS NULL')
    for row in rows:
        row['postcode_district'] = row['postcode'].partition(' ')[0]
        scraperwiki.sqlite.save(['booking_reference_number'], row)


main()




# Liverpool Schools Data

# Data provided by TATE Liverpool for academic use only:
# http://www.ljmu.ac.uk/MAS/Openlabs/OpenLabs_Docs/TATE_LIVERPOOL_EXHIBITIONS_ENTA_DATA.zip

# We first download the zip file, extract the xls file, and save it to disk
# Then we read the xls file and save its contents to the datastore
# And because we're awesome, we also geocode the postcodes


import scraperwiki
import tempfile, zipfile
import urllib
import base64
import xlrd
import os
import datetime

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


def main():
    """# get pretty screenshot
    scraperwiki.scrape('http://www.ljmu.ac.uk/aps/openlabs/')

    # Check whether file exists
    print 'Q: I CAN HAZ XLS?'
    try:
        open(os.getcwd() + '/TATE_LIVERPOOL_EXHIBITIONS_ENTA DATA.xls', 'r')
        print 'A: COMPUTER SAYS YES!'
    except:
        print 'A: COMPUTER SAYS NO :-('
        download_xls()
    
    extract_data_from_xls()
    geocode()"""
    postcode_district()


def download_xls():
    print 'Downloading zip file from ljmu.ac.uk...'
    print '-- creating temp file'
    t = tempfile.NamedTemporaryFile(suffix=".zip")
    
    print '-- downloading zip'
    t.write(urllib.urlopen('http://www.ljmu.ac.uk/MAS/Openlabs/OpenLabs_Docs/TATE_LIVERPOOL_EXHIBITIONS_ENTA_DATA.zip').read())
    t.seek(0)
    
    print '-- unzipping'
    z = zipfile.ZipFile(t.name)

    print '-- unzipped!'
    contents = z.namelist()

    print '-- saving file "' + contents[0] + '" to local storage'
    z.extract('TATE_LIVERPOOL_EXHIBITIONS_ENTA DATA.xls')
    print '-- file saved!'



def extract_data_from_xls():
    print 'Extracting data from xls file...'
    print '-- reading xls file'
    bin = open(os.getcwd() + '/TATE_LIVERPOOL_EXHIBITIONS_ENTA DATA.xls', 'r').read()
    book = xlrd.open_workbook(file_contents=bin)
    for n, s in enumerate(book.sheets()):
        print "-- sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

    extract_data_from_sheet(book, 1, 'Magritte')
    extract_data_from_sheet(book, 2, 'Alice')



def extract_data_from_sheet(book, num, name):
    print '-- extracting ' + name + ' data'
    sheet = book.sheet_by_index(num)

    keys = []
    for key in sheet.row_values(0):
        keys.append(key.replace(' ', '_').lower())

    i = 0
    for n in range(1, sheet.nrows):
        values = [ cellval(c, book.datemode) for c in sheet.row(n) ]
        data = dict(zip(keys, values))
        scraperwiki.sqlite.save([keys[0]], data)
        i = i + 1
    print '-- saved ' + str(i) + ' rows to database'



def geocode():
    print 'Geocoding postcodes...'
    try:
        rows = scraperwiki.sqlite.select('* FROM swdata WHERE postcode IS NOT NULL and lat IS NULL')
    except:
        rows = scraperwiki.sqlite.select('* FROM swdata WHERE postcode IS NOT NULL')
    print '-- ' + str(len(rows)) + ' postcodes to geocode'

    scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', 'p')

    for row in rows:
        lres = scraperwiki.sqlite.select('Northings, Eastings from p.swdata where Postcode like ? limit 1', row['postcode'].replace(' ', ''))
        if lres:
            loc = scraperwiki.geo.os_easting_northing_to_latlng(lres[0]['Eastings'], lres[0]['Northings'], grid='GB')
            row['lat'] = loc[0]
            row['long'] = loc[1]
            scraperwiki.sqlite.save(['booking_reference_number'], row)
        else:
            print '!! could not geocode ' + str(row['postcode']) + ' (booking_reference_number ' + str(int(row['booking_reference_number'])) + ')'

        #loc = scraperwiki.geo.gb_postcode_to_latlng( row['postcode'].replace(' ', '') )
        #if loc:
        #    row['lat'] = loc[0]
        #    row['long'] = loc[1]
        #    scraperwiki.sqlite.save(['booking_reference_number'], row)
        #else:
        #    print '!! could not geocode ' + str(row['postcode']) + ' (booking_reference_number ' + str(int(row['booking_reference_number'])) + ')'



def postcode_district():
    rows = scraperwiki.sqlite.select('* FROM swdata WHERE postcode IS NOT NULL and postcode_district IS NULL')
    for row in rows:
        row['postcode_district'] = row['postcode'].partition(' ')[0]
        scraperwiki.sqlite.save(['booking_reference_number'], row)


main()




