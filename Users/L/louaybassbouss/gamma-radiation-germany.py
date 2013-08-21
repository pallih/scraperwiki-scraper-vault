# http://odlinfo.bfs.de/laenderliste.php

import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
from datetime import timedelta

baseURL = 'http://odlinfo.bfs.de/'
name = "Gamma Radiation"
indicator = "TID"
unit = "µSv/h"

def run():
    html = scraperwiki.scrape(baseURL+'laenderliste.php')
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[4];
    rows = table.findAll('tr');
    for i in range(1,len(rows)):
        row = rows[i]
        cols = row.findAll('td')
        href = cols[0].find('a')['href']
        state = cols[1].text
        try:
            scrape_site(baseURL+href,state)
        except:
            print "error "+ baseURL+href 
            pass

def scrape_site(url,state):
    d = date.today()-timedelta(days=1)
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    table = html.findAll('table')[4];
    rows = table.findAll('tr');
    for i in range(1,len(rows)):
        row = rows[i]
        cols = row.findAll('td')
        observation = {}
        observation['station'] = cols[1].text
        observation['name'] = name
        observation['indicator'] = indicator
        observation['unit'] = unit
        observation['date'] = d
        observation['state'] = state
        try:
            observation['elevation'] = float(cols[2].text)
        except ValueError:
            observation['elevation'] = None
        try:
            observation['value'] = float(cols[3].text)
        except ValueError:
            observation['value'] = None
        scraperwiki.sqlite.save(unique_keys=['name','indicator','station','date'], data = observation,table_name="observations")
        print observation

run()