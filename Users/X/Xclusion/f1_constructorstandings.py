from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
mech = Browser()
url = 'http://www.gpupdate.net/en/standings/178/2013-formula-1-standings/'
#url = 'http://www.gpupdate.net/en/standings/154/2013-formula-1-standings/' 
#url = 'http://grandprixweather.com/appContent/F1/F1_standings.htm'
page = mech.open(url)
html = page.read()
soup = BeautifulSoup(html)

resContainer =  soup.find("div", { "id" : "middle_container" })
print(resContainer)
rownumber = 0

table = resContainer("table")[1]
for row in table.findAll('tr')[1:]:
    col = row.findAll('td')
    
    pos = int(col[0].string.replace(".", ""))
    driver = col[1].a.string
    points = col[2].text

    #print(col[2])
    data= (pos, driver, points)
    scraperwiki.sqlite.save(unique_keys=["pos"], data={"pos":pos, "driver":driver, "points":points})

