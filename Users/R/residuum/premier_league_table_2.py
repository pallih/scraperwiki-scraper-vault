import BeautifulSoup
from scraperwiki import sqlite
from scraperwiki import scrape

html = scrape('http://www.premierleague.com/en-gb/matchday/league-table.html')

page = BeautifulSoup.BeautifulSoup(html)

premierLeagueData = []

for row in page.find('table').find('tbody').findAll('tr', 'club-row'):
    pos = int(row.find('td', 'col-pos').string)
    team = row.find('td', 'col-club').string
    goalsFor = int(row.find('td', 'col-gf').string)
    goalsAgainst = int(row.find('td', 'col-ga').string)
    goalDifference = int(row.find('td', 'col-gd').string)
    points = int(row.find('td', 'col-pts').string)
    #print pos, team,"gf", goalsFor, "ga", goalsAgainst, "gd", goalDifference, "pts", points
    teamItem = {'pos':pos,
        'team':team,
        'gf':goalsFor,
        'ga':goalsAgainst,
        'gd':goalDifference,
        'pts':points}
    premierLeagueData.append(teamItem)

if len(premierLeagueData) > 0:
    #truncate data store
    sqlite.execute("DELETE FROM `swdata`")
    #add each table line to data store
    for teamItem in premierLeagueData:
        sqlite.save(unique_keys=['team'], data=teamItem)



