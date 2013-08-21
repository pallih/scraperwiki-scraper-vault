import scraperwiki
import datetime

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

import scraperwiki
from scraperwiki import sqlite
import re
import numpy 

mech = Browser()
thisYear = datetime.datetime.now().year
years = range(1950, thisYear)
for year in years:
    url = "http://www.formula1.com/results/season/" + str(year)
    page = mech.open(url)
    html = page.read()
    soup = BeautifulSoup(html)
    table = soup.find("table",{"class" : "raceResults"})
    rows = table.findAll("tr")
    for row in rows:
        tds = row.findAll("td")
        if len(tds):
            track = tds[0].text
            date = tds[1].text
            driver = tds[2].text
            team = tds[3].text
            
            urlRace = tds[0].a['href']
            pageRace = mech.open(urlRace)
            htmlRace = pageRace.read()
            soupRace = BeautifulSoup(htmlRace)
            tableRace = soupRace.find("table",{"class" : "raceResults"})
            rowsRace = tableRace.findAll("tr")
            pilots = []
            cars = []
            for rowRace in rowsRace[0:4]:
                tdsRace = rowRace.findAll("td")
                if len(tdsRace):
                    pilots.append(tdsRace[2].text)
                    cars.append(tdsRace[3].text)

            scraperwiki.sqlite.save(unique_keys=["date"], data={"circuit":track, "driver1":pilots[0], "team1":cars[0],"driver2":pilots[1], "team2":cars[1], "driver3":pilots[2], "team3":cars[2], "date":date, "year":year})