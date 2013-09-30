import scraperwiki
import json
import re
import xlrd
import urllib


def get_source( src ): #open excel and get the second sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0) #First sheet in the excel
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        scrape_content(rows[0], rownum) #First column

def scrape_content(q, rnum):
    parm = {
        'cx' : '014212376427772793791:tied54jph3a',
        'key' : 'AIzaSyBYiMH_P-KgXkBRdrqbKxIjU9_fEzW1U6s',
        'num' : 1,
        'q' : q
    }
    data = scraperwiki.scrape('https://www.googleapis.com/customsearch/v1?' + urllib.urlencode(parm))
    res = parse_results(json.loads(data))
    result = {
        'q' : q,
        'res' : res,
        'rnum' : rnum
    }
    print scraperwiki.sqlite.save(unique_keys=['rnum'], data=result)
def parse_results(data):
    if 'items' in data:
        res = data['items'][0]
        url = res['link']
    else:
        url = "Couldn't find URL"
    return url

#START
src = 'http://ramu.bugs3.com/and/and/and.xls'
#Takes input search terms (hotel names) from here
#src = 'http://sanspace.in/pet/set1.xls'
get_source(src)

    
import scraperwiki
import json
import re
import xlrd
import urllib


def get_source( src ): #open excel and get the second sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0) #First sheet in the excel
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        scrape_content(rows[0], rownum) #First column

def scrape_content(q, rnum):
    parm = {
        'cx' : '014212376427772793791:tied54jph3a',
        'key' : 'AIzaSyBYiMH_P-KgXkBRdrqbKxIjU9_fEzW1U6s',
        'num' : 1,
        'q' : q
    }
    data = scraperwiki.scrape('https://www.googleapis.com/customsearch/v1?' + urllib.urlencode(parm))
    res = parse_results(json.loads(data))
    result = {
        'q' : q,
        'res' : res,
        'rnum' : rnum
    }
    print scraperwiki.sqlite.save(unique_keys=['rnum'], data=result)
def parse_results(data):
    if 'items' in data:
        res = data['items'][0]
        url = res['link']
    else:
        url = "Couldn't find URL"
    return url

#START
src = 'http://ramu.bugs3.com/and/and/and.xls'
#Takes input search terms (hotel names) from here
#src = 'http://sanspace.in/pet/set1.xls'
get_source(src)

    
