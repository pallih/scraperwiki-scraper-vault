import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

html1 = scraperwiki.scrape("http://mlb.mlb.com/mlb/players/")
soup1 = BeautifulSoup(html1)

for team_roster in soup1.find('select', {'id':'ps_team'}).findAll('option'):
    if (len(team_roster["value"]) > 0):
        team = team_roster["value"].split('=')[1]
        team_name = team_roster.text
                    
        record = {}
        record["ID"] = team
        record["TEAM"] = team_name

        #print record
        if record.has_key('ID'):
            # save records to the datastore
            scraperwiki.sqlite.save(["ID"], record) 

