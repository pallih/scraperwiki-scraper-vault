import scraperwiki
import lxml.html
import xlrd
from BeautifulSoup import BeautifulSoup          # For processing HTML

def get_detail (url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    hotel = root.cssselect("input[name='hotel']")[0]
    chain = root.cssselect("input[name='chain']")[0]
    #print chain
    
    soup = BeautifulSoup(html)

    hotel = soup.findAll(attrs={'name':'hotel'})[0]['value']
    chain = soup.findAll(attrs={'name':'chain'})[0]['value']
    return 'https://gc.synxis.com/rez.aspx?hotel=' + hotel + '&chain=' + chain + '&template=ABVI_GCFLX&shell=ABVI_flex&arrive=09-23-2012&depart=09-24-2012&NumberOfRooms=1'      

def scrape_content( url, rownum ):
    dest = get_detail(url)
    data = {
        'rownum' : rownum,
        'input-url' : url,
        'output-url' : dest        
    }
    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        url = rows[1]
        scrape_content(url, rownum)        

#START


#Data source
#src = "http://sanspace.in/pet/set1.xls"
#get_source(src)
url = 'http://www.americasbestvalueinn.com/bestv.cfm?idp=429'
print scrape_content(url, 1)
import scraperwiki
import lxml.html
import xlrd
from BeautifulSoup import BeautifulSoup          # For processing HTML

def get_detail (url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    hotel = root.cssselect("input[name='hotel']")[0]
    chain = root.cssselect("input[name='chain']")[0]
    #print chain
    
    soup = BeautifulSoup(html)

    hotel = soup.findAll(attrs={'name':'hotel'})[0]['value']
    chain = soup.findAll(attrs={'name':'chain'})[0]['value']
    return 'https://gc.synxis.com/rez.aspx?hotel=' + hotel + '&chain=' + chain + '&template=ABVI_GCFLX&shell=ABVI_flex&arrive=09-23-2012&depart=09-24-2012&NumberOfRooms=1'      

def scrape_content( url, rownum ):
    dest = get_detail(url)
    data = {
        'rownum' : rownum,
        'input-url' : url,
        'output-url' : dest        
    }
    print scraperwiki.sqlite.save(unique_keys=['rownum'], data=data)

def get_source( src ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        url = rows[1]
        scrape_content(url, rownum)        

#START


#Data source
#src = "http://sanspace.in/pet/set1.xls"
#get_source(src)
url = 'http://www.americasbestvalueinn.com/bestv.cfm?idp=429'
print scrape_content(url, 1)
