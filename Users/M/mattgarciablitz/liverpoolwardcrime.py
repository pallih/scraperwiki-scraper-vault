import scraperwiki
import xlrd
xlbin = scraperwiki.scrape("http://liverpool.gov.uk/Images/ward_crime.xls")
book = xlrd.open_workbook(file_contents=xlbin)

sheet = book.sheet_by_name('crime')

for n, s in enumerate(book.sheets()):
    print "Sheet %d is called %s and has %d columns and %d rows" % (n, s.name, s.ncols, s.nrows)

#Titles of columns
keys = sheet.row_values(11)
print keys

for rownumber in range(13, sheet.nrows):
    # create dictionary of the row values
    values = [ c for c in sheet.row(rownumber) ]
    print values
    data = dict(zip(keys, values))
    data['rownumber'] = rownumber

    # remove the empty column (which has a blank heading)
    del data['']

    scraperwiki.sqlite.save(unique_keys=['rownumber'], data=data)



