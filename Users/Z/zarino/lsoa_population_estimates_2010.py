import scraperwiki
import requests
import tempfile, zipfile
import xlrd
import os


def cellval(cell, datemode):
    # handy function for working with excel cells
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value


def download_xls():
    print 'Downloading zip file from ONS...'
    print '-- creating temp file'
    t = tempfile.NamedTemporaryFile(suffix=".zip")
    
    print '-- downloading zip'
    t.write(requests.get('http://www.ons.gov.uk/ons/rel/sape/soa-mid-year-pop-est-engl-wales-exp/mid-2010-release/rft---mid-2010-lsoa-population-estimates.zip', verify=False).content)
    t.seek(0)
    
    print '-- unzipping'
    z = zipfile.ZipFile(t.name)
    contents = z.namelist()

    print '-- saving file "' + contents[0] + '" to local storage'
    z.extract('mid_2010_lsoa_broad_est.xls')


def extract_data_from_xls():
    print 'Reading xls file...'
    bin = open(os.getcwd() + '/mid_2010_lsoa_broad_est.xls', 'r').read()
    book = xlrd.open_workbook(file_contents=bin)
    for n, s in enumerate(book.sheets()):
        print "-- sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

    extract_data_from_sheet(book, 1, 'Persons')
    extract_data_from_sheet(book, 2, 'Males')
    extract_data_from_sheet(book, 3, 'Females')

def extract_data_from_sheet(book, num, name):
    print 'Extracting data from sheet: ' + name + '...'
    sheet = book.sheet_by_index(num)

    keys = []
    for key in sheet.row_values(3):
        keys.append(key.replace(' ', '_').replace('+','-plus').lower())

    i = 0
    data = []
    for n in range(4, sheet.nrows):
        values = [ cellval(c, book.datemode) for c in sheet.row(n) ]
        data.append(dict(zip(keys, values)))
        i += 1
    print '-- extracted %s rows from spreadsheet' % i

    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `%s` (`%s` TEXT PRIMARY KEY, `%s` TEXT, `%s` INTEGER, `%s` INTEGER, `%s` INTEGER, `%s` INTEGER, `%s` INTEGER, `%s` INTEGER)' % (name.lower(), keys[0], keys[1], keys[2], keys[3], keys[4], keys[5], keys[6], keys[7]))
    scraperwiki.sqlite.commit()
    scraperwiki.sqlite.save([keys[0]], data, name.lower())
    print '-- saved %s rows to database' % i


download_xls()
extract_data_from_xls()