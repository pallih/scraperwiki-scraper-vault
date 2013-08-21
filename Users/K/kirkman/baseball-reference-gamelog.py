import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`date` text, `game_minutes` integer, `home` text, `visitor` text, `home_score` integer, `visitor_score` integer, `daynight` text, `innings` integer, `home_lg` text) ")



allTeams = [
    ['BAL','AL'],
    ['BOS','AL'],
    ['CHW','AL'],
    ['CLE','AL'],
    ['DET','AL'],
    ['HOU','AL'],
    ['KCR','AL'],
    ['LAA','AL'],
    ['MIN','AL'],
    ['NYY','AL'],
    ['OAK','AL'],
    ['SEA','AL'],
    ['TBR','AL'],
    ['TEX','AL'],
    ['TOR','AL'],
    ['ARI','NL'],
    ['ATL','NL'],
    ['CHC','NL'],
    ['CIN','NL'],
    ['COL','NL'],
    ['LAD','NL'],
    ['MIA','NL'],
    ['MIL','NL'],
    ['NYM','NL'],
    ['PHI','NL'],
    ['PIT','NL'],
    ['SDP','NL'],
    ['SFG','NL'],
    ['STL','NL'],
    ['WSN','NL']
]

for team in allTeams:

    url1 = "http://www.baseball-reference.com/teams/" + team[0] + "/2013-schedule-scores.shtml"
    league = team[1]
    html1 = scraperwiki.scrape(url1)
    soup1 = BeautifulSoup(html1)
    
    season_table = soup1.find('table',id='team_schedule')
    if (season_table):
    #    print (reg_season)
        for section in season_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                ## We don't want to process rows that serve as decorative borders
                ## ie, <tr class=" thead">
                if (not row.get('class') == ' thead'):
                    columns = row.findAll('td')
                    ## We don't want to process rows where a game has not been played.
                    ## So we check for existence of the boxscore
                    boxscore = columns[3].text
                    if (boxscore == 'boxscore'):
    
                        game_homeAway = columns[5].text

                        ## We only need to process home games. That way there won't be duplicates as we scrape all of MLB.
                        if (not game_homeAway == '@'):

                            game_date = columns[2].find('a')["href"].split('=')[1]
                            ## figure out who was home and who was away
                            game_team = columns[4].text
                            game_opp = columns[6].text
                            game_runs = columns[8].text
                            game_runsAllowed = columns[9].text
                            game_homeTeam = game_team
                            game_homeScore = game_runs
                            game_awayTeam = game_opp
                            game_awayScore = game_runsAllowed
        
                            game_result = columns[7].text
                            game_innings = columns[10].text
                            if (game_innings == ''):
                                game_innings = 9
                            else:
                                game_innings = int(game_innings)
        
                            game_length_h = int( columns[17].text.split(':')[0] )
                            game_length_m = int( columns[17].text.split(':')[1] )
                            game_length = (game_length_h * 60) + game_length_m
        
                            game_dayNight = columns[18].text
        
        
                            record = {}
                            record["date"] = game_date
                            record["game_minutes"] = game_length
                            record["home"] = game_homeTeam
                            record["visitor"] = game_awayTeam
                            record["home_score"] = game_homeScore
                            record["visitor_score"] = game_awayScore
                            record["daynight"] = game_dayNight
                            record["innings"] = game_innings
                            record["home_lg"] = league
        
        
                            #print record
                            # save HOME games to the datastore, but not Away games. Don't want duplicates as we scrape rest of MLB.
                            if (game_homeTeam == game_team):
                                # we don't really have a unique key unfortunately
                                scraperwiki.sqlite.save([], record)

import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`date` text, `game_minutes` integer, `home` text, `visitor` text, `home_score` integer, `visitor_score` integer, `daynight` text, `innings` integer, `home_lg` text) ")



allTeams = [
    ['BAL','AL'],
    ['BOS','AL'],
    ['CHW','AL'],
    ['CLE','AL'],
    ['DET','AL'],
    ['HOU','AL'],
    ['KCR','AL'],
    ['LAA','AL'],
    ['MIN','AL'],
    ['NYY','AL'],
    ['OAK','AL'],
    ['SEA','AL'],
    ['TBR','AL'],
    ['TEX','AL'],
    ['TOR','AL'],
    ['ARI','NL'],
    ['ATL','NL'],
    ['CHC','NL'],
    ['CIN','NL'],
    ['COL','NL'],
    ['LAD','NL'],
    ['MIA','NL'],
    ['MIL','NL'],
    ['NYM','NL'],
    ['PHI','NL'],
    ['PIT','NL'],
    ['SDP','NL'],
    ['SFG','NL'],
    ['STL','NL'],
    ['WSN','NL']
]

for team in allTeams:

    url1 = "http://www.baseball-reference.com/teams/" + team[0] + "/2013-schedule-scores.shtml"
    league = team[1]
    html1 = scraperwiki.scrape(url1)
    soup1 = BeautifulSoup(html1)
    
    season_table = soup1.find('table',id='team_schedule')
    if (season_table):
    #    print (reg_season)
        for section in season_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                ## We don't want to process rows that serve as decorative borders
                ## ie, <tr class=" thead">
                if (not row.get('class') == ' thead'):
                    columns = row.findAll('td')
                    ## We don't want to process rows where a game has not been played.
                    ## So we check for existence of the boxscore
                    boxscore = columns[3].text
                    if (boxscore == 'boxscore'):
    
                        game_homeAway = columns[5].text

                        ## We only need to process home games. That way there won't be duplicates as we scrape all of MLB.
                        if (not game_homeAway == '@'):

                            game_date = columns[2].find('a')["href"].split('=')[1]
                            ## figure out who was home and who was away
                            game_team = columns[4].text
                            game_opp = columns[6].text
                            game_runs = columns[8].text
                            game_runsAllowed = columns[9].text
                            game_homeTeam = game_team
                            game_homeScore = game_runs
                            game_awayTeam = game_opp
                            game_awayScore = game_runsAllowed
        
                            game_result = columns[7].text
                            game_innings = columns[10].text
                            if (game_innings == ''):
                                game_innings = 9
                            else:
                                game_innings = int(game_innings)
        
                            game_length_h = int( columns[17].text.split(':')[0] )
                            game_length_m = int( columns[17].text.split(':')[1] )
                            game_length = (game_length_h * 60) + game_length_m
        
                            game_dayNight = columns[18].text
        
        
                            record = {}
                            record["date"] = game_date
                            record["game_minutes"] = game_length
                            record["home"] = game_homeTeam
                            record["visitor"] = game_awayTeam
                            record["home_score"] = game_homeScore
                            record["visitor_score"] = game_awayScore
                            record["daynight"] = game_dayNight
                            record["innings"] = game_innings
                            record["home_lg"] = league
        
        
                            #print record
                            # save HOME games to the datastore, but not Away games. Don't want duplicates as we scrape rest of MLB.
                            if (game_homeTeam == game_team):
                                # we don't really have a unique key unfortunately
                                scraperwiki.sqlite.save([], record)

