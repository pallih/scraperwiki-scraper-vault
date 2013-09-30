from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

url = 'http://www.wrc.com/results/2013/championship-standings/drivers/'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

table = soup.find("table", { "class" : "results" })


for row in table.findAll('tr')[1:50]:
    col = row.findAll('td') 

    pos = col[0].string.replace(".", "")
    pos = pos.strip()
    driver = col[2].string
    driver = driver.strip()
    points = col[16].string
    points = points.strip()

    data = (pos, driver, points)
    scraperwiki.sqlite.save(unique_keys=["driver"], data={"pos":pos, "driver":driver, "points":points})



from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

url = 'http://www.wrc.com/results/2013/championship-standings/drivers/'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

table = soup.find("table", { "class" : "results" })


for row in table.findAll('tr')[1:50]:
    col = row.findAll('td') 

    pos = col[0].string.replace(".", "")
    pos = pos.strip()
    driver = col[2].string
    driver = driver.strip()
    points = col[16].string
    points = points.strip()

    data = (pos, driver, points)
    scraperwiki.sqlite.save(unique_keys=["driver"], data={"pos":pos, "driver":driver, "points":points})



