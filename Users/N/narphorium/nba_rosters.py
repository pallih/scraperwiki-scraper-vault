import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

#html1 = scraperwiki.scrape("http://www.nba.com/teams/teamIndividualLinks.html")
#html1 = scraperwiki.scrape("http://www.nba.com/")
html1 = scraperwiki.scrape("http://www.nba.com/playoffs/2011/index.html")
soup1 = BeautifulSoup(html1)

for section in soup1.findAll('div', {'class':'nbaT2OverHalf'}):
    for team_entry in section.findAll('a'):
        #team_name = 'Dallas Mavericks'
        #team_id = 'mavericks'
        
        team_name = team_entry.text
        team_id = team_entry['href'].split("'")[3].lower()
        
        page_url = Template("http://www.nba.com/$team/roster/").substitute(team=team_id)
        html2 = scraperwiki.scrape(page_url)
        soup2 = BeautifulSoup(html2)
        
        roster_table = soup2.find('table', {'class':' gSGTable'})
        
        for row in roster_table.findAll('tr', recursive=False)[2:]:
            record = {}
            columns = row.findAll('td')
            record["ID"] = columns[1].find('a')["href"].split('/')[2]
            record["Team"] = team_name
            record["Jersey Number"] = columns[0].text
            record["Name"] = columns[1].text
            record["Position"] = columns[2].text
            record["Height"] = columns[3].text
            record["Weight"] = columns[4].text
            record["Date of Birth"] = columns[5].text
            record["From"] = columns[6].text.replace('&nbsp;',' ').strip()
            print record
            #if record.has_key('ID'):
                # save records to the datastore
                #scraperwiki.sqlite.save(["ID"], record) 
import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

#html1 = scraperwiki.scrape("http://www.nba.com/teams/teamIndividualLinks.html")
#html1 = scraperwiki.scrape("http://www.nba.com/")
html1 = scraperwiki.scrape("http://www.nba.com/playoffs/2011/index.html")
soup1 = BeautifulSoup(html1)

for section in soup1.findAll('div', {'class':'nbaT2OverHalf'}):
    for team_entry in section.findAll('a'):
        #team_name = 'Dallas Mavericks'
        #team_id = 'mavericks'
        
        team_name = team_entry.text
        team_id = team_entry['href'].split("'")[3].lower()
        
        page_url = Template("http://www.nba.com/$team/roster/").substitute(team=team_id)
        html2 = scraperwiki.scrape(page_url)
        soup2 = BeautifulSoup(html2)
        
        roster_table = soup2.find('table', {'class':' gSGTable'})
        
        for row in roster_table.findAll('tr', recursive=False)[2:]:
            record = {}
            columns = row.findAll('td')
            record["ID"] = columns[1].find('a')["href"].split('/')[2]
            record["Team"] = team_name
            record["Jersey Number"] = columns[0].text
            record["Name"] = columns[1].text
            record["Position"] = columns[2].text
            record["Height"] = columns[3].text
            record["Weight"] = columns[4].text
            record["Date of Birth"] = columns[5].text
            record["From"] = columns[6].text.replace('&nbsp;',' ').strip()
            print record
            #if record.has_key('ID'):
                # save records to the datastore
                #scraperwiki.sqlite.save(["ID"], record) 
