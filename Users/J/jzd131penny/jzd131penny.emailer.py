import scraperwiki
import urllib2
import xlrd
from httplib import BadStatusLine

def save_data(data, key):
    print scraperwiki.sqlite.save(unique_keys=[key], data=data)

def check_string(url, strings):
    if "http" not in url:
        url = 'http://' + url 
    try:
        html = scraperwiki.scrape(url)
    except urllib2.HTTPError, BadStatusLine:
        return "HTTP Error; Check link"
    except:
        return "Unknown error for URL"
    for chkStr in strings:
        if chkStr in html:
            return chkStr
    return "Nothing"

def get_source( src, config ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet, config)

def read_rows(sheet, config): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        src = rows[0]
        scrape_content(src, rownum, config)

def scrape_content(link, num, config):
    res = dict()
    res['id'] = num
    res['src'] = link
    res['res'] = check_string(link, config)
    save_data(res,'id')
    if num == 30: return

urllist = ["www.planethondanj.com/index.htm",
            "http://www.prestigevolvo.com/index.htm",
            "http://www.cherryhilltriplex.com/index.htm",
            "http://www.fsautomall.com/index.htm",
            "http://www.burnshonda.com/index.htm",
            "http://www.shrewsburyvw.com/"] # For testing

config = ["staff", "team"] # Can add more strings here as you wish

#Once excel link is ready comment the below
i = 1
#for link in urllist:
#    scrape_content(link, i, config)
#    i += 1
#Uncomment the below when excel is ready
get_source('http://salemove.com/wp-content/uploads/2013/04/websitestolookup.xls', config)import scraperwiki
import urllib2
import xlrd
from httplib import BadStatusLine

def save_data(data, key):
    print scraperwiki.sqlite.save(unique_keys=[key], data=data)

def check_string(url, strings):
    if "http" not in url:
        url = 'http://' + url 
    try:
        html = scraperwiki.scrape(url)
    except urllib2.HTTPError, BadStatusLine:
        return "HTTP Error; Check link"
    except:
        return "Unknown error for URL"
    for chkStr in strings:
        if chkStr in html:
            return chkStr
    return "Nothing"

def get_source( src, config ): #open excel and get the sheet
    xlbin = scraperwiki.scrape(src)
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    read_rows(sheet, config)

def read_rows(sheet, config): #read each row in the sheet
    for rownum in range(sheet.nrows):
        rows = sheet.row_values(rownum)
        src = rows[0]
        scrape_content(src, rownum, config)

def scrape_content(link, num, config):
    res = dict()
    res['id'] = num
    res['src'] = link
    res['res'] = check_string(link, config)
    save_data(res,'id')
    if num == 30: return

urllist = ["www.planethondanj.com/index.htm",
            "http://www.prestigevolvo.com/index.htm",
            "http://www.cherryhilltriplex.com/index.htm",
            "http://www.fsautomall.com/index.htm",
            "http://www.burnshonda.com/index.htm",
            "http://www.shrewsburyvw.com/"] # For testing

config = ["staff", "team"] # Can add more strings here as you wish

#Once excel link is ready comment the below
i = 1
#for link in urllist:
#    scrape_content(link, i, config)
#    i += 1
#Uncomment the below when excel is ready
get_source('http://salemove.com/wp-content/uploads/2013/04/websitestolookup.xls', config)