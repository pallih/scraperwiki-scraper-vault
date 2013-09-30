# Based on Dylan Watson's AFL Player Stats 2013. Extracts the players available for the dream team in 2013.
# Unlike AFL Player Stats 2013, this one only saves the name and positions.

import scraperwiki
import lxml.html
import re
import urllib2

'''Scrapes an individual page'''
def parseProfile(num):
    url = "http://dreamteam.afl.com.au/player/%s" % str(num)
    profile= lxml.html.fromstring(scraperwiki.scrape(url))

    title = profile.cssselect("div.title")[0].text_content()
    name = title[:title.find("\n")]

    mainContent = profile.cssselect("div.colTwo")[0]
    cell = mainContent.cssselect("td")

    price = int(cell[0].text_content().strip().replace("$", "").replace(",",""))
    team = cell[1].text_content().split("\n")[-1].strip()
    position = cell[2].text_content().split("\n")[-1].strip().split(",")
    tp_text = mainContent.cssselect("div.sameHeight1")[0].cssselect("div.box")[1].text_content().split(":")[-1].strip()
    total_points = -1
    if tp_text != 'N/A':
        total_points = int(mainContent.cssselect("div.sameHeight1")[0].cssselect("div.box")[1].text_content().split(":")[-1].strip())

    player = {
        "id": num,
        "name": name,
        "price": price,
        "team": team,
        "total_points": total_points
    }
    scraperwiki.sqlite.save(unique_keys=["id"], data=player, table_name="player")
    

    for p in position:
        positionData = {
            "id": num,
            "position": p
        }
    scraperwiki.sqlite.save(unique_keys=['id', 'position'], data=positionData, table_name="position")


#do the scraping
parseProfile(817)
#for i in range(1, 816):
#  parseProfile(i)# Based on Dylan Watson's AFL Player Stats 2013. Extracts the players available for the dream team in 2013.
# Unlike AFL Player Stats 2013, this one only saves the name and positions.

import scraperwiki
import lxml.html
import re
import urllib2

'''Scrapes an individual page'''
def parseProfile(num):
    url = "http://dreamteam.afl.com.au/player/%s" % str(num)
    profile= lxml.html.fromstring(scraperwiki.scrape(url))

    title = profile.cssselect("div.title")[0].text_content()
    name = title[:title.find("\n")]

    mainContent = profile.cssselect("div.colTwo")[0]
    cell = mainContent.cssselect("td")

    price = int(cell[0].text_content().strip().replace("$", "").replace(",",""))
    team = cell[1].text_content().split("\n")[-1].strip()
    position = cell[2].text_content().split("\n")[-1].strip().split(",")
    tp_text = mainContent.cssselect("div.sameHeight1")[0].cssselect("div.box")[1].text_content().split(":")[-1].strip()
    total_points = -1
    if tp_text != 'N/A':
        total_points = int(mainContent.cssselect("div.sameHeight1")[0].cssselect("div.box")[1].text_content().split(":")[-1].strip())

    player = {
        "id": num,
        "name": name,
        "price": price,
        "team": team,
        "total_points": total_points
    }
    scraperwiki.sqlite.save(unique_keys=["id"], data=player, table_name="player")
    

    for p in position:
        positionData = {
            "id": num,
            "position": p
        }
    scraperwiki.sqlite.save(unique_keys=['id', 'position'], data=positionData, table_name="position")


#do the scraping
parseProfile(817)
#for i in range(1, 816):
#  parseProfile(i)