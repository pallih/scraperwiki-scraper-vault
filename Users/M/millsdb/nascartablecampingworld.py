from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

url = 'http://aol.sportingnews.com/nascar/standings/league/Camping%20World%20Truck%20Series/2013'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

table = soup.find("table", { "class" : "table table-bordered table-striped" })


for row in table.findAll('tr')[1:85]:
    col = row.findAll('td')
    
    pos = col[0].string
    pos = pos.strip()
    
    driver = col[2].a.string
    driver = driver.strip()
    points = col[3].string
    points = points.strip()

    data = (pos, driver, points)
    scraperwiki.sqlite.save(unique_keys=["pos"], data={"pos":pos, "driver":driver, "points":points})



