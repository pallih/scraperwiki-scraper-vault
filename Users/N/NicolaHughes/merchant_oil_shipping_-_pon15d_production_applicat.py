import scraperwiki
import xlrd    
import re
import urllib2
import datetime


url = 'https://www.og.decc.gov.uk/environment/Website_PON15D_Apps.xls'

contents = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=contents)
sheet = book.sheet_by_index(0)
                      
headings = [ sheet.cell(0, col).value  for col in range(sheet.ncols) ]
assert headings == ['Company Name', 'Host Discharging Installation', 'Tie-Backs to Host', 'DTI Ref', 'Received Date', 'Chemical Permit Issued', 'EIA Direction Issued'], headings


def ConvValue(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        dm = xlrd.xldate_as_tuple(cell.value, book.datemode)
        return datetime.date(dm[0], dm[1], dm[2])
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        assert not cell.value
        return None
    return cell.value.strip()

for row in range(2, sheet.nrows):
    values = [ ConvValue(sheet.cell(row, col))  for col in range(sheet.ncols) ]
    data = dict(zip(headings, values))
    mcname = re.match("(.*?)\s*\(\s*(?:was|previously)\s*(.*?)\)$", data["Company Name"])
    if mcname:
        data["Company Name"] = mcname.group(1)
        data["Was Company Name"] = mcname.group(2)
    scraperwiki.sqlite.save(unique_keys=['DTI Ref'], data=data)
    
                              


import scraperwiki
import xlrd    
import re
import urllib2
import datetime


url = 'https://www.og.decc.gov.uk/environment/Website_PON15D_Apps.xls'

contents = urllib2.urlopen(url).read()
book = xlrd.open_workbook(file_contents=contents)
sheet = book.sheet_by_index(0)
                      
headings = [ sheet.cell(0, col).value  for col in range(sheet.ncols) ]
assert headings == ['Company Name', 'Host Discharging Installation', 'Tie-Backs to Host', 'DTI Ref', 'Received Date', 'Chemical Permit Issued', 'EIA Direction Issued'], headings


def ConvValue(cell):
    if cell.ctype == xlrd.XL_CELL_DATE:
        dm = xlrd.xldate_as_tuple(cell.value, book.datemode)
        return datetime.date(dm[0], dm[1], dm[2])
    if cell.ctype == xlrd.XL_CELL_EMPTY:
        assert not cell.value
        return None
    return cell.value.strip()

for row in range(2, sheet.nrows):
    values = [ ConvValue(sheet.cell(row, col))  for col in range(sheet.ncols) ]
    data = dict(zip(headings, values))
    mcname = re.match("(.*?)\s*\(\s*(?:was|previously)\s*(.*?)\)$", data["Company Name"])
    if mcname:
        data["Company Name"] = mcname.group(1)
        data["Was Company Name"] = mcname.group(2)
    scraperwiki.sqlite.save(unique_keys=['DTI Ref'], data=data)
    
                              


