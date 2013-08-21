import scraperwiki
import xlrd
import lxml.html

def get_policy(root, data):
    try:
        div = root.cssselect('div.facts-container')[1]
        el = div.cssselect('div.column')[1]
        li = el.cssselect('li')[-1]
        data['policy'] = li.text_content().strip()
        data['valid-policy'] = el.cssselect('h4')[-1].text_content()
        data['errors'] = 'none'

    except IndexError:
        data['errors'] = 'index error'

def save_data(data, key):
    print scraperwiki.sqlite.save(unique_keys=[key], data=data)   

def scrape_content( src, rownum ):
    html = scraperwiki.scrape(src)
    root = lxml.html.fromstring(html)
       
    data = {
        'rownum' : rownum,
        'url' : url
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
        src= rows[0]
        scrape_content(src, rownum)
        
#START
#src = 'http://www.marriott.com/hotels/fact-sheet/travel/atlhg-residence-inn-atlanta-cumberland/'
#src = 'http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls'
src = 'http://sanspace.in/pet/set1.xls'
get_source(src)
#scrape_content(src, 1)
