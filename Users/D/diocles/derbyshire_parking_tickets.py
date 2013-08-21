import scraperwiki
import xlrd
import urllib
import datetime


def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        if datetuple[:3] == (0, 0, 0):
            return datetime.time(datetuple[3], datetuple[4], datetuple[5])
        # Possible floating-point error?
        return datetime.date(datetuple[0], datetuple[1], datetuple[2])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

surl = 'http://www.whatdotheyknow.com/request/72330/response/187170/attach/5/foi%20derbyshire.xls'
book = xlrd.open_workbook(file_contents=urllib.urlopen(surl).read())

for n, sheet in enumerate(book.sheets()):
    print "Sheet %d has %d columns and %d rows" % (n, sheet.ncols, sheet.nrows)

keys = sheet.row_values(0)

# Replace the last two column headers.
keys.pop()
keys.pop()
keys.append("Date Paid")
keys.append("Payment Method")

result = scraperwiki.sqlite.select("max(rownumber) as max from swdata")
max = result[0]["max"]

for rownumber in range(max + 1, sheet.nrows):
    values = [ cellval(sheet.cell(rownumber, j), book.datemode) for j in range(sheet.ncols) ]
    data = dict(zip(keys, values))

    # Set the time to midnight if it is missing.
    if data["Time"] == None:
        data["Time"] = datetime.time(0,0,0)

    data["Date Issued"] = datetime.datetime.combine(data["Issue Date"], data["Time"])

    del data["Time"]
    del data["Issue Date"]

    data["rownumber"] = rownumber
    scraperwiki.sqlite.save(unique_keys=["rownumber"], data=data)