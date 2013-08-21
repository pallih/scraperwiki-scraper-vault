#!/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
print('starting')
mech = Browser()

url = 'http://www.gpupdate.net/en/standings/178/2013-formula-1-standings/'


#url = 'http://www.grandprixweather.com/appContent/F1/F1_standings.htm'
print('opening url')
page = mech.open(url)
print('reading page')
html = page.read()
print('souping page')
soup = BeautifulSoup(html)

print('searching divs')
resContainer =  soup.find("div", { "id" : "middle_container" })
rownumber = 0

table = soup.find("table")
for row in table.findAll('tr')[1:24]:
    print('processing data..')
    col = row.findAll('td')
    
    pos = int(col[0].string.replace(".", ""))
    driver = col[1].a.string
    points = col[2].string


    data= (pos, driver, points)
    scraperwiki.sqlite.save(unique_keys=["pos"], data={"pos":pos, "driver":driver, "points":points})

