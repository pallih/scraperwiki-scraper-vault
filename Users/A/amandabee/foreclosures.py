import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

## start simple
#print soup.find_all("table")

## how many tables did that find?

#print len(soup.find_all("table"))

# not simple enough. So use the element inspector to confirm that we want a table with <table border="0" cellspacing="1" cellpadding="2">

tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})
print len(tables)

## That is a much more manageable number. So let's take a look at what we got:
# print tables

## Okay, so now let's get fancy:

for row in tables[1].find_all('tr'):
    for cell in row.find_all("td"):
        ## show this first without the "strip()"
        print cell.get_text().strip() 
        
## Let's find our header row:

rows = tables[1].find_all('tr')

i = 0
for cell in rows[0].find_all("td"):
    print i,":", cell.get_text().strip()
    i += 1

#it looks like we have five columns in this table. So let's push this into a data store:

print "now for the data"

for row in rows:
    cells = row.find_all("td")
    # every other row is just a grey bar!
    if len(cells) > 5:
        data = {
            'rank' : cells[0].get_text().strip(), ## 0 : Rate rank 
            'state' : cells[1].get_text().strip(), ## 1 : 
            'total_filings' : cells[2].get_text().strip(), ## 2 : Total filings 
            '1_per_x' : cells[3].get_text().strip(), ## 3 : 1 per X housing units 
            'change_dec_jan' : cells[4].get_text().strip(), ## 4 : Change Dec-Jan 
            'change_jan08' : cells[5].get_text().strip() ## 5 : Change from Jan. 08 
        }
        scraperwiki.sqlite.save(unique_keys=['state'],data=data)

