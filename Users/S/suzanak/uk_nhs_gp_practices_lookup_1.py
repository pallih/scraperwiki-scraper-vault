import scraperwiki
import xlrd


#cribbing https://scraperwiki.com/docs/python/python_excel_guide/
def cellval(cell):
    if cell.ctype == xlrd.XL_CELL_EMPTY:    return None
    return cell.value

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass

def reGrabber():
    #dropper('GPpracticeLookup')
    url='https://indicators.ic.nhs.uk/download/GP%20Practice%20data/summaries/demography/Practice%20Addresses%20Final.xls'

    xlbin = scraperwiki.scrape(url)
    book = xlrd.open_workbook(file_contents=xlbin)

    sheet = book.sheet_by_index(0)        

    keys = sheet.row_values(8)           
    keys[1] = keys[1].replace('.', '')
    print keys

    for rownumber in range(9, sheet.nrows):           
        # create dictionary of the row values
        values = [ cellval(c) for c in sheet.row(rownumber) ]
        data = dict(zip(keys, values))
        #print data
        scraperwiki.sqlite.save(table_name='GPpracticeLookup',unique_keys=['Practice Code'], data=data)

#Uncomment the next line if you want to regrab the data from the original spreadsheet
#reGrabber()