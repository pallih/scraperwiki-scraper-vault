import scraperwiki
import xlrd
import re

scraperwiki.cache(False)

url = "http://customs.hmrc.gov.uk/channelsPortalWebApp/downloadFile?contentID=HMCE_PROD_009941&rendition=nativeFile"

# This is the register kept for the purpose of administering the Landfill Tax
# See links at bottom

book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

# We can loop over each 
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can access each worksheet by it's index
sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
print headings
assert headings == [u'Registration Number', u'Operator Name', 
                    u'Site Address 1', u'Site Address 2', u'Site Address 3', u'Site Address 4', 
                    u'Site County', u'Site Country', u'Site Post Code']
for irow in range(1, sheet.nrows):
    row = [ sheet.cell(irow, i).value  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    salist = [ data.pop(u'Site Address %d'%sai)  for sai in range(1, 5) ]
    salist = filter(None, salist)
    data[u'Site Address'] = ', '.join(salist)
    latlng = scraperwiki.geo.gb_postcode_to_latlng(data[u'Site Post Code'])
          
    colour = 'ffffff'
    if re.search('Quarry', data[u'Site Address']):
        colour = '00ff00'
    if re.search('Landfill', data[u'Site Address']):
        colour = '0000ff'
    data['colour'] = colour
    scraperwiki.datastore.save(unique_keys=['Site Address', 'Site Post Code'], data=data, latlng=latlng)
    


#ctypes:
#    XL_CELL_BLANK = 6
#    XL_CELL_BOOLEAN = 4
#    XL_CELL_DATE = 3
#    XL_CELL_EMPTY = 0
#    XL_CELL_ERROR = 5
#    XL_CELL_NUMBER = 2
#    XL_CELL_TEXT = 1

# Sections in the Finance Act 1996 here:
# http://www.statutelaw.gov.uk/legResults.aspx?LegType=All+Legislation&title=Finance+Act&searchEnacted=0&extentMatchOnly=0&confersPower=0&blanketAmendment=0&sortAlpha=0&PageNumber=4&NavFrom=0&activeTextDocId=2378315
    
# holding page: http://customs.hmrc.gov.uk/channelsPortalWebApp/channelsPortalWebApp.portal?_nfpb=true&_pageLabel=pageExcise_ShowContent&id=HMCE_PROD_009941&propertyType=document

import scraperwiki
import xlrd
import re

scraperwiki.cache(False)

url = "http://customs.hmrc.gov.uk/channelsPortalWebApp/downloadFile?contentID=HMCE_PROD_009941&rendition=nativeFile"

# This is the register kept for the purpose of administering the Landfill Tax
# See links at bottom

book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

# We can loop over each 
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can access each worksheet by it's index
sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
print headings
assert headings == [u'Registration Number', u'Operator Name', 
                    u'Site Address 1', u'Site Address 2', u'Site Address 3', u'Site Address 4', 
                    u'Site County', u'Site Country', u'Site Post Code']
for irow in range(1, sheet.nrows):
    row = [ sheet.cell(irow, i).value  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    salist = [ data.pop(u'Site Address %d'%sai)  for sai in range(1, 5) ]
    salist = filter(None, salist)
    data[u'Site Address'] = ', '.join(salist)
    latlng = scraperwiki.geo.gb_postcode_to_latlng(data[u'Site Post Code'])
          
    colour = 'ffffff'
    if re.search('Quarry', data[u'Site Address']):
        colour = '00ff00'
    if re.search('Landfill', data[u'Site Address']):
        colour = '0000ff'
    data['colour'] = colour
    scraperwiki.datastore.save(unique_keys=['Site Address', 'Site Post Code'], data=data, latlng=latlng)
    


#ctypes:
#    XL_CELL_BLANK = 6
#    XL_CELL_BOOLEAN = 4
#    XL_CELL_DATE = 3
#    XL_CELL_EMPTY = 0
#    XL_CELL_ERROR = 5
#    XL_CELL_NUMBER = 2
#    XL_CELL_TEXT = 1

# Sections in the Finance Act 1996 here:
# http://www.statutelaw.gov.uk/legResults.aspx?LegType=All+Legislation&title=Finance+Act&searchEnacted=0&extentMatchOnly=0&confersPower=0&blanketAmendment=0&sortAlpha=0&PageNumber=4&NavFrom=0&activeTextDocId=2378315
    
# holding page: http://customs.hmrc.gov.uk/channelsPortalWebApp/channelsPortalWebApp.portal?_nfpb=true&_pageLabel=pageExcise_ShowContent&id=HMCE_PROD_009941&propertyType=document

import scraperwiki
import xlrd
import re

scraperwiki.cache(False)

url = "http://customs.hmrc.gov.uk/channelsPortalWebApp/downloadFile?contentID=HMCE_PROD_009941&rendition=nativeFile"

# This is the register kept for the purpose of administering the Landfill Tax
# See links at bottom

book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

# We can loop over each 
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can access each worksheet by it's index
sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
print headings
assert headings == [u'Registration Number', u'Operator Name', 
                    u'Site Address 1', u'Site Address 2', u'Site Address 3', u'Site Address 4', 
                    u'Site County', u'Site Country', u'Site Post Code']
for irow in range(1, sheet.nrows):
    row = [ sheet.cell(irow, i).value  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    salist = [ data.pop(u'Site Address %d'%sai)  for sai in range(1, 5) ]
    salist = filter(None, salist)
    data[u'Site Address'] = ', '.join(salist)
    latlng = scraperwiki.geo.gb_postcode_to_latlng(data[u'Site Post Code'])
          
    colour = 'ffffff'
    if re.search('Quarry', data[u'Site Address']):
        colour = '00ff00'
    if re.search('Landfill', data[u'Site Address']):
        colour = '0000ff'
    data['colour'] = colour
    scraperwiki.datastore.save(unique_keys=['Site Address', 'Site Post Code'], data=data, latlng=latlng)
    


#ctypes:
#    XL_CELL_BLANK = 6
#    XL_CELL_BOOLEAN = 4
#    XL_CELL_DATE = 3
#    XL_CELL_EMPTY = 0
#    XL_CELL_ERROR = 5
#    XL_CELL_NUMBER = 2
#    XL_CELL_TEXT = 1

# Sections in the Finance Act 1996 here:
# http://www.statutelaw.gov.uk/legResults.aspx?LegType=All+Legislation&title=Finance+Act&searchEnacted=0&extentMatchOnly=0&confersPower=0&blanketAmendment=0&sortAlpha=0&PageNumber=4&NavFrom=0&activeTextDocId=2378315
    
# holding page: http://customs.hmrc.gov.uk/channelsPortalWebApp/channelsPortalWebApp.portal?_nfpb=true&_pageLabel=pageExcise_ShowContent&id=HMCE_PROD_009941&propertyType=document

import scraperwiki
import xlrd
import re

scraperwiki.cache(False)

url = "http://customs.hmrc.gov.uk/channelsPortalWebApp/downloadFile?contentID=HMCE_PROD_009941&rendition=nativeFile"

# This is the register kept for the purpose of administering the Landfill Tax
# See links at bottom

book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url))

# We can find out information about the workbook
print "Workbook has %s sheet(s)" % book.nsheets

# We can loop over each 
for sheet in book.sheets():
    print "Sheet called %s has %s rows and %s columns" %(sheet.name,sheet.nrows,sheet.ncols)

# You can access each worksheet by it's index
sheet = book.sheet_by_index(0)
headings = [ sheet.cell(0, i).value  for i in range(sheet.ncols) ]
print headings
assert headings == [u'Registration Number', u'Operator Name', 
                    u'Site Address 1', u'Site Address 2', u'Site Address 3', u'Site Address 4', 
                    u'Site County', u'Site Country', u'Site Post Code']
for irow in range(1, sheet.nrows):
    row = [ sheet.cell(irow, i).value  for i in range(sheet.ncols) ]
    data = dict(zip(headings, row))
    salist = [ data.pop(u'Site Address %d'%sai)  for sai in range(1, 5) ]
    salist = filter(None, salist)
    data[u'Site Address'] = ', '.join(salist)
    latlng = scraperwiki.geo.gb_postcode_to_latlng(data[u'Site Post Code'])
          
    colour = 'ffffff'
    if re.search('Quarry', data[u'Site Address']):
        colour = '00ff00'
    if re.search('Landfill', data[u'Site Address']):
        colour = '0000ff'
    data['colour'] = colour
    scraperwiki.datastore.save(unique_keys=['Site Address', 'Site Post Code'], data=data, latlng=latlng)
    


#ctypes:
#    XL_CELL_BLANK = 6
#    XL_CELL_BOOLEAN = 4
#    XL_CELL_DATE = 3
#    XL_CELL_EMPTY = 0
#    XL_CELL_ERROR = 5
#    XL_CELL_NUMBER = 2
#    XL_CELL_TEXT = 1

# Sections in the Finance Act 1996 here:
# http://www.statutelaw.gov.uk/legResults.aspx?LegType=All+Legislation&title=Finance+Act&searchEnacted=0&extentMatchOnly=0&confersPower=0&blanketAmendment=0&sortAlpha=0&PageNumber=4&NavFrom=0&activeTextDocId=2378315
    
# holding page: http://customs.hmrc.gov.uk/channelsPortalWebApp/channelsPortalWebApp.portal?_nfpb=true&_pageLabel=pageExcise_ShowContent&id=HMCE_PROD_009941&propertyType=document

