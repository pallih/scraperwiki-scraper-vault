import scraperwiki

import json
import urllib2
import csv
from pprint import pprint
import re
import HTMLParser
import dateutil.parser

daily_mirror_players = 'https://fantasyfootball.mirror.co.uk/json/players/'


teams= ["LIV","SWA","SOT","REA","NOR","TOT","EVE","AVL","FUL","STO","WHM","WBA","LYN","SUN","WIG","BCA","QPR","MUN","NEW","MCY","CHE","ARS"]
# import the gameweeks

pos = {0:'GK',1:'STR',2:'MID',3:'DEF'}

def import_players():
    met = urllib2.urlopen(daily_mirror_players)
    mirror_players = json.load(met)
    
    
    all_players = []
    for i in range(0,4):
        for player_data in mirror_players['players'][i]:
            
            team = mirror_players['team'][player_data[2]]
            if team not in teams:
                continue
            price = player_data[3]
            name = player_data[1].replace(',','')
            position = i
            mirror_id = player_data[0]
          
            player_data_rankings = { 
                        'id' : mirror_id, 
                        'team' : team, 
                        'name' : name, 
                        'price' : price, 
                        'position' : pos[position], 
                    }
               
            scraperwiki.sqlite.save(unique_keys=['id'], data=player_data_rankings, table_name='players')


def main():
    import_players()

main()

