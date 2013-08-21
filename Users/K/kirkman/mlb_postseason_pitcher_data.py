import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `era` text, `g` text, `w` text, `l` text, `ip` text, `er` text, `pbb` text,  `pso` text, `pavg` text, `sho` text, `sv` text)")


scraperwiki.sqlite.attach('mlb_division_series_player_list')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_division_series_player_list`.swdata WHERE playerPos = "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player['playerId']
    player_full_name = player['playerFullName']
    player_first_name = player['playerFirstName']
    player_last_name = player['playerLastName']
    player_url = player['playerUrl']
    player_team = player['playerTeam']
    player_position = player['playerPos']
    player_uni = player['playerUni']


    if player_position == 'P':


        json_url1 = Template("http://mlb.mlb.com/lookup/json/named.sport_pitching_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_pitching_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
        json1 = scraperwiki.scrape(json_url1)
        json_decode1 = demjson.decode(json1)

        career_len1 = int(json_decode1['sport_pitching_composed']['sport_pitching_agg']['queryResults']['totalSize'])
        if career_len1 > 0:
            theRow1 = career_len1 - 1
            if theRow1 == 0:
                theStats = json_decode1['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row']
            else:
                theStats = json_decode1['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row'][theRow1]
    

        json_url2 = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_pitching_postseason_summary.bam?game_type='F'&game_type='D'&game_type='L'&game_type='W'&sport_code='mlb'&season=2012&player_id=$player_id").substitute(player_id=player_id)
        json2 = scraperwiki.scrape(json_url2)
        json_decode2 = demjson.decode(json2)

        career_len2 = int(json_decode2['mlb_bio_pitching_postseason_summary']['mlb_individual_pitching_season']['queryResults']['totalSize'])
        if career_len2 > 0:
            theRow2 = career_len2 - 1
            if theRow2 == 0:
                postStats = json_decode2['mlb_bio_pitching_postseason_summary']['mlb_individual_pitching_season']['queryResults']['row']
            else:
                postStats = json_decode2['mlb_bio_pitching_postseason_summary']['mlb_individual_pitching_season']['queryResults']['row'][theRow2]


            record = {}
            record['playerId'] = player_id
            record['playerFirstName'] = player_first_name
            record['playerLastName'] = player_last_name
            record['playerFullName'] = player_full_name
            record['playerUrl'] = player_url
            record['playerTeam'] = player_team
            record['playerUni'] = player_uni
    
            record['era'] = theStats['era']
            record['g'] = theStats['g']
            record['w'] = theStats['w']
            record['l'] = theStats['l']
            record['ip'] = theStats['ip']
            record['er'] = theStats['er']
            record['pbb'] = theStats['bb']
            record['pso'] = theStats['so']
            record['pavg'] = theStats['avg']
            record['sho'] = theStats['sho']
            record['sv'] = theStats['sv']

            record['p-era'] = postStats['era']
            record['p-g'] = postStats['g']
            record['p-w'] = postStats['w']
            record['p-l'] = postStats['l']
            record['p-ip'] = postStats['ip']
            record['p-er'] = postStats['er']
            record['p-pbb'] = postStats['bb']
            record['p-pso'] = postStats['so']
            record['p-pavg'] = postStats['avg']
            record['p-sho'] = postStats['sho']
            record['p-sv'] = postStats['sv']
    
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(['playerId'],record)



import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `era` text, `g` text, `w` text, `l` text, `ip` text, `er` text, `pbb` text,  `pso` text, `pavg` text, `sho` text, `sv` text)")


scraperwiki.sqlite.attach('mlb_division_series_player_list')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_division_series_player_list`.swdata WHERE playerPos = "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player['playerId']
    player_full_name = player['playerFullName']
    player_first_name = player['playerFirstName']
    player_last_name = player['playerLastName']
    player_url = player['playerUrl']
    player_team = player['playerTeam']
    player_position = player['playerPos']
    player_uni = player['playerUni']


    if player_position == 'P':


        json_url1 = Template("http://mlb.mlb.com/lookup/json/named.sport_pitching_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_pitching_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
        json1 = scraperwiki.scrape(json_url1)
        json_decode1 = demjson.decode(json1)

        career_len1 = int(json_decode1['sport_pitching_composed']['sport_pitching_agg']['queryResults']['totalSize'])
        if career_len1 > 0:
            theRow1 = career_len1 - 1
            if theRow1 == 0:
                theStats = json_decode1['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row']
            else:
                theStats = json_decode1['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row'][theRow1]
    

        json_url2 = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_pitching_postseason_summary.bam?game_type='F'&game_type='D'&game_type='L'&game_type='W'&sport_code='mlb'&season=2012&player_id=$player_id").substitute(player_id=player_id)
        json2 = scraperwiki.scrape(json_url2)
        json_decode2 = demjson.decode(json2)

        career_len2 = int(json_decode2['mlb_bio_pitching_postseason_summary']['mlb_individual_pitching_season']['queryResults']['totalSize'])
        if career_len2 > 0:
            theRow2 = career_len2 - 1
            if theRow2 == 0:
                postStats = json_decode2['mlb_bio_pitching_postseason_summary']['mlb_individual_pitching_season']['queryResults']['row']
            else:
                postStats = json_decode2['mlb_bio_pitching_postseason_summary']['mlb_individual_pitching_season']['queryResults']['row'][theRow2]


            record = {}
            record['playerId'] = player_id
            record['playerFirstName'] = player_first_name
            record['playerLastName'] = player_last_name
            record['playerFullName'] = player_full_name
            record['playerUrl'] = player_url
            record['playerTeam'] = player_team
            record['playerUni'] = player_uni
    
            record['era'] = theStats['era']
            record['g'] = theStats['g']
            record['w'] = theStats['w']
            record['l'] = theStats['l']
            record['ip'] = theStats['ip']
            record['er'] = theStats['er']
            record['pbb'] = theStats['bb']
            record['pso'] = theStats['so']
            record['pavg'] = theStats['avg']
            record['sho'] = theStats['sho']
            record['sv'] = theStats['sv']

            record['p-era'] = postStats['era']
            record['p-g'] = postStats['g']
            record['p-w'] = postStats['w']
            record['p-l'] = postStats['l']
            record['p-ip'] = postStats['ip']
            record['p-er'] = postStats['er']
            record['p-pbb'] = postStats['bb']
            record['p-pso'] = postStats['so']
            record['p-pavg'] = postStats['avg']
            record['p-sho'] = postStats['sho']
            record['p-sv'] = postStats['sv']
    
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(['playerId'],record)



