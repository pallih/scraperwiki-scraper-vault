from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

url = 'http://www.crash.net/wtcc/championship_tables/content.html'
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

resContainer =  soup.find("div", { "id" : "main" })
rownumber = 0

table = soup.find("table")
for row in table.findAll('tr')[1:40]:

    col = row.findAll('td')
    
    pos = col[0].string
    driver = col[1].string
    team = col[2].string
    points = col[3].string


    data= (pos, driver, team, points)
    scraperwiki.sqlite.save(unique_keys=["driver"], data={"pos":pos, "driver":driver, "team":team, "points":points})

