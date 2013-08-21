from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()

#url = 'http://www.gpupdate.net/en/standings/157/2012-motogp-standings/'
#url = 'http://www.grandprixweather.com/appContent/MotoGP/MotoGP_standings.htm'
url = 'http://www.gpupdate.net/nl/stand/190/motogp-stand-2013/'
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

resContainer =  soup.find("div", { "id" : "middle_container" })
rownumber = 0

table = soup.find("table")
for row in table.findAll('tr')[1:]:
    col = row.findAll('td')
    
    pos = int(col[0].string.replace(".", ""))
    driver = col[1].a.string
    points = col[2].string


    data= (pos, driver, points)
    #print(data)
    scraperwiki.sqlite.save(unique_keys=["pos"], data={"pos":pos, "driver":driver, "points":points})