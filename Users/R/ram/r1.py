import scraperwiki
import lxml.html
import xlrd
import re

def scrape_content( url, rownum ):
    hotel_name = 'Empty Hotel Name'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    hotel_name = get_hotelname(root)    
    policy = get_policy(root)    
    
    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : hotel_name,
        'policy' : policy
    }

    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)  

def get_policy(root):
    try:
        for a in root.cssselect('td strong'):
            if ( 'Pet Policy:' in a):
                content= root.cssselect('td').text_content()
                if ( 'Pet Policy:' in content):
                    return content[content.find('Pet Policy:') + 12:]
                else:
                    return 'Empty Policy (Pet policy not in 32)'
            else:
                return'Error'
    except IndexError:
        return 'No Divs'

def get_hotelname(root):
    return root.cssselect('title')[0].text_content()

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
#src = 'http://sanspace.in/pet/set1.xls'
#get_source(src)
url = 'http://book.bestwestern.com/bestwestern/US/CO/Monte-Vista-hotels/BEST-WESTERN-Movie-Manor/Hotel-Overview.do?propertyCode=06029'
scrape_content(url, 4)import scraperwiki
import lxml.html
import xlrd
import re

def scrape_content( url, rownum ):
    hotel_name = 'Empty Hotel Name'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    hotel_name = get_hotelname(root)    
    policy = get_policy(root)    
    
    data = {
        'rownum' : rownum,
        'url' : url,
        'name' : hotel_name,
        'policy' : policy
    }

    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)  

def get_policy(root):
    try:
        for a in root.cssselect('td strong'):
            if ( 'Pet Policy:' in a):
                content= root.cssselect('td').text_content()
                if ( 'Pet Policy:' in content):
                    return content[content.find('Pet Policy:') + 12:]
                else:
                    return 'Empty Policy (Pet policy not in 32)'
            else:
                return'Error'
    except IndexError:
        return 'No Divs'

def get_hotelname(root):
    return root.cssselect('title')[0].text_content()

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
#src = 'http://sanspace.in/pet/set1.xls'
#get_source(src)
url = 'http://book.bestwestern.com/bestwestern/US/CO/Monte-Vista-hotels/BEST-WESTERN-Movie-Manor/Hotel-Overview.do?propertyCode=06029'
scrape_content(url, 4)