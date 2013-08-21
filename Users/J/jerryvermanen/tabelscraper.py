from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()
from datetime import date, timedelta, datetime

datum = date.today()

print datum

url = 'http://www.tradingeconomics.com/country-list/rating'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

table = soup.find("table", { "class" : "datatable" })

print table


for row in table.findAll('tr')[1:200]:
    col = row.findAll('td') 

    land = col[0]    
    land = land.text.strip()
    senp_rating = col[1].string
    senp_rating = senp_rating.strip()
    senp_outlook = col[2].string
    senp_outlook = senp_outlook.strip()
    moody_rating = col[3].string
    moody_rating = moody_rating.strip()
    moody_outlook = col[4].string
    moody_outlook = moody_outlook.strip()
    fitch_rating = col[5].string
    fitch_rating = fitch_rating.strip()
    fitch_outlook = col[6].string
    fitch_outlook = fitch_outlook.strip()
    te_rating = col[7].string
    te_rating = te_rating.strip()
    te_outlook = col[7].string
    te_outlook = te_outlook.strip()

    data = (land, senp_rating, senp_outlook, moody_rating, moody_outlook, fitch_rating, fitch_outlook, te_rating, te_outlook, datum)

    print data
    scraperwiki.sqlite.save(unique_keys=["land","datum"], data={"land":land, "senp_rating":senp_rating, "senp_outlook":senp_outlook, "moody_rating":moody_rating, "moody_outlook":moody_outlook, "fitch_rating":fitch_rating, "fitch_outlook":fitch_outlook, "te_rating":te_rating, "te_outlook":te_outlook, "datum":datum})


