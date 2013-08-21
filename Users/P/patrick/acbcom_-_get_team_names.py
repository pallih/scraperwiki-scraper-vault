# This is a work in progress to scrape ACB.COM for player/game info
# This is a working version scraping the ACB ranking page for extracting
# a list of teams.

import scraperwiki
import lxml.html

def ScrapeTeamList(url):
    # Grab the web page and scrape using lxml.html
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    RowTitles = ['team', 'url', 'nombre'] 
    data = {}
    for el in root.cssselect("td.naranja a.negro"):
        #print el
        nombre = el.text_content()
        SubUrl = el.attrib['href']
        team = SubUrl.rpartition("&id=")[2]
        RowData = [team, SubUrl, nombre]
        for k,v in zip(RowTitles,RowData):
            data[k] = v
        #print data
        scraperwiki.sqlite.save(unique_keys=RowTitles, data=data)
        TeamList == data
    return TeamList

LeagueUrl = "http://www.acb.com/"
TeamUrl = "plantilla.php?cod_equipo="
TeamCod = "BAR"
RowTitles = []
TeamList = []
RowData = []
el = []

url = "http://www.acb.com/resulcla.php"
ScrapeTeamList(url)

