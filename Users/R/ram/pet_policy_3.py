import scraperwiki
import lxml.html
import xlrd
import urllib2

def scrape_content( data ):
    try:
        html = scraperwiki.scrape(data['url'])
    except urllib2.HTTPError: # Handling 404
        data['name'] = 'Not Found URL'
        data['policy'] = 'Page Not Found'
        print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)
        return
    root = lxml.html.fromstring(html)
    for c in root.cssselect("h1#hotelname"):
        name = c.text_content()
    policy = 'Empty'
    for d in root.cssselect("div#roPetPolicy"):
        policy = d.text_content()
    data['name'] = name if name is not None else 'Empty Hotel Name'
    data['policy'] = policy if policy is not 'Empty' else 'No Pet Policy'
    
    #print name
    if name is not None:
        print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        data = dict()
        data['url'] = rows[0]
        data['rownum'] = rownum
        scrape_content(data)        


#START


#Data source
src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
get_source(src)
#data = dict()
#data['url'] = 'http://www.ichotelsgroup.com/ihg/hotels/fr/fr/malvern/vmvpa/hoteldetail'
#data['rownum'] = 1
#scrape_content(data)
import scraperwiki
import lxml.html
import xlrd
import urllib2

def scrape_content( data ):
    try:
        html = scraperwiki.scrape(data['url'])
    except urllib2.HTTPError: # Handling 404
        data['name'] = 'Not Found URL'
        data['policy'] = 'Page Not Found'
        print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)
        return
    root = lxml.html.fromstring(html)
    for c in root.cssselect("h1#hotelname"):
        name = c.text_content()
    policy = 'Empty'
    for d in root.cssselect("div#roPetPolicy"):
        policy = d.text_content()
    data['name'] = name if name is not None else 'Empty Hotel Name'
    data['policy'] = policy if policy is not 'Empty' else 'No Pet Policy'
    
    #print name
    if name is not None:
        print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        data = dict()
        data['url'] = rows[0]
        data['rownum'] = rownum
        scrape_content(data)        


#START


#Data source
src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
get_source(src)
#data = dict()
#data['url'] = 'http://www.ichotelsgroup.com/ihg/hotels/fr/fr/malvern/vmvpa/hoteldetail'
#data['rownum'] = 1
#scrape_content(data)
