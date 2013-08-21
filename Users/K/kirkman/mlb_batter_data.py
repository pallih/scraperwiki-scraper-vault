import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

#scraperwiki.sqlite.execute('drop table if exists `swdata`')
#scraperwiki.sqlite.execute('CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `g` text, `ab` text, `r` text, `h` text, `2b` text, `3b` text, `hr` text, `rbi` text, `bb` text, `ibb` text, `so` text, `sb` text, `avg` text)')


scraperwiki.sqlite.attach('mlb_team_roster')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_team_roster`.swdata WHERE playerPos != "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player['playerId']
    player_full_name = player['playerFullName']
    player_first_name = player['playerFirstName']
    player_last_name = player['playerLastName']
    player_url = player['playerUrl']
    player_team = player['playerTeam']
    player_position = player['playerPos']
    player_uni = player['playerUni']


    json_url = Template("http://mlb.mlb.com/lookup/json/named.sport_hitting_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_hitting_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(json_url)
    json_decode = demjson.decode(json1)

    career_len = int(json_decode['sport_hitting_composed']['sport_hitting_tm']['queryResults']['totalSize'])
    if career_len > 0:
        theRow = career_len - 1
        if theRow == 0:
            theStats = json_decode['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row']
        else:
            theStats = json_decode['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row'][theRow]

        record = {}
        record['playerId'] = player_id
        record['playerFirstName'] = player_first_name
        record['playerLastName'] = player_last_name
        record['playerFullName'] = player_full_name
        record['playerUrl'] = player_url
        record['playerTeam'] = player_team
        record['playerUni'] = player_uni

        record['g'] = theStats['g']
        record['ab'] = theStats['ab']
        record['r'] = theStats['r']
        record['h'] = theStats['h']
        record['2b'] = theStats['d']
        record['3b'] = theStats['t']
        record['hr'] = theStats['hr']
        record['rbi'] = theStats['rbi']
        record['bb'] = theStats['bb']
        record['ibb'] = theStats['ibb']
        record['so'] = theStats['so']
        record['sb'] = theStats['sb']
        record['avg'] = theStats['avg']




        #print record
        if record.has_key('playerId'):
            # save records to the datastore
                scraperwiki.sqlite.save(['playerId'],record)



import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

#scraperwiki.sqlite.execute('drop table if exists `swdata`')
#scraperwiki.sqlite.execute('CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `g` text, `ab` text, `r` text, `h` text, `2b` text, `3b` text, `hr` text, `rbi` text, `bb` text, `ibb` text, `so` text, `sb` text, `avg` text)')


scraperwiki.sqlite.attach('mlb_team_roster')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_team_roster`.swdata WHERE playerPos != "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player['playerId']
    player_full_name = player['playerFullName']
    player_first_name = player['playerFirstName']
    player_last_name = player['playerLastName']
    player_url = player['playerUrl']
    player_team = player['playerTeam']
    player_position = player['playerPos']
    player_uni = player['playerUni']


    json_url = Template("http://mlb.mlb.com/lookup/json/named.sport_hitting_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_hitting_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(json_url)
    json_decode = demjson.decode(json1)

    career_len = int(json_decode['sport_hitting_composed']['sport_hitting_tm']['queryResults']['totalSize'])
    if career_len > 0:
        theRow = career_len - 1
        if theRow == 0:
            theStats = json_decode['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row']
        else:
            theStats = json_decode['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row'][theRow]

        record = {}
        record['playerId'] = player_id
        record['playerFirstName'] = player_first_name
        record['playerLastName'] = player_last_name
        record['playerFullName'] = player_full_name
        record['playerUrl'] = player_url
        record['playerTeam'] = player_team
        record['playerUni'] = player_uni

        record['g'] = theStats['g']
        record['ab'] = theStats['ab']
        record['r'] = theStats['r']
        record['h'] = theStats['h']
        record['2b'] = theStats['d']
        record['3b'] = theStats['t']
        record['hr'] = theStats['hr']
        record['rbi'] = theStats['rbi']
        record['bb'] = theStats['bb']
        record['ibb'] = theStats['ibb']
        record['so'] = theStats['so']
        record['sb'] = theStats['sb']
        record['avg'] = theStats['avg']




        #print record
        if record.has_key('playerId'):
            # save records to the datastore
                scraperwiki.sqlite.save(['playerId'],record)



