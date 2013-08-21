import scraperwiki
import json
import re
import xlrd
import urllib

def valid_url(url):
    return re.compile(r'\w*/services$').search(url)

def get_source( src ): #open excel and get the second sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(1) #Second sheet in the excel
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        scrape_content(rows[1], rownum) #second column

def scrape_content(q, rnum):
    parm = {
        'cx' : '014212376427772793791:aygfardeqhc',
        'key' : 'AIzaSyASbUdSobqdfnjVPqHeqkzPyfYNY1R7hJs',
        'num' : 3,
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
        for res in data['items']:
            url = res['link']
            if valid_url(url):
                print url
                break
    else:
        url = "Couldn't find URL"
    
    return url

#START
src = 'http://sanspace.in/pet/set1.xls'  #Takes input search terms (hotel names) from here
get_source(src)