from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()
from datetime import date, timedelta, datetime

#set date to recognise date of scraping

datum = date.today()

url = 'http://www.jerryvermanen.nl/datajournalistiek/jerry.php'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

table = soup.find("table")

print table

for row in table.findAll('tr')[1:20]:
    col = row.findAll('td') 

    api = col[0].string    
    api = api.strip()
    codename = col[1].string
    codename = codename.strip()
    percentage = col[2].string
    percentage = percentage.strip()

    data = (percentage, codename, api, datum)

    print data
    scraperwiki.sqlite.save(unique_keys=["api","datum"], data={"percentage":percentage, "codename":codename, "api":api, "datum":datum})



