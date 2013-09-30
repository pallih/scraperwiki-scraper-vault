import scraperwiki
import xlrd
import lxml.html

def get_policy(root, data):
    try:
        data['policy'] = root.cssselect("div#centerContentContainer a[name='policy9'] ~ p")[0].text_content()
        data['errors'] = 'none'
    except IndexError:
        data['errors'] = 'index error'

def save_data(data, key):
    print scraperwiki.sqlite.save(unique_keys=[key], data=data)   

def scrape_content( src, rownum ):
    html = scraperwiki.scrape(src)
    root = lxml.html.fromstring(html)
    data = dict()
    
    data = {
        'rownum' : rownum,
        'src' : src
    }
    
    get_policy(root, data)
    save_data(data, 'rownum')


def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        src = rows[0]
        scrape_content(src, rownum)
        
#START
#src = 'http://www.starwoodhotels.com/sheraton/property/overview/announcements.html?propertyID=995'
#src = 'http://sanspace.in/pet/set1.xls'
#src = 'http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls'
#get_source(src)
#scrape_content(src, 1)
src = 'http://www.marriott.com/hotels/fact-sheet/travel/atlhg-residence-inn-atlanta-cumberland/'
#src = 'http://www.starwoodhotels.com/sheraton/property/overview/announcements.html?propertyID=350'
scrape_content(src, 2)
import scraperwiki
import xlrd
import lxml.html

def get_policy(root, data):
    try:
        data['policy'] = root.cssselect("div#centerContentContainer a[name='policy9'] ~ p")[0].text_content()
        data['errors'] = 'none'
    except IndexError:
        data['errors'] = 'index error'

def save_data(data, key):
    print scraperwiki.sqlite.save(unique_keys=[key], data=data)   

def scrape_content( src, rownum ):
    html = scraperwiki.scrape(src)
    root = lxml.html.fromstring(html)
    data = dict()
    
    data = {
        'rownum' : rownum,
        'src' : src
    }
    
    get_policy(root, data)
    save_data(data, 'rownum')


def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        src = rows[0]
        scrape_content(src, rownum)
        
#START
#src = 'http://www.starwoodhotels.com/sheraton/property/overview/announcements.html?propertyID=995'
#src = 'http://sanspace.in/pet/set1.xls'
#src = 'http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls'
#get_source(src)
#scrape_content(src, 1)
src = 'http://www.marriott.com/hotels/fact-sheet/travel/atlhg-residence-inn-atlanta-cumberland/'
#src = 'http://www.starwoodhotels.com/sheraton/property/overview/announcements.html?propertyID=350'
scrape_content(src, 2)
