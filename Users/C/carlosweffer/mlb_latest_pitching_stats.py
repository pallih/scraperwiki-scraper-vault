import scraperwiki
import re
from string import Template
import demjson

#remove the drop table line if you want to maintain all the games in the table
scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.attach('mlb_rosters_3')
thePlayers = scraperwiki.sqlite.select('player_id from `mlb_rosters_3`.`swdata` where `primary_position` = "1" order by player_id')

for player in thePlayers:
    player_id = player['player_id']

#for n in range (0,1) : 
#    player_id = 433587

#TWO Latest batting stats: results=2
    page_url = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_pitching_last_10.bam?results=5&season=2013&game_type='R'&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(page_url)
    json_decode1 = demjson.decode(json1)

    if int(json_decode1['mlb_bio_pitching_last_10']['mlb_individual_pitching_last_x_total']['queryResults']['totalSize']) > 0 :
        latest_len = int(json_decode1['mlb_bio_pitching_last_10']['mlb_individual_pitching_game_log']['queryResults']['totalSize'])
        if latest_len > 0 :
            
            theGames = json_decode1['mlb_bio_pitching_last_10']['mlb_individual_pitching_game_log']['queryResults']['row']
            if latest_len == 1 :
                    record = {}
                    record['playerId'] = player_id
                    record['game_id'] = theGames['game_id']
                    record['opponent_id'] = theGames['opp_team_id']
                    record['key'] = theGames['game_pk'] + str(player_id)

                    gs = theGames['gs']
                    w = int(theGames['w']) 
                    l = int(theGames['l'])
                    er = int(theGames['er'])
                    hr = int(theGames['hr'])
                    
                    h = int(theGames['h'])
                    
                    # print record['key']
                    # print h

                    sv = int(theGames['sv'])
                    bb = int(theGames['bb'])
                    so = int(theGames['so'])
                    hbp = int(theGames['hb'])
                    cg = int(theGames['cg'])
                    sho = int(theGames['sho'])
                    ip = theGames['ip']

                    game_id_split = theGames['game_id'].split('/')
                    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames['date']
                    record['game_pk'] = theGames['game_pk']
                    record['home_away'] = theGames['home_away']
                    record['g'] = 1
                    record['gs'] = gs
                    record['w'] = w
                    record['l'] = l
                    record['er'] = er
                    record['hr'] = hr
                    record['h'] = h
                    record['sv'] = sv
                    record['bb'] = bb
                    record['so'] = so
                    record['hbp'] = hbp
                    record['cg'] = cg
                    record['sho'] = sho
                    record['ip'] = ip          
                    
                    if ip.find('.') < 0 :
                        ipw = int(ip)
                        iph = 0
                    else :
                        ip_split = ip.split('.')
                        ipw = int(ip_split[0])
                        iph = int(ip_split[1])
                    
                    if (cg == 1 and h==0 and w==1) :
                        nhnr = 1
                    else : 
                        nhnr = 0

                    record['nhnr'] = nhnr
                    record['points'] = (ipw * 2) + (iph * 0.667) + so + (w * 8) + (sv * 5) + (cg * 5) - (l * 5) - (er * 2) - bb - h + (nhnr * 20)

                    if record.has_key('key'):
                        # save record to the datastore
                        scraperwiki.sqlite.save(['key'],record)

            
            else :

                for i in range (0,latest_len) :

                    record = {}
                    record['playerId'] = player_id
                    record['game_id'] = theGames[i]['game_id']
                    record['opponent_id'] = theGames[i]['opp_team_id']
                    record['key'] = theGames[i]['game_pk'] + str(player_id)
                    
                    gs = theGames[i]['gs']
                    w = int(theGames[i]['w']) 
                    l = int(theGames[i]['l'])
                    er = int(theGames[i]['er'])
                    hr = int(theGames[i]['hr'])

                    #Fix error h="" - occurs when scrapper is executed while baseball games in progress
                    if theGames[i]['h'] == "" :
                        h = int(0)
                    else :
                        h = int(theGames[i]['h'])
                    
                    sv = int(theGames[i]['sv'])
                    bb = int(theGames[i]['bb'])
                    so = int(theGames[i]['so'])
                    hbp = int(theGames[i]['hb'])
                    cg = int(theGames[i]['cg'])
                    sho = int(theGames[i]['sho'])
                    ip = theGames[i]['ip']

                    game_id_split = theGames[i]['game_id'].split('/')
                    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames[i]['date']
                    record['game_pk'] = theGames[i]['game_pk']
                    record['game_pk'] = theGames[i]['game_pk']
                    record['home_away'] = theGames[i]['home_away']
                    record['g'] = 1
                    record['gs'] = gs
                    record['w'] = w
                    record['l'] = l
                    record['er'] = er
                    record['hr'] = hr   
                    record['h'] = h
                    record['sv'] = sv
                    record['bb'] = bb
                    record['so'] = so
                    record['hbp'] = hbp
                    record['cg'] = cg
                    record['sho'] = sho
                    record['ip'] = ip              
                    
                    if ip.find('.') < 0 :
                        ipw = int(ip)
                        iph = 0
                    else :
                        ip_split = ip.split('.')
                        ipw = int(ip_split[0])
                        iph = int(ip_split[1])
                         
                    if (cg == 1 and h==0 and w==1 and er==0) :
                        nhnr = 1
                    else : 
                        nhnr = 0
                    
                    record['nhnr'] = nhnr
                    record['points'] = (ipw * 2) + (iph * 0.667) + so + (w * 8) + (sv * 5) + (cg * 5) - (l * 5) - (er * 2) - bb - h + (nhnr * 20)
            
                    if record.has_key('key'):
                    # save records to the datastore
                        scraperwiki.sqlite.save(['key'],record)import scraperwiki
