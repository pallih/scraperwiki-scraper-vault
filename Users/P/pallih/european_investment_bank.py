import scraperwiki
import lxml.html
import re
import xlrd
import datetime
import urllib

regions=['european-union', 'efta', 'enlargement', 'cei', 'mediterranean-countries', 'acp', 'south-africa', 'ala']

'''
oldtables = ['loans_by_regions(south-africa)_1959_2011','loans_by_regions(ala)_1959_2011','loans_by_regions(european-union)_1959_2011','loans_by_regions_1959_2011','loans_by_regions(mediterranean-countries)_1959_2011','loans_by_regions(acp)_1959_2011','loans_by_regions(cei)_1959_2011','loans_by_regions(enlargement)_1959_2011','loans_by_regions(efta)_1959_2011','loans_by_sectors_1959_2011','loans_all_countries_1959_2011']
#clean
for table in oldtables:
    statement = 'drop table if exists "' + table +'"'
    scraperwiki.sqlite.execute(statement)
    scraperwiki.sqlite.commit()
exit()

'''

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

def get_by_years(query,start,end):
    sectors_url = 'http://www.eib.org/projects/loans/'+query+'/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(1, sheet.nrows):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data[query] = values[0]
        data['amount'] = values[1]
        #print data
        scraperwiki.sqlite.save([query], data=data, table_name='loans_by_'+query+'_1959_2012')

def get_by_regions(region,start,end):
    sectors_url = 'http://www.eib.org/projects/loans/regions/'+region+'/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(1, sheet.nrows-1):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data['country'] = values[0]
        data['amount'] = values[1]
        #print data
        scraperwiki.sqlite.save(['country'], data=data, table_name='loans_by_regions('+region+')_1959_2012')
        scraperwiki.sqlite.save(['country'], data=data, table_name='loans_all_countries_1959_2012')

def process_financed_projects(start,end):
    sectors_url = 'http://www.eib.org/projects/loans/list/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(6, sheet.nrows-1):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data['name'] = values[0]
        data['region'] = values[1]
        data['country'] = values[2]
        data['sector'] = values[3]
        data['sign_date'] = values[4]
        data['signed_amount'] = values[5]
        data['description'] = values[6]
        data['rownumber_id'] = rownumber
        #print data
        scraperwiki.sqlite.save(['name','description','signed_amount','sign_date','country', 'rownumber_id'], data=data, table_name='financed_projects')

def process_projects_to_be_financed(start,end):
    sectors_url = 'http://www.eib.org/projects/pipeline/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(7, sheet.nrows):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data['entry_date'] = values[0]
        data['name'] = values[1]
        data['country'] = values[2]
        data['sector'] = values[3]
        data['status'] = values[4]
        data['rownumber_id'] = rownumber
        #print data
        scraperwiki.sqlite.save(['name','entry_date','country','sector','rownumber_id'], data=data, table_name='projects_to_be_financed')


### START




### Get sectors and regions from 1959-2012 ###

get_by_years('sectors',1959,2012)
print 'Processed sectors 1959-2012'
get_by_years('regions',1959,2012)
print 'Processed regions 1959-2012'

###--###


### Get projects to be financed up until (and including) 2012 ###

process_projects_to_be_financed(2001,2012)
print 'Processed projects to be financed 2001-2012'

###--###


### Get financed projects from 2011-2012 - Older ones are already in the db ###

process_financed_projects(2011,2012)
print 'Processed financed projects 1959-2012'

###--###

### Get Regions breakdown (and populate all countries table)

for region in regions:
    get_by_regions(region,1959,2012)


print 'Processed individual regions and all countries tables'
    
###--###
import scraperwiki
import lxml.html
import re
import xlrd
import datetime
import urllib

regions=['european-union', 'efta', 'enlargement', 'cei', 'mediterranean-countries', 'acp', 'south-africa', 'ala']

