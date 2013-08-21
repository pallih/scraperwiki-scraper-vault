import scraperwiki           
import lxml.html
import re
from BeautifulSoup import BeautifulSoup

yearStart = 1997
urls = [
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/ministries11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/legassembly11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/judiciary11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/crown11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/electric11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/munic11a.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/munic11b.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/schbd11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/univer11a.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/univer11b.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/colleg11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/hospit11.html',
'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/otherp11.html'
#,'http://www.fin.gov.on.ca/en/publications/salarydisclosure/2011/nosal11.html'
]

for x in range(0,15):
    r = 0; #db_key resets at the start of each table
    src = urls[x]
    tableName = 'sunshineTb%d-%s' % (yearStart,x)
    html = scraperwiki.scrape(src) 
    soup = BeautifulSoup(html)    
    table = soup.findAll('table')[0]
    for row in table.findAll('tr')[1:]:
        r = r+1
        col = row.findAll('td')
        data = {
        '_db_key':r,
        'employer':col[0].getText(),
        'surname':col[1].getText(),
        'givenName':col[2].getText(),
        'position':col[3].getText(),
        'salaryPaid':col[4].getText(),
        'taxableBenefits':col[5].getText()
        }
        scraperwiki.sqlite.save(unique_keys=["_db_key"], data=data, table_name=tableName, verbose=2)
    yearStart = yearStart + 1