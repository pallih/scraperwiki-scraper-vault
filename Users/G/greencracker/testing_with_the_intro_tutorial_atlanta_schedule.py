import scraperwiki
html = scraperwiki.scrape("http://www.justice.gov/crt/about/vot/notices/noticepg.php")
import lxml.html
import xlrd
import time
from BeautifulSoup import BeautifulSoup, SoupStrainer 
import re 
import urllib 

full_url = "http://www.justice.gov/crt/about/vot/notices/noticepg.php"
html = urllib.urlopen(full_url).read() 
handle = "http://www.justice.gov/crt/about/vot/notices/"
soup = BeautifulSoup(html) 
soup = soup.prettify() 

m = re.findall('vnote+.+.xls', soup)

counter = 0
for item in m:
    time.sleep(10)
    xlbin = scraperwiki.scrape(handle + m[counter])
    #print m[counter]
    #print handle + m[counter]
    counter = counter + 1
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    for rownum in range (39,sheet.nrows):
        data = {
        'key' : m[counter] + str(rownum),
        'subjuris' : sheet.cell(rownum,6),
        'county' : sheet.cell(rownum, 3),
        'post_date' : m[counter],
        'state' : sheet.cell(rownum, 0),
        'submssion_no' : sheet.cell(rownum, 10),
        'action_date' : sheet.cell(rownum, 14),
        'action' : sheet.cell(rownum, 17),
        'changes' : sheet.cell(rownum, 24),
        'comments' : sheet.cell(rownum, 30),
        }
        #print data
        
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)



