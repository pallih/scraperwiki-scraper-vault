import scraperwiki
import requests
import urllib2
from scraperwiki import scrape
from scraperwiki.sqlite import save
from BeautifulSoup import BeautifulSoup


# this scrapes the 2011 NYC lobbyist list by name and organization
lobbyists = urllib2.urlopen('http://www.nyc.gov/lobbyistsearch/directory.jsp?year_select=2011&view_select=All+Lobbyists')
soupedPage = BeautifulSoup(lobbyists)


for allTables in soupedPage.findAll("td", "multmatch"):
    for allRows in allTables.findAll("tr"):
            myVar = allRows.findAll("a", "backtolist")
            if len(myVar) > 0:
                aRow = {"name": myVar[0].contents[0],
                        "org" : myVar[1].contents[0]
                }
                save([],aRow)
            