import re
from string import Template
import demjson

#remove the drop table line if you want to maintain all the games in the table
scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.attach('mlb_rosters_3')
thePlayers = scraperwiki.sqlite.select('player_id from `mlb_rosters_3`.`swdata` where `primary_position` = "1" order by player_id')

for player in thePlayers:
    player_id = player['player_id']

#for n in range (0,1) : 
#    player_id = 433587

#TWO Latest batting stats: results=2
    page_url = Template("http://mlb.mlb.com/lookup/json/named.mlb_bio_pitching_last_10.bam?results=5&season=2013&game_type='R'&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(page_url)
    json_decode1 = demjson.decode(json1)

    if int(json_decode1['mlb_bio_pitching_last_10']['mlb_individual_pitching_last_x_total']['queryResults']['totalSize']) > 0 :
        latest_len = int(json_decode1['mlb_bio_pitching_last_10']['mlb_individual_pitching_game_log']['queryResults']['totalSize'])
        if latest_len > 0 :
            
            theGames = json_decode1['mlb_bio_pitching_last_10']['mlb_individual_pitching_game_log']['queryResults']['row']
            if latest_len == 1 :
                    record = {}
                    record['playerId'] = player_id
                    record['game_id'] = theGames['game_id']
                    record['opponent_id'] = theGames['opp_team_id']
                    record['key'] = theGames['game_pk'] + str(player_id)

                    gs = theGames['gs']
                    w = int(theGames['w']) 
                    l = int(theGames['l'])
                    er = int(theGames['er'])
                    hr = int(theGames['hr'])
                    
                    h = int(theGames['h'])
                    
                    # print record['key']
                    # print h

                    sv = int(theGames['sv'])
                    bb = int(theGames['bb'])
                    so = int(theGames['so'])
                    hbp = int(theGames['hb'])
                    cg = int(theGames['cg'])
                    sho = int(theGames['sho'])
                    ip = theGames['ip']

                    game_id_split = theGames['game_id'].split('/')
                    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames['date']
                    record['game_pk'] = theGames['game_pk']
                    record['home_away'] = theGames['home_away']
                    record['g'] = 1
                    record['gs'] = gs
                    record['w'] = w
                    record['l'] = l
                    record['er'] = er
                    record['hr'] = hr
                    record['h'] = h
                    record['sv'] = sv
                    record['bb'] = bb
                    record['so'] = so
                    record['hbp'] = hbp
                    record['cg'] = cg
                    record['sho'] = sho
                    record['ip'] = ip          
                    
                    if ip.find('.') < 0 :
                        ipw = int(ip)
                        iph = 0
                    else :
                        ip_split = ip.split('.')
                        ipw = int(ip_split[0])
                        iph = int(ip_split[1])
                    
                    if (cg == 1 and h==0 and w==1) :
                        nhnr = 1
                    else : 
                        nhnr = 0

                    record['nhnr'] = nhnr
                    record['points'] = (ipw * 2) + (iph * 0.667) + so + (w * 8) + (sv * 5) + (cg * 5) - (l * 5) - (er * 2) - bb - h + (nhnr * 20)

                    if record.has_key('key'):
                        # save record to the datastore
                        scraperwiki.sqlite.save(['key'],record)

            
            else :

                for i in range (0,latest_len) :

                    record = {}
                    record['playerId'] = player_id
                    record['game_id'] = theGames[i]['game_id']
                    record['opponent_id'] = theGames[i]['opp_team_id']
                    record['key'] = theGames[i]['game_pk'] + str(player_id)
                    
                    gs = theGames[i]['gs']
                    w = int(theGames[i]['w']) 
                    l = int(theGames[i]['l'])
                    er = int(theGames[i]['er'])
                    hr = int(theGames[i]['hr'])

                    #Fix error h="" - occurs when scrapper is executed while baseball games in progress
                    if theGames[i]['h'] == "" :
                        h = int(0)
                    else :
                        h = int(theGames[i]['h'])
                    
                    sv = int(theGames[i]['sv'])
                    bb = int(theGames[i]['bb'])
                    so = int(theGames[i]['so'])
                    hbp = int(theGames[i]['hb'])
                    cg = int(theGames[i]['cg'])
                    sho = int(theGames[i]['sho'])
                    ip = theGames[i]['ip']

                    game_id_split = theGames[i]['game_id'].split('/')
                    game_date = game_id_split[0] + game_id_split[1] + game_id_split[2]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames[i]['date']
                    record['game_pk'] = theGames[i]['game_pk']
                    record['game_pk'] = theGames[i]['game_pk']
                    record['home_away'] = theGames[i]['home_away']
                    record['g'] = 1
                    record['gs'] = gs
                    record['w'] = w
                    record['l'] = l
                    record['er'] = er
                    record['hr'] = hr   
                    record['h'] = h
                    record['sv'] = sv
                    record['bb'] = bb
                    record['so'] = so
                    record['hbp'] = hbp
                    record['cg'] = cg
                    record['sho'] = sho
                    record['ip'] = ip              
                    
                    if ip.find('.') < 0 :
                        ipw = int(ip)
                        iph = 0
                    else :
                        ip_split = ip.split('.')
                        ipw = int(ip_split[0])
                        iph = int(ip_split[1])
                         
                    if (cg == 1 and h==0 and w==1 and er==0) :
                        nhnr = 1
                    else : 
                        nhnr = 0
                    
                    record['nhnr'] = nhnr
                    record['points'] = (ipw * 2) + (iph * 0.667) + so + (w * 8) + (sv * 5) + (cg * 5) - (l * 5) - (er * 2) - bb - h + (nhnr * 20)
            
                    if record.has_key('key'):
                    # save records to the datastore
                        scraperwiki.sqlite.save(['key'],record)