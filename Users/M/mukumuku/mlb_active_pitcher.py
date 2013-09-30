import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `era` text, `g` text, `w` text, `l` text, `ip` text, `er` text, `pbb` text,  `pso` text, `pavg` text, `sho` text, `sv` text)")


scraperwiki.sqlite.attach('mlb_team_roster')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_team_roster`.swdata WHERE playerPos = "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player["playerId"]
    player_full_name = player["playerFullName"]
    player_first_name = player["playerFirstName"]
    player_last_name = player["playerLastName"]
    player_url = player["playerUrl"]
    player_team = player["playerTeam"]
    player_position = player["playerPos"]
    player_uni = player["playerUni"]


    if player_position == 'P':


        json_url = Template("http://mlb.mlb.com/lookup/json/named.sport_pitching_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_pitching_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
        json1 = scraperwiki.scrape(json_url)
        json_decode = demjson.decode(json1)

        career_len = int(json_decode['sport_pitching_composed']['sport_pitching_agg']['queryResults']['totalSize'])
        if career_len > 0:
            theRow = career_len - 1
            if theRow == 0:
                theStats = json_decode['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row']
            else:
                theStats = json_decode['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row'][theRow]
    
            record = {}
            record["playerId"] = player_id
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerFullName"] = player_full_name
            record["playerUrl"] = player_url
            record["playerTeam"] = player_team
            record["playerUni"] = player_uni
    
            record["era"] = theStats['era']
            record["g"] = theStats['g']
            record["w"] = theStats['w']
            record["l"] = theStats['l']
            record["ip"] = theStats['ip']
            record["er"] = theStats['er']
            record["pbb"] = theStats['bb']
            record["pso"] = theStats['so']
            record["pavg"] = theStats['avg']
            record["sho"] = theStats['sho']
            record["sv"] = theStats['sv']
    
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"],record)



import scraperwiki
import re
from string import Template
import demjson

# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerUni` text, `era` text, `g` text, `w` text, `l` text, `ip` text, `er` text, `pbb` text,  `pso` text, `pavg` text, `sho` text, `sv` text)")


scraperwiki.sqlite.attach('mlb_team_roster')

thePlayers = scraperwiki.sqlite.select('* FROM `mlb_team_roster`.swdata WHERE playerPos = "P" ORDER BY playerId ')

for player in thePlayers:
    player_id = player["playerId"]
    player_full_name = player["playerFullName"]
    player_first_name = player["playerFirstName"]
    player_last_name = player["playerLastName"]
    player_url = player["playerUrl"]
    player_team = player["playerTeam"]
    player_position = player["playerPos"]
    player_uni = player["playerUni"]


    if player_position == 'P':


        json_url = Template("http://mlb.mlb.com/lookup/json/named.sport_pitching_composed.bam?game_type='R'&sport_code='mlb'&sort_by='season_asc'&sport_pitching_composed.season=2012&player_id=$player_id").substitute(player_id=player_id)
        json1 = scraperwiki.scrape(json_url)
        json_decode = demjson.decode(json1)

        career_len = int(json_decode['sport_pitching_composed']['sport_pitching_agg']['queryResults']['totalSize'])
        if career_len > 0:
            theRow = career_len - 1
            if theRow == 0:
                theStats = json_decode['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row']
            else:
                theStats = json_decode['sport_pitching_composed']['sport_pitching_agg']['queryResults']['row'][theRow]
    
            record = {}
            record["playerId"] = player_id
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerFullName"] = player_full_name
            record["playerUrl"] = player_url
            record["playerTeam"] = player_team
            record["playerUni"] = player_uni
    
            record["era"] = theStats['era']
            record["g"] = theStats['g']
            record["w"] = theStats['w']
            record["l"] = theStats['l']
            record["ip"] = theStats['ip']
            record["er"] = theStats['er']
            record["pbb"] = theStats['bb']
            record["pso"] = theStats['so']
            record["pavg"] = theStats['avg']
            record["sho"] = theStats['sho']
            record["sv"] = theStats['sv']
    
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"],record)



