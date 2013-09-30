import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

html1 = scraperwiki.scrape("http://www.baseball-reference.com/awards/mvp_cya.shtml")
soup1 = BeautifulSoup(html1)

for team_roster in soup1.find('select', {'id':'ps_team'}).findAll('option'):
    if (len(team_roster["value"]) > 0):
        team = team_roster["value"].split('=')[1]

        page_url = Template("http://www.baseball-reference.com/awards/mvp_cya.shtml").substitute(team=team)
        html2 = scraperwiki.scrape(page_url)
        soup2 = BeautifulSoup(html2)
        
        roster_table = soup2.find('table', {'class':'team_table_results'})
        team_name = roster_table.find('caption').text.replace(' Active Roster','')
        
        for section in roster_table.findAll(re.compile('thead|tbody'), recursive=False):
            if section.name == "thead":
                position_name = section.find('th', {'class':'playernameHead'}).text
            elif section.name == "tbody":
                for row in section.findAll('tr'):
                    record = {}
                    columns = row.findAll('td')
                    record["ID"] = columns[1].find('a')["href"].replace('/team/player.jsp?player_id=','')
                    record["Team"] = team_name
                    record["Jersey Number"] = columns[0].text
                    record["Name"] = columns[1].text
                    record["Position"] = re.sub(re.compile('s$'), '', position_name)
                    bat_throw = columns[2].text.split('-')
                    record["Bats"] = bat_throw[0]
                    record["Throws"] = bat_throw[1]
                    record["Height"] = columns[3].text
                    record["Weight"] = columns[4].text
                    record["Date of Birth"] = columns[5].text
                    #print record
                    if record.has_key('ID'):
                        # save records to the datastore
                        scraperwiki.sqlite.save(["ID"], record) import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

html1 = scraperwiki.scrape("http://www.baseball-reference.com/awards/mvp_cya.shtml")
soup1 = BeautifulSoup(html1)

for team_roster in soup1.find('select', {'id':'ps_team'}).findAll('option'):
    if (len(team_roster["value"]) > 0):
        team = team_roster["value"].split('=')[1]

        page_url = Template("http://www.baseball-reference.com/awards/mvp_cya.shtml").substitute(team=team)
        html2 = scraperwiki.scrape(page_url)
        soup2 = BeautifulSoup(html2)
        
        roster_table = soup2.find('table', {'class':'team_table_results'})
        team_name = roster_table.find('caption').text.replace(' Active Roster','')
        
        for section in roster_table.findAll(re.compile('thead|tbody'), recursive=False):
            if section.name == "thead":
                position_name = section.find('th', {'class':'playernameHead'}).text
            elif section.name == "tbody":
                for row in section.findAll('tr'):
                    record = {}
                    columns = row.findAll('td')
                    record["ID"] = columns[1].find('a')["href"].replace('/team/player.jsp?player_id=','')
                    record["Team"] = team_name
                    record["Jersey Number"] = columns[0].text
                    record["Name"] = columns[1].text
                    record["Position"] = re.sub(re.compile('s$'), '', position_name)
                    bat_throw = columns[2].text.split('-')
                    record["Bats"] = bat_throw[0]
                    record["Throws"] = bat_throw[1]
                    record["Height"] = columns[3].text
                    record["Weight"] = columns[4].text
                    record["Date of Birth"] = columns[5].text
                    #print record
                    if record.has_key('ID'):
                        # save records to the datastore
                        scraperwiki.sqlite.save(["ID"], record) 