'''
oldtables = ['loans_by_regions(south-africa)_1959_2011','loans_by_regions(ala)_1959_2011','loans_by_regions(european-union)_1959_2011','loans_by_regions_1959_2011','loans_by_regions(mediterranean-countries)_1959_2011','loans_by_regions(acp)_1959_2011','loans_by_regions(cei)_1959_2011','loans_by_regions(enlargement)_1959_2011','loans_by_regions(efta)_1959_2011','loans_by_sectors_1959_2011','loans_all_countries_1959_2011']
#clean
for table in oldtables:
    statement = 'drop table if exists "' + table +'"'
    scraperwiki.sqlite.execute(statement)
    scraperwiki.sqlite.commit()
exit()

'''

def cellval(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        datetuple = xlrd.xldate_as_tuple(cell.value, datemode)
        if datetuple[3:] == (0, 0, 0):
            return datetime.date(datetuple[0], datetuple[1], datetuple[2])
        return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    if cell.ctype == xlrd.XL_CELL_BOOLEAN:  return cell.value == 1
    return cell.value

def get_by_years(query,start,end):
    sectors_url = 'http://www.eib.org/projects/loans/'+query+'/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(1, sheet.nrows):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data[query] = values[0]
        data['amount'] = values[1]
        #print data
        scraperwiki.sqlite.save([query], data=data, table_name='loans_by_'+query+'_1959_2012')

def get_by_regions(region,start,end):
    sectors_url = 'http://www.eib.org/projects/loans/regions/'+region+'/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(1, sheet.nrows-1):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data['country'] = values[0]
        data['amount'] = values[1]
        #print data
        scraperwiki.sqlite.save(['country'], data=data, table_name='loans_by_regions('+region+')_1959_2012')
        scraperwiki.sqlite.save(['country'], data=data, table_name='loans_all_countries_1959_2012')

def process_financed_projects(start,end):
    sectors_url = 'http://www.eib.org/projects/loans/list/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(6, sheet.nrows-1):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data['name'] = values[0]
        data['region'] = values[1]
        data['country'] = values[2]
        data['sector'] = values[3]
        data['sign_date'] = values[4]
        data['signed_amount'] = values[5]
        data['description'] = values[6]
        data['rownumber_id'] = rownumber
        #print data
        scraperwiki.sqlite.save(['name','description','signed_amount','sign_date','country', 'rownumber_id'], data=data, table_name='financed_projects')

def process_projects_to_be_financed(start,end):
    sectors_url = 'http://www.eib.org/projects/pipeline/index.xls?start='+str(start)+'&end='+str(end)
    book = xlrd.open_workbook(file_contents=urllib.urlopen(sectors_url).read())
    for n, sheet in enumerate(book.sheets()):
        pass
    keys = sheet.row_values(0)
    for rownumber in range(7, sheet.nrows):
        data = {}
        values = [ cellval(sheet.cell(rownumber, j), book.datemode)  for j in range(sheet.ncols) ]
        data['entry_date'] = values[0]
        data['name'] = values[1]
        data['country'] = values[2]
        data['sector'] = values[3]
        data['status'] = values[4]
        data['rownumber_id'] = rownumber
        #print data
        scraperwiki.sqlite.save(['name','entry_date','country','sector','rownumber_id'], data=data, table_name='projects_to_be_financed')


### START




### Get sectors and regions from 1959-2012 ###

get_by_years('sectors',1959,2012)
print 'Processed sectors 1959-2012'
get_by_years('regions',1959,2012)
print 'Processed regions 1959-2012'

###--###


### Get projects to be financed up until (and including) 2012 ###

process_projects_to_be_financed(2001,2012)
print 'Processed projects to be financed 2001-2012'

###--###


### Get financed projects from 2011-2012 - Older ones are already in the db ###

process_financed_projects(2011,2012)
print 'Processed financed projects 1959-2012'

###--###

### Get Regions breakdown (and populate all countries table)

for region in regions:
    get_by_regions(region,1959,2012)


print 'Processed individual regions and all countries tables'
    
###--###
