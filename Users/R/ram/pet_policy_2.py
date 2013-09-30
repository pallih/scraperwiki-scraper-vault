import scraperwiki
import lxml.html
import xlrd

def scrape_content( url, rownum ):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for c in root.cssselect("h1#hotelname"):
        name = c.text_content()
    policy = 'Empty'
    for d in root.cssselect("div#roPetPolicy"):
        policy = d.text_content()
    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : name if name is not None else 'Empty Hotel Name',
        'policy' : policy if policy is not 'Empty' else 'No Pet Policy'
    }
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
        url = rows[0]
        scrape_content(url, rownum)        

#START


#Data source
src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
get_source(src)
import scraperwiki
import lxml.html
import xlrd

def scrape_content( url, rownum ):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for c in root.cssselect("h1#hotelname"):
        name = c.text_content()
    policy = 'Empty'
    for d in root.cssselect("div#roPetPolicy"):
        policy = d.text_content()
    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : name if name is not None else 'Empty Hotel Name',
        'policy' : policy if policy is not 'Empty' else 'No Pet Policy'
    }
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
        url = rows[0]
        scrape_content(url, rownum)        

#START


#Data source
src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
get_source(src)
