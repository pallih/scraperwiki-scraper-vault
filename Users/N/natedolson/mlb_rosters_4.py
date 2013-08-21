import scraperwiki
import re
from string import Template
import demjson

scraperwiki.sqlite.execute('drop table if exists `swdata`')

#MLB Teams:
#108 ana
#109 ari
#110 bal
#111 bos
#112 chc
#113 cin
#114 cle
#115 col
#116 det
#117 hou
#118 kc
#119 la
#120 was
#121 nym
#133 oak
#134 pit
#135 sd
#136 sea
#137 sf
#138 stl
#139 tb
#140 tex
#141 tor
#142 min
#143 phi
#144 atl
#145 cws
#146 mia
#147 nyy
#158 mil

for team in range (108,160) :
    page_url = Template("http://mlb.mlb.com/lookup/json/named.roster_40.bam?team_id=$team").substitute(team=team)
    json1 = scraperwiki.scrape(page_url)
    json_decode1 = demjson.decode(json1)

    roster_len = int(json_decode1['roster_40']['queryResults']['totalSize'])
    if roster_len > 0 :
        players = json_decode1['roster_40']['queryResults']['row']
        for i in range (0,roster_len) :
            record = {}
            record['key'] = players[i]['player_id']
            record['player_id'] = players[i]['player_id']
            record['status_code'] = players[i]['status_code']
            record['primary_position'] = players[i]['primary_position']
            record['position_txt'] = players[i]['position_txt']
            record['name_display_first_last'] = players[i]['name_display_first_last']
            record['name_display_last_first'] = players[i]['name_display_last_first']
            record['name_first'] = players[i]['name_first']
            record['name_last'] = players[i]['name_last']
            record['name_full'] = players[i]['name_full']
            record['name'] = players[i]['name_first'] + " " + players[i]['name_last']
            record['jersey_number'] = players[i]['jersey_number']
            record['team_id'] = players[i]['team_id']
            record['team_code'] = players[i]['team_code']
            record['team_abbrev'] =  players[i]['team_abbrev']
            record['throws'] = players[i]['throws']
            record['bats'] = players[i]['bats']
            if players[i]['primary_position'] == '1':
                    pos_long_txt = 'Pitcher'
            elif players[i]['primary_position'] == '2':
                    pos_long_txt = 'Catcher'
            elif players[i]['primary_position'] == '3' or players[i]['primary_position'] == '4' or players[i]['primary_position'] == '5' or players[i]['primary_position'] == '6':
                    pos_long_txt = 'Infielder'
            elif players[i]['primary_position'] == '7' or players[i]['primary_position'] == '8' or players[i]['primary_position'] == '9' or players[i]['primary_position'] == 'O':
                    pos_long_txt = 'Outfielder'
                    record['position_txt'] = 'OF'
            record['pos_long_txt'] = pos_long_txt
        

            if record.has_key('key'):
                # save records to the datastore
                scraperwiki.sqlite.save(['key'],record)

