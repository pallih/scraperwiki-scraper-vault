import scraperwiki
import lxml.html
import xlrd
import re


def parse_content(root):
    counter = 0
    for elem in root.cssselect("td:contains('Pet Policy:')"):
        counter += 1
        tag = elem.cssselect('strong')[0]
        if (tag.text_content() == 'Pet Policy:'):
            content = elem.text_content()
            print content[content.find('Pet Policy:') + 12:].strip()
            return content[content.find('Pet Policy:') + 12:]
    print counter        
        

def get_hotelname(root):
    return root.cssselect('title')[0].text_content()

def scrape_content( url, rownum ):
    hotel_name = 'Empty Hotel Name'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    hotel_name = get_hotelname(root)    
    policy = parse_content(root)    
    
    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : hotel_name,
        'policy' : policy
    }

    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)    

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(1)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        url = rows[0]
        scrape_content(url, rownum)        

#START


#Data source
src = 'http://sanspace.in/pet/set1.xls'
get_source(src)
#url = 'http://book.bestwestern.com/bestwestern/productInfo.do?propertyCode=37084&disablenav=true&language=en_US'
#scrape_content(url, 4)import scraperwiki
import lxml.html
import xlrd
import re


def parse_content(root):
    counter = 0
    for elem in root.cssselect("td:contains('Pet Policy:')"):
        counter += 1
        tag = elem.cssselect('strong')[0]
        if (tag.text_content() == 'Pet Policy:'):
            content = elem.text_content()
            print content[content.find('Pet Policy:') + 12:].strip()
            return content[content.find('Pet Policy:') + 12:]
    print counter        
        

def get_hotelname(root):
    return root.cssselect('title')[0].text_content()

def scrape_content( url, rownum ):
    hotel_name = 'Empty Hotel Name'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    hotel_name = get_hotelname(root)    
    policy = parse_content(root)    
    
    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : hotel_name,
        'policy' : policy
    }

    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)    

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(1)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        url = rows[0]
        scrape_content(url, rownum)        

#START


#Data source
src = 'http://sanspace.in/pet/set1.xls'
get_source(src)
#url = 'http://book.bestwestern.com/bestwestern/productInfo.do?propertyCode=37084&disablenav=true&language=en_US'
#scrape_content(url, 4)