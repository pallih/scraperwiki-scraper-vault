import scraperwiki
import scraperwiki
import json
import re
import xlrd
import urllib
import lxml.html
from BeautifulSoup import BeautifulSoup          # For processing HTML


def get_source( src ): #open excel and get the second sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0) #Second sheet in the excel
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        get_detail(rows[0], rownum) #First column

def get_detail (url, rnum):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    hotel = root.cssselect("input[name='hotel']")[0]
    chain = root.cssselect("input[name='chain']")[0]
    #print chain
    
    soup = BeautifulSoup(html)
    #for el in soup.findAll('input'):
        #print el['value']
    hotel = soup.findAll(attrs={'name':'hotel'})[0]['value']
    chain = soup.findAll(attrs={'name':'chain'})[0]['value']
    myurl = 'https://gc.synxis.com/rez.aspx?hotel=' + hotel + '&chain=' + chain + '&template=ABVI_GCFLX&shell=ABVI_flex&arrive=09-23-2012&depart=09-24-2012&NumberOfRooms=1'        
    pet = {
        'url' : myurl,
        'rnum' : int(rnum)
        }
    print scraperwiki.sqlite.save(unique_keys=['rnum'], data=pet)

src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
get_source(src)import scraperwiki
import scraperwiki
import json
import re
import xlrd
import urllib
import lxml.html
from BeautifulSoup import BeautifulSoup          # For processing HTML


def get_source( src ): #open excel and get the second sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0) #Second sheet in the excel
    read_rows(sheet)

def read_rows(sheet): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        get_detail(rows[0], rownum) #First column

def get_detail (url, rnum):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    hotel = root.cssselect("input[name='hotel']")[0]
    chain = root.cssselect("input[name='chain']")[0]
    #print chain
    
    soup = BeautifulSoup(html)
    #for el in soup.findAll('input'):
        #print el['value']
    hotel = soup.findAll(attrs={'name':'hotel'})[0]['value']
    chain = soup.findAll(attrs={'name':'chain'})[0]['value']
    myurl = 'https://gc.synxis.com/rez.aspx?hotel=' + hotel + '&chain=' + chain + '&template=ABVI_GCFLX&shell=ABVI_flex&arrive=09-23-2012&depart=09-24-2012&NumberOfRooms=1'        
    pet = {
        'url' : myurl,
        'rnum' : int(rnum)
        }
    print scraperwiki.sqlite.save(unique_keys=['rnum'], data=pet)

src = "http://www.weebly.com/uploads/1/1/0/3/1103525/set1.xls"
get_source(src)