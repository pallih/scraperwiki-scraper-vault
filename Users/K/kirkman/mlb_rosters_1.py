import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

html1 = scraperwiki.scrape("http://mlb.mlb.com/mlb/players/")
soup1 = BeautifulSoup(html1)

for team_roster in soup1.find('select', {'id':'ps_team'}).findAll('option'):
    if (len(team_roster["value"]) > 0):
        team = team_roster["value"].split('=')[1]

        page_url = Template("http://mlb.com/team/roster_active.jsp?c_id=$team").substitute(team=team)
        html2 = scraperwiki.scrape(page_url)
        soup2 = BeautifulSoup(html2)
        
        roster_table = soup2.find('table', {'class':'team_table_results'})
        team_name = roster_table.find('caption').text.replace(' Active Roster','')
        
        for section in roster_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                columns = row.findAll('td')

                player_url_source = columns[1].find('a')["href"]
                player_id = player_url_source.replace('/team/player.jsp?player_id=','')
                player_url = Template("http://mlb.com/team/player.jsp?player_id=$player_id").substitute(player_id=player_id)

                html3 = scraperwiki.scrape(player_url)
                soup3 = BeautifulSoup(html3)

                player_name = soup3.find('h1', {'id':'player_name'}).text.replace('&nbsp;','')
                print(player_name)

                player_h1 = soup3.find('h1', {'id':'player_name'})
                print(player_h1)


                # From this point on, the script doesn't work.
                # The reason is that MLB is not serving these pages with the data in them.
                # Instead, the page loads and then grabs JSON file(s) to populate the page.
                # These scrapers don't execute JS on the page, I think, which is why it breaks down.

                # Given that, I'm better off just grabbing their JSON feed myself rather than scraping.

                player_num = soup3.find('span', {'id':'player_number'}).text
                print(player_num)

                player_pos = soup3.find('span', {'id':'player_position'}).text.replace(' | ','')
                print(player_pos)


                player_stat_table = soup3.find('table', {'class':'stats_table'})


                player_stats = player_stat_table.findAll('tr', {'index':'0'}, recursive=False)

                record = {}
                columns3 = player_stats.findAll('td')
                record["ID"] = player_id
                record["Team"] = team_name
                record["Name"] = plauer_name
                record["Position"] = player_pos
                record["Num"] = player_num
                record["Wins"] = columns3[1].text
                record["Losses"] = columns3[2].text
                record["ERA"] = columns3[3].text
                #print record
                if record.has_key('ID'):
                    # save records to the datastore
                    scraperwiki.sqlite.save(["ID"], record) import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

html1 = scraperwiki.scrape("http://mlb.mlb.com/mlb/players/")
soup1 = BeautifulSoup(html1)

for team_roster in soup1.find('select', {'id':'ps_team'}).findAll('option'):
    if (len(team_roster["value"]) > 0):
        team = team_roster["value"].split('=')[1]

        page_url = Template("http://mlb.com/team/roster_active.jsp?c_id=$team").substitute(team=team)
        html2 = scraperwiki.scrape(page_url)
        soup2 = BeautifulSoup(html2)
        
        roster_table = soup2.find('table', {'class':'team_table_results'})
        team_name = roster_table.find('caption').text.replace(' Active Roster','')
        
        for section in roster_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                columns = row.findAll('td')

                player_url_source = columns[1].find('a')["href"]
                player_id = player_url_source.replace('/team/player.jsp?player_id=','')
                player_url = Template("http://mlb.com/team/player.jsp?player_id=$player_id").substitute(player_id=player_id)

                html3 = scraperwiki.scrape(player_url)
                soup3 = BeautifulSoup(html3)

                player_name = soup3.find('h1', {'id':'player_name'}).text.replace('&nbsp;','')
                print(player_name)

                player_h1 = soup3.find('h1', {'id':'player_name'})
                print(player_h1)


                # From this point on, the script doesn't work.
                # The reason is that MLB is not serving these pages with the data in them.
                # Instead, the page loads and then grabs JSON file(s) to populate the page.
                # These scrapers don't execute JS on the page, I think, which is why it breaks down.

                # Given that, I'm better off just grabbing their JSON feed myself rather than scraping.

                player_num = soup3.find('span', {'id':'player_number'}).text
                print(player_num)

                player_pos = soup3.find('span', {'id':'player_position'}).text.replace(' | ','')
                print(player_pos)


                player_stat_table = soup3.find('table', {'class':'stats_table'})


                player_stats = player_stat_table.findAll('tr', {'index':'0'}, recursive=False)

                record = {}
                columns3 = player_stats.findAll('td')
                record["ID"] = player_id
                record["Team"] = team_name
                record["Name"] = plauer_name
                record["Position"] = player_pos
                record["Num"] = player_num
                record["Wins"] = columns3[1].text
                record["Losses"] = columns3[2].text
                record["ERA"] = columns3[3].text
                #print record
                if record.has_key('ID'):
                    # save records to the datastore
                    scraperwiki.sqlite.save(["ID"], record) 