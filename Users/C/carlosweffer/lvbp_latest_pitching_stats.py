import scraperwiki
import re
from string import Template
import demjson

scraperwiki.sqlite.execute('drop table if exists `swdata`')
scraperwiki.sqlite.attach('lvbp_rosters')
thePlayers = scraperwiki.sqlite.select('player_id from `lvbp_rosters`.`swdata` where `primary_position` = "1" order by player_id')
#Excluding player 150208 and 433589: problem with game 350115 : hits = ''
#thePlayers = scraperwiki.sqlite.select('player_id from `lvbp_rosters`.`swdata` where `primary_position` = "1" and player_id <> "150208" and player_id <> "433589" order by player_id')

for player in thePlayers:
    player_id = player['player_id']
#for n in range (0,1) : 
#    player_id = 489296

#TWO Latest batting stats: results=2
    page_url = Template("http://mlb.com/lookup/json/named.minors_bio_page_pitching.bam?season=2012&num_games=2&game_type='R'&league_id=135&player_id=$player_id").substitute(player_id=player_id)
    json1 = scraperwiki.scrape(page_url)
    json_decode1 = demjson.decode(json1)

    latest_len = int(json_decode1['minors_bio_page_pitching']['minors_stats_pitching_previous_games']['queryResults']['totalSize'])
    if latest_len > 1 :
            
            theGames = json_decode1['minors_bio_page_pitching']['minors_stats_pitching_previous_games']['queryResults']['row']
            for i in range (0,latest_len-1) :

                    record = {}
                    record['playerId'] = player_id
                    record['team_id'] = theGames[i]['team_id']
                    record['opponent_id'] = theGames[i]['opponent_id']
                    record['key'] = theGames[i]['game_pk'] + str(player_id)
                
                #Skip a game
                #gamepk = theGames[i]['game_pk']
                #if gamepk.find('350154') < 0 :
    
                    gs = theGames[i]['gs']
                    w = int(theGames[i]['w']) 
                    l = int(theGames[i]['l'])
                    er = int(theGames[i]['er'])
                    hr = int(theGames[i]['hr'])
                    h = int(theGames[i]['h'])
                    sv = int(theGames[i]['sv'])
                    bb = int(theGames[i]['bb'])
                    so = int(theGames[i]['so'])
                    hbp = int(theGames[i]['hb'])
                    cg = int(theGames[i]['cg'])
                    sho = int(theGames[i]['sho'])
                    ip = theGames[i]['ip']

                    game_date_split = theGames[i]['game_date'].split('-')
                    date_display_split = theGames[i]['game_date_display'].split(' ')
                    game_date = game_date_split[0] + game_date_split[1] + date_display_split[1]
                    record['game_id_date'] = game_date
                    record['cal_date']  = theGames[i]['game_date_display']
                    record['game_pk'] = theGames[i]['game_pk']
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