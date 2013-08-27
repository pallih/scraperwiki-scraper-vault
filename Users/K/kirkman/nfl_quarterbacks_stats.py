import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

# this is the code to establish a schema. Only need it the first time I run.

#scraperwiki.sqlite.execute("drop table if exists `swdata`")
#scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`gameId` text, `playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `gameWeek` text, `gameDate` text, `gameOpp` text, `gameResult` text, `gameScore` text, `gameG` text, `gameGS` text, `gameComp` text, `gamePassAtt` text, `gamePct` text, `gamePassYds` text, `gamePassTd` text, `gameInt` text, `gameSck` text, `gameSckY` text, `gameRate` text, `gameRushAtt` text, `gameRushYds` text, `gameRushTd` text, `gameFum` text, `gameFumLost` text) ")


scraperwiki.sqlite.attach('nfl_quarterback_stats')

theQuarterbacks = scraperwiki.sqlite.select('* FROM `nfl_quarterback_stats`.swdata WHERE playerStatus = "ACT"')

for player in theQuarterbacks:
    player_id = player["playerId"]
    player_full_name = player["playerFullName"]
    player_first_name = player["playerFirstName"]
    player_last_name = player["playerLastName"]
    player_name_code = player["playerNameCode"]
    player_status = player["playerStatus"]
    player_url = player["playerUrl"]
    player_gamelog_url = player_url.replace('profile','gamelogs')
    player_gamelog_url += '?99'
    player_team = player["playerTeam"]
    player_position = player["playerPos"]
    player_uni_number = player["playerNum"]


    html1 = scraperwiki.scrape(player_gamelog_url)
    soup1 = BeautifulSoup(html1)

    print player_gamelog_url
    print soup1
    game_year = soup1.find('div',id='game-log-year').find('strong').text.replace('Game Log: ','')

    # The table with Regular Season stats does not have a unique ID. 
    # So we look for a header cell which says "Regular Season" and then find its parent TABLE.

    ## Some players may not have reg season stats yet. If so, exclude them.

    reg_season = soup1.find('td',text='Regular Season')
    if (reg_season):
        game_table = reg_season.findParents('table')[0]
    
        for section in game_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                ## print (row)
                columns = row.findAll('td')
    
                ## We don't want to process rows that serve as decorative borders
                ## ie, <tr><td colspan="22" class="border-td" ></td></tr>
                ## We also don't want to process the Player-Totals row
                ## Searching for colspan in the first TD takes care of both cases
    
                if (not columns[0].has_key('colspan')): 
    

                    ## also have to watch out for Bye weeks

                    if (not columns[1].text == 'Bye'):

                        game_week = columns[0].text
                        game_date = columns[1].text
                        game_opp = columns[2].text.replace('\r','').replace('\n','').replace('\t','')
                
                        ## game_result = columns[3].find('span').text
                        game_result_raw = columns[3].text
                        game_result = game_result_raw[0]

                        game_score = columns[3].find('a').text
                        game_id = game_year + game_date + player_id
                        game_id = game_id.replace('/','')
            
                        ## begin stats
                        # these stats will always have a number
                        game_g = columns[4].text
                        game_gs = columns[5].text


                        # these stats might be blank
                        game_rate = columns[15].text
                        if (game_rate == '0.0' and game_g == '0') : game_rate = None
                        game_comp = columns[6].text
                        if (game_comp == '--') : game_comp = None
                        game_pass_att = columns[7].text
                        if (game_pass_att == '--') : game_pass_att = None
                        game_pct = columns[8].text
                        if (game_pct == '--') : game_pct = None
                        game_pass_yds = columns[9].text
                        if (game_pass_yds == '--') : game_pass_yds = None
                        game_pass_td = columns[11].text
                        if (game_pass_td == '--') : game_pass_td = None
                        game_int = columns[12].text
                        if (game_int == '--') : game_int = None
                        game_sck = columns[13].text
                        if (game_sck == '--') : game_sck = None
                        game_sckY = columns[14].text
                        if (game_sckY == '--') : game_sckY = None
                        game_rush_att = columns[16].text
                        if (game_rush_att == '--') : game_rush_att = None
                        game_rush_yds = columns[17].text
                        if (game_rush_yds == '--') : game_rush_yds = None
                        game_rush_td = columns[19].text
                        if (game_rush_td == '--') : game_rush_td = None
                        game_fum = columns[20].text
                        if (game_fum == '--') : game_fum = None
                        game_fum_lost = columns[20].text
                        if (game_fum_lost == '--') : game_fum_lost = None

                    else:
                        game_week = columns[0].text
                        if   (game_week == '1')  : game_date = '09/09'
                        elif (game_week == '2')  : game_date = '09/16'
                        elif (game_week == '3')  : game_date = '09/23'
                        elif (game_week == '4')  : game_date = '09/30'
                        elif (game_week == '5')  : game_date = '10/07'
                        elif (game_week == '6')  : game_date = '10/14'
                        elif (game_week == '7')  : game_date = '10/21'
                        elif (game_week == '8')  : game_date = '10/28'
                        elif (game_week == '9')  : game_date = '11/04'
                        elif (game_week == '10') : game_date = '11/11'
                        elif (game_week == '11') : game_date = '11/18'
                        elif (game_week == '12') : game_date = '11/25'
                        elif (game_week == '13') : game_date = '12/02'
                        elif (game_week == '14') : game_date = '12/09'
                        elif (game_week == '15') : game_date = '12/16'
                        elif (game_week == '16') : game_date = '12/23'
                        elif (game_week == '17') : game_date = '12/30'
                        else : game_date = '99/99'

                        game_id = game_year + game_date + player_id
                        game_id = game_id.replace('/','')

                        game_opp = None
                        game_result = None
                        game_score = None
                        game_g = None
                        game_gs = None
                        game_rate = None
                        game_comp = None
                        game_pass_att = None
                        game_pct = None
                        game_pass_yds = None
                        game_pass_td = None
                        game_int = None
                        game_sck = None
                        game_sckY = None
                        game_rush_att = None
                        game_rush_yds = None
                        game_rush_td = None
                        game_fum = None
                        game_fum_lost = None

    
    
                    record = {}
                    record["playerId"] = player_id
                    record["playerFullName"] = player_full_name
                    record["playerFirstName"] = player_first_name
                    record["playerLastName"] = player_last_name
                    record["playerTeam"] = player_team
                    record["gameId"] = game_id
                    record["gameWeek"] = game_week
                    record["gameDate"] = game_date
                    record["gameOpp"] = game_opp
                    record["gameResult"] = game_result
                    record["gameScore"] = game_score
                    record["gameId"] = game_id
                    record["gameG"] = game_g
                    record["gameGS"] = game_gs
                    record["gameRate"] = game_rate
                    record["gameComp"] = game_comp
                    record["gamePassAtt"] = game_pass_att
                    record["gamePct"] = game_pct
                    record["gamePassYds"] = game_pass_yds
                    record["gamePassTd"] = game_pass_td
                    record["gameInt"] = game_int
                    record["gameSck"] = game_sck
                    record["gameSckY"] = game_sckY
                    record["gameRushAtt"] = game_rush_att
                    record["gameRushYds"] = game_rush_yds
                    record["gameRushTd"] = game_rush_td
                    record["gameFum"] = game_fum
                    record["gameFumLost"] = game_fum_lost
    
            
                    #print record
                    if record.has_key('gameId'):
                        # save records to the datastore
                        scraperwiki.sqlite.save(["gameId"], record)


import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

# this is the code to establish a schema. Only need it the first time I run.

#scraperwiki.sqlite.execute("drop table if exists `swdata`")
#scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`gameId` text, `playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `gameWeek` text, `gameDate` text, `gameOpp` text, `gameResult` text, `gameScore` text, `gameG` text, `gameGS` text, `gameComp` text, `gamePassAtt` text, `gamePct` text, `gamePassYds` text, `gamePassTd` text, `gameInt` text, `gameSck` text, `gameSckY` text, `gameRate` text, `gameRushAtt` text, `gameRushYds` text, `gameRushTd` text, `gameFum` text, `gameFumLost` text) ")


scraperwiki.sqlite.attach('nfl_quarterback_stats')

theQuarterbacks = scraperwiki.sqlite.select('* FROM `nfl_quarterback_stats`.swdata WHERE playerStatus = "ACT"')

for player in theQuarterbacks:
    player_id = player["playerId"]
    player_full_name = player["playerFullName"]
    player_first_name = player["playerFirstName"]
    player_last_name = player["playerLastName"]
    player_name_code = player["playerNameCode"]
    player_status = player["playerStatus"]
    player_url = player["playerUrl"]
    player_gamelog_url = player_url.replace('profile','gamelogs')
    player_gamelog_url += '?99'
    player_team = player["playerTeam"]
    player_position = player["playerPos"]
    player_uni_number = player["playerNum"]


    html1 = scraperwiki.scrape(player_gamelog_url)
    soup1 = BeautifulSoup(html1)

    print player_gamelog_url
    print soup1
    game_year = soup1.find('div',id='game-log-year').find('strong').text.replace('Game Log: ','')

    # The table with Regular Season stats does not have a unique ID. 
    # So we look for a header cell which says "Regular Season" and then find its parent TABLE.

    ## Some players may not have reg season stats yet. If so, exclude them.

    reg_season = soup1.find('td',text='Regular Season')
    if (reg_season):
        game_table = reg_season.findParents('table')[0]
    
        for section in game_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                ## print (row)
                columns = row.findAll('td')
    
                ## We don't want to process rows that serve as decorative borders
                ## ie, <tr><td colspan="22" class="border-td" ></td></tr>
                ## We also don't want to process the Player-Totals row
                ## Searching for colspan in the first TD takes care of both cases
    
                if (not columns[0].has_key('colspan')): 
    

                    ## also have to watch out for Bye weeks

                    if (not columns[1].text == 'Bye'):

                        game_week = columns[0].text
                        game_date = columns[1].text
                        game_opp = columns[2].text.replace('\r','').replace('\n','').replace('\t','')
                
                        ## game_result = columns[3].find('span').text
                        game_result_raw = columns[3].text
                        game_result = game_result_raw[0]

                        game_score = columns[3].find('a').text
                        game_id = game_year + game_date + player_id
                        game_id = game_id.replace('/','')
            
                        ## begin stats
                        # these stats will always have a number
                        game_g = columns[4].text
                        game_gs = columns[5].text


                        # these stats might be blank
                        game_rate = columns[15].text
                        if (game_rate == '0.0' and game_g == '0') : game_rate = None
                        game_comp = columns[6].text
                        if (game_comp == '--') : game_comp = None
                        game_pass_att = columns[7].text
                        if (game_pass_att == '--') : game_pass_att = None
                        game_pct = columns[8].text
                        if (game_pct == '--') : game_pct = None
                        game_pass_yds = columns[9].text
                        if (game_pass_yds == '--') : game_pass_yds = None
                        game_pass_td = columns[11].text
                        if (game_pass_td == '--') : game_pass_td = None
                        game_int = columns[12].text
                        if (game_int == '--') : game_int = None
                        game_sck = columns[13].text
                        if (game_sck == '--') : game_sck = None
                        game_sckY = columns[14].text
                        if (game_sckY == '--') : game_sckY = None
                        game_rush_att = columns[16].text
                        if (game_rush_att == '--') : game_rush_att = None
                        game_rush_yds = columns[17].text
                        if (game_rush_yds == '--') : game_rush_yds = None
                        game_rush_td = columns[19].text
                        if (game_rush_td == '--') : game_rush_td = None
                        game_fum = columns[20].text
                        if (game_fum == '--') : game_fum = None
                        game_fum_lost = columns[20].text
                        if (game_fum_lost == '--') : game_fum_lost = None

                    else:
                        game_week = columns[0].text
                        if   (game_week == '1')  : game_date = '09/09'
                        elif (game_week == '2')  : game_date = '09/16'
                        elif (game_week == '3')  : game_date = '09/23'
                        elif (game_week == '4')  : game_date = '09/30'
                        elif (game_week == '5')  : game_date = '10/07'
                        elif (game_week == '6')  : game_date = '10/14'
                        elif (game_week == '7')  : game_date = '10/21'
                        elif (game_week == '8')  : game_date = '10/28'
                        elif (game_week == '9')  : game_date = '11/04'
                        elif (game_week == '10') : game_date = '11/11'
                        elif (game_week == '11') : game_date = '11/18'
                        elif (game_week == '12') : game_date = '11/25'
                        elif (game_week == '13') : game_date = '12/02'
                        elif (game_week == '14') : game_date = '12/09'
                        elif (game_week == '15') : game_date = '12/16'
                        elif (game_week == '16') : game_date = '12/23'
                        elif (game_week == '17') : game_date = '12/30'
                        else : game_date = '99/99'

                        game_id = game_year + game_date + player_id
                        game_id = game_id.replace('/','')

                        game_opp = None
                        game_result = None
                        game_score = None
                        game_g = None
                        game_gs = None
                        game_rate = None
                        game_comp = None
                        game_pass_att = None
                        game_pct = None
                        game_pass_yds = None
                        game_pass_td = None
                        game_int = None
                        game_sck = None
                        game_sckY = None
                        game_rush_att = None
                        game_rush_yds = None
                        game_rush_td = None
                        game_fum = None
                        game_fum_lost = None

    
    
                    record = {}
                    record["playerId"] = player_id
                    record["playerFullName"] = player_full_name
                    record["playerFirstName"] = player_first_name
                    record["playerLastName"] = player_last_name
                    record["playerTeam"] = player_team
                    record["gameId"] = game_id
                    record["gameWeek"] = game_week
                    record["gameDate"] = game_date
                    record["gameOpp"] = game_opp
                    record["gameResult"] = game_result
                    record["gameScore"] = game_score
                    record["gameId"] = game_id
                    record["gameG"] = game_g
                    record["gameGS"] = game_gs
                    record["gameRate"] = game_rate
                    record["gameComp"] = game_comp
                    record["gamePassAtt"] = game_pass_att
                    record["gamePct"] = game_pct
                    record["gamePassYds"] = game_pass_yds
                    record["gamePassTd"] = game_pass_td
                    record["gameInt"] = game_int
                    record["gameSck"] = game_sck
                    record["gameSckY"] = game_sckY
                    record["gameRushAtt"] = game_rush_att
                    record["gameRushYds"] = game_rush_yds
                    record["gameRushTd"] = game_rush_td
                    record["gameFum"] = game_fum
                    record["gameFumLost"] = game_fum_lost
    
            
                    #print record
                    if record.has_key('gameId'):
                        # save records to the datastore
                        scraperwiki.sqlite.save(["gameId"], record)


import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

# this is the code to establish a schema. Only need it the first time I run.

#scraperwiki.sqlite.execute("drop table if exists `swdata`")
#scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`gameId` text, `playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `gameWeek` text, `gameDate` text, `gameOpp` text, `gameResult` text, `gameScore` text, `gameG` text, `gameGS` text, `gameComp` text, `gamePassAtt` text, `gamePct` text, `gamePassYds` text, `gamePassTd` text, `gameInt` text, `gameSck` text, `gameSckY` text, `gameRate` text, `gameRushAtt` text, `gameRushYds` text, `gameRushTd` text, `gameFum` text, `gameFumLost` text) ")


scraperwiki.sqlite.attach('nfl_quarterback_stats')

theQuarterbacks = scraperwiki.sqlite.select('* FROM `nfl_quarterback_stats`.swdata WHERE playerStatus = "ACT"')

for player in theQuarterbacks:
    player_id = player["playerId"]
    player_full_name = player["playerFullName"]
    player_first_name = player["playerFirstName"]
    player_last_name = player["playerLastName"]
    player_name_code = player["playerNameCode"]
    player_status = player["playerStatus"]
    player_url = player["playerUrl"]
    player_gamelog_url = player_url.replace('profile','gamelogs')
    player_gamelog_url += '?99'
    player_team = player["playerTeam"]
    player_position = player["playerPos"]
    player_uni_number = player["playerNum"]


    html1 = scraperwiki.scrape(player_gamelog_url)
    soup1 = BeautifulSoup(html1)

    print player_gamelog_url
    print soup1
    game_year = soup1.find('div',id='game-log-year').find('strong').text.replace('Game Log: ','')

    # The table with Regular Season stats does not have a unique ID. 
    # So we look for a header cell which says "Regular Season" and then find its parent TABLE.

    ## Some players may not have reg season stats yet. If so, exclude them.

    reg_season = soup1.find('td',text='Regular Season')
    if (reg_season):
        game_table = reg_season.findParents('table')[0]
    
        for section in game_table.findAll(re.compile('tbody'), recursive=False):
            for row in section.findAll('tr'):
                ## print (row)
                columns = row.findAll('td')
    
                ## We don't want to process rows that serve as decorative borders
                ## ie, <tr><td colspan="22" class="border-td" ></td></tr>
                ## We also don't want to process the Player-Totals row
                ## Searching for colspan in the first TD takes care of both cases
    
                if (not columns[0].has_key('colspan')): 
    

                    ## also have to watch out for Bye weeks

                    if (not columns[1].text == 'Bye'):

                        game_week = columns[0].text
                        game_date = columns[1].text
                        game_opp = columns[2].text.replace('\r','').replace('\n','').replace('\t','')
                
                        ## game_result = columns[3].find('span').text
                        game_result_raw = columns[3].text
                        game_result = game_result_raw[0]

                        game_score = columns[3].find('a').text
                        game_id = game_year + game_date + player_id
                        game_id = game_id.replace('/','')
            
                        ## begin stats
                        # these stats will always have a number
                        game_g = columns[4].text
                        game_gs = columns[5].text


                        # these stats might be blank
                        game_rate = columns[15].text
                        if (game_rate == '0.0' and game_g == '0') : game_rate = None
                        game_comp = columns[6].text
                        if (game_comp == '--') : game_comp = None
                        game_pass_att = columns[7].text
                        if (game_pass_att == '--') : game_pass_att = None
                        game_pct = columns[8].text
                        if (game_pct == '--') : game_pct = None
                        game_pass_yds = columns[9].text
                        if (game_pass_yds == '--') : game_pass_yds = None
                        game_pass_td = columns[11].text
                        if (game_pass_td == '--') : game_pass_td = None
                        game_int = columns[12].text
                        if (game_int == '--') : game_int = None
                        game_sck = columns[13].text
                        if (game_sck == '--') : game_sck = None
                        game_sckY = columns[14].text
                        if (game_sckY == '--') : game_sckY = None
                        game_rush_att = columns[16].text
                        if (game_rush_att == '--') : game_rush_att = None
                        game_rush_yds = columns[17].text
                        if (game_rush_yds == '--') : game_rush_yds = None
                        game_rush_td = columns[19].text
                        if (game_rush_td == '--') : game_rush_td = None
                        game_fum = columns[20].text
                        if (game_fum == '--') : game_fum = None
                        game_fum_lost = columns[20].text
                        if (game_fum_lost == '--') : game_fum_lost = None

                    else:
                        game_week = columns[0].text
                        if   (game_week == '1')  : game_date = '09/09'
                        elif (game_week == '2')  : game_date = '09/16'
                        elif (game_week == '3')  : game_date = '09/23'
                        elif (game_week == '4')  : game_date = '09/30'
                        elif (game_week == '5')  : game_date = '10/07'
                        elif (game_week == '6')  : game_date = '10/14'
                        elif (game_week == '7')  : game_date = '10/21'
                        elif (game_week == '8')  : game_date = '10/28'
                        elif (game_week == '9')  : game_date = '11/04'
                        elif (game_week == '10') : game_date = '11/11'
                        elif (game_week == '11') : game_date = '11/18'
                        elif (game_week == '12') : game_date = '11/25'
                        elif (game_week == '13') : game_date = '12/02'
                        elif (game_week == '14') : game_date = '12/09'
                        elif (game_week == '15') : game_date = '12/16'
                        elif (game_week == '16') : game_date = '12/23'
                        elif (game_week == '17') : game_date = '12/30'
                        else : game_date = '99/99'

                        game_id = game_year + game_date + player_id
                        game_id = game_id.replace('/','')

                        game_opp = None
                        game_result = None
                        game_score = None
                        game_g = None
                        game_gs = None
                        game_rate = None
                        game_comp = None
                        game_pass_att = None
                        game_pct = None
                        game_pass_yds = None
                        game_pass_td = None
                        game_int = None
                        game_sck = None
                        game_sckY = None
                        game_rush_att = None
                        game_rush_yds = None
                        game_rush_td = None
                        game_fum = None
                        game_fum_lost = None

    
    
                    record = {}
                    record["playerId"] = player_id
                    record["playerFullName"] = player_full_name
                    record["playerFirstName"] = player_first_name
                    record["playerLastName"] = player_last_name
                    record["playerTeam"] = player_team
                    record["gameId"] = game_id
                    record["gameWeek"] = game_week
                    record["gameDate"] = game_date
                    record["gameOpp"] = game_opp
                    record["gameResult"] = game_result
                    record["gameScore"] = game_score
                    record["gameId"] = game_id
                    record["gameG"] = game_g
                    record["gameGS"] = game_gs
                    record["gameRate"] = game_rate
                    record["gameComp"] = game_comp
                    record["gamePassAtt"] = game_pass_att
                    record["gamePct"] = game_pct
                    record["gamePassYds"] = game_pass_yds
                    record["gamePassTd"] = game_pass_td
                    record["gameInt"] = game_int
                    record["gameSck"] = game_sck
                    record["gameSckY"] = game_sckY
                    record["gameRushAtt"] = game_rush_att
                    record["gameRushYds"] = game_rush_yds
                    record["gameRushTd"] = game_rush_td
                    record["gameFum"] = game_fum
                    record["gameFumLost"] = game_fum_lost
    
            
                    #print record
                    if record.has_key('gameId'):
                        # save records to the datastore
                        scraperwiki.sqlite.save(["gameId"], record)


