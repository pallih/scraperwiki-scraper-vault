import scraperwiki

from bs4 import BeautifulSoup

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

print soup.prettify()

print soup.find_all("table")

print len(soup.find_all("table"))

tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})
print len(tables)

print tables

for table in tables:
    for row in table.find_all('tr'):
        for cell in row.find_all("td"):
            print cell.get_text().strip() 

rows = tables[1].find_all('tr')

for row in rows:
    for cell in row.find_all("td"):
        print cell.get_text().strip()     

for row in rows:
    cells = row.find_all("td")
    print "zero", cells[0]

for row in rows:
    cells = row.find_all("td")
    print "there are", len(cells), "cells in this row"
    print "zero", cells[0]

for row in rows:
    cells = row.find_all("td")
    print "there are", len(cells), "cells in this row"
    if len(cells) > 5:
        print "rank", cells[0].get_text().strip()
        print "state", cells[1].get_text().strip()
        print 'total_filings', cells[2].get_text().strip()
        print '1_per_x' , cells[3].get_text().strip()

for row in rows:
    cells = row.find_all("td")
    if len(cells) > 5:
        data = {
            'rank' : cells[0].get_text().strip(),
            'state' : cells[1].get_text().strip(),
            'total_filings' : cells[2].get_text().strip(),
            '1_per_x' : cells[3].get_text().strip(),
            'change_dec_jan' : cells[4].get_text().strip(),
            'change_jan08' : cells[5].get_text().strip()
        }
        scraperwiki.sqlite.save(unique_keys=['state'],data=data)
