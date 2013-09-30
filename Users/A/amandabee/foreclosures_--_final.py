import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})

rows = tables[1].find_all('tr')

for row in rows:
    cells = row.find_all("td")
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

print "et voila!"
import scraperwiki
from bs4 import BeautifulSoup

import string

html = scraperwiki.scrape("http://usatoday30.usatoday.com/money/economy/housing/2009-02-11-decline-housing-foreclosure_N.htm")
soup = BeautifulSoup(html)

tables = soup.find_all("table", {"border" : "0", "cellspacing": "1", "cellpadding": "2"})

rows = tables[1].find_all('tr')

for row in rows:
    cells = row.find_all("td")
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

print "et voila!"
