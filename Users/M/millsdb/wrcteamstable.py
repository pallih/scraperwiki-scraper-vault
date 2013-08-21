from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

url = 'http://www.wrc.com/results/2013/championship-standings/manufacturers/'

page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

table = soup.find("table", { "class" : "results team" })


for row in table.findAll('tr')[1:50]:
    col = row.findAll('td') 

    pos = col[0].string.replace(".", "")
    pos = pos.strip()
    team = col[2].string
    team = team.strip()
    points = col[16].string
    points = points.strip()

    data = (pos, team, points)
    scraperwiki.sqlite.save(unique_keys=["team"], data={"pos":pos, "team":team, "points":points})



