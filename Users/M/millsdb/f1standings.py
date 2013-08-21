from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

url = 'http://www.gpupdate.net/en/standings/178/2013-formula-1-standings/'


#url = 'http://www.grandprixweather.com/appContent/F1/F1_standings.htm'
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

resContainer =  soup.find("div", { "id" : "middle_container" })
rownumber = 0

table = soup.find("table")
for row in table.findAll('tr')[1:24]:
    col = row.findAll('td')
    
    pos = int(col[0].string.replace(".", ""))
    driver = col[1].a.string
    
    tempTD = col[1]

    team = tempTD.findAll('span')
    team = team[1].string
    points = col[2].string

    country = tempTD.findAll('img')
    country = country[0]['alt'].upper()


    data= (pos, country, driver, team, points)
    scraperwiki.sqlite.save(unique_keys=["pos"], data={"pos":pos, "country":country, "driver":driver, "team":team, "points":points})

