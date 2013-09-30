import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.execute('CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `g` text, `ab` text, `r` text, `h` text, `2b` text, `3b` text, `hr` text, `rbi` text, `bb` text, `ibb` text, `so` text, `sb` text, `avg` text, `slg` text, `p-g` text, `p-ab` text, `p-r` text, `p-h` text, `p-2b` text, `p-3b` text, `p-hr` text, `p-rbi` text, `p-bb` text, `p-ibb` text, `p-so` text, `p-sb` text, `p-avg` text, `p-slg` text)')


scraperwiki.sqlite.attach('mlb_division_series_player_list')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_division_series_player_list`.swdata WHERE playerPos != "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player['playerId']
    player_full_name = player['playerFullName']
    player_first_name = player['playerFirstName']
    player_last_name = player['playerLastName']
    player_url = player['playerUrl']
    player_team = player['playerTeamId']
    player_position = player['playerPos']
    player_uni = player['playerUni']


    json_url1 = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_hitting_postseason_summary.bam?game_type='F'&game_type='D'&game_type='L'&game_type='W'&sport_code='mlb'&season=2012&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(json_url1)
    json_decode1 = demjson.decode(json1)

    career_len1 = int(json_decode1['mlb_bio_hitting_postseason_summary']['mlb_individual_hitting_season']['queryResults']['totalSize'])
    if career_len1 > 0:
        theRow = career_len1 - 1
        if theRow == 0:
            postStats = json_decode1['mlb_bio_hitting_postseason_summary']['mlb_individual_hitting_season']['queryResults']['row']
        else:
            postStats = json_decode1['mlb_bio_hitting_postseason_summary']['mlb_individual_hitting_season']['row'][theRow]



    json_url2 = Template("http://mlb.mlb.com/lookup/json/named.sport_hitting_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_hitting_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
    json2 = scraperwiki.scrape(json_url2)
    json_decode2 = demjson.decode(json2)

    career_len2 = int(json_decode2['sport_hitting_composed']['sport_hitting_tm']['queryResults']['totalSize'])
    if career_len2 > 0:
        theRow = career_len2 - 1
        if theRow == 0:
            theStats = json_decode2['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row']
        else:
            theStats = json_decode2['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row'][theRow]

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
        record['slg'] = theStats['slg']

        record['p-g'] = postStats['g']
        record['p-ab'] = postStats['ab']
        record['p-r'] = postStats['r']
        record['p-h'] = postStats['h']
        record['p-2b'] = postStats['h2b']
        record['p-3b'] = postStats['h3b']
        record['p-hr'] = postStats['hr']
        record['p-rbi'] = postStats['rbi']
        record['p-bb'] = postStats['bb']
        record['p-ibb'] = postStats['ibb']
        record['p-so'] = postStats['so']
        record['p-sb'] = postStats['sb']
        record['p-avg'] = postStats['avg']
        record['p-slg'] = postStats['slg']





        #print record
        if record.has_key('playerId'):
            # save records to the datastore
                scraperwiki.sqlite.save(['playerId'],record)



import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.execute('CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `g` text, `ab` text, `r` text, `h` text, `2b` text, `3b` text, `hr` text, `rbi` text, `bb` text, `ibb` text, `so` text, `sb` text, `avg` text, `slg` text, `p-g` text, `p-ab` text, `p-r` text, `p-h` text, `p-2b` text, `p-3b` text, `p-hr` text, `p-rbi` text, `p-bb` text, `p-ibb` text, `p-so` text, `p-sb` text, `p-avg` text, `p-slg` text)')


scraperwiki.sqlite.attach('mlb_division_series_player_list')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_division_series_player_list`.swdata WHERE playerPos != "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player['playerId']
    player_full_name = player['playerFullName']
    player_first_name = player['playerFirstName']
    player_last_name = player['playerLastName']
    player_url = player['playerUrl']
    player_team = player['playerTeamId']
    player_position = player['playerPos']
    player_uni = player['playerUni']


    json_url1 = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_hitting_postseason_summary.bam?game_type='F'&game_type='D'&game_type='L'&game_type='W'&sport_code='mlb'&season=2012&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(json_url1)
    json_decode1 = demjson.decode(json1)

    career_len1 = int(json_decode1['mlb_bio_hitting_postseason_summary']['mlb_individual_hitting_season']['queryResults']['totalSize'])
    if career_len1 > 0:
        theRow = career_len1 - 1
        if theRow == 0:
            postStats = json_decode1['mlb_bio_hitting_postseason_summary']['mlb_individual_hitting_season']['queryResults']['row']
        else:
            postStats = json_decode1['mlb_bio_hitting_postseason_summary']['mlb_individual_hitting_season']['row'][theRow]



    json_url2 = Template("http://mlb.mlb.com/lookup/json/named.sport_hitting_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_hitting_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
    json2 = scraperwiki.scrape(json_url2)
    json_decode2 = demjson.decode(json2)

    career_len2 = int(json_decode2['sport_hitting_composed']['sport_hitting_tm']['queryResults']['totalSize'])
    if career_len2 > 0:
        theRow = career_len2 - 1
        if theRow == 0:
            theStats = json_decode2['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row']
        else:
            theStats = json_decode2['sport_hitting_composed']['sport_hitting_tm']['queryResults']['row'][theRow]

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
        record['slg'] = theStats['slg']

        record['p-g'] = postStats['g']
        record['p-ab'] = postStats['ab']
        record['p-r'] = postStats['r']
        record['p-h'] = postStats['h']
        record['p-2b'] = postStats['h2b']
        record['p-3b'] = postStats['h3b']
        record['p-hr'] = postStats['hr']
        record['p-rbi'] = postStats['rbi']
        record['p-bb'] = postStats['bb']
        record['p-ibb'] = postStats['ibb']
        record['p-so'] = postStats['so']
        record['p-sb'] = postStats['sb']
        record['p-avg'] = postStats['avg']
        record['p-slg'] = postStats['slg']





        #print record
        if record.has_key('playerId'):
            # save records to the datastore
                scraperwiki.sqlite.save(['playerId'],record)



