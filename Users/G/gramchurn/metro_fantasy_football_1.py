import scraperwiki

import json
import urllib2
import csv
from pprint import pprint
import re
import HTMLParser
import dateutil.parser

metro_gameweeks_url = "http://fantasyfootball.metro.co.uk/fixtures.json?matchWeekId="
metro_players_url = 'http://fantasyfootball.metro.co.uk/newTeam.json?url=%2FnewTeam.json&templateId=1&_=1345214042000'
metro_rankings_url = 'http://fantasyfootball.metro.co.uk/rankings.json?competitionId=1&seasonId=13&measure=Fantasy+Points&offset=0&limit=553'

def get_metro_manager_rankings_url(off,lim):
    metro_manager_rankings_url = 'http://fantasyfootball.metro.co.uk/leaderboards.json?tournamentId=19994&offset='+str(off)+'&limit='+str(lim)
    return metro_manager_rankings_url


# import the gameweeks
def import_gameweeks():
    for i in range (1,39):
        data = urllib2.urlopen(metro_gameweeks_url+str(i))
        fixture_data = json.load(data)['fixtures']
        
        for k in fixture_data:
            week_date = dateutil.parser.parse(k['s']).date() 
            teams = k['n'].split(' v ')
            gameweek = {
                'week_no' : i,
                'date' : week_date,
                'id' : k['id'],
                'home_team' : teams[0].strip(),
                'away_team' : teams[1].strip(),
                }

            scraperwiki.sqlite.save(unique_keys=['id'], data=gameweek, table_name='gameweeks')


def import_players():
    met = urllib2.urlopen(metro_players_url)
    metro_players = json.load(met)
    
    met = urllib2.urlopen(metro_rankings_url)
    rankings = json.load(met)
        
    
    all_players = []
    
    for player_data in metro_players['players']:
        price = player_data['pr']
        metro_name = player_data['n'].replace(',','')
        position = player_data['p']+1
        metro_id = player_data['id']
        note = ''
        if str(metro_id) in metro_players['notes']:
            note = metro_players['notes'][str(metro_id)]['ty']+'-'+metro_players['notes'][str(metro_id)]['e']
        team = metro_players['teams'][str(player_data['t'])]['n']
        
        #print metro_name
        for player_data in rankings['rankings']:
            if metro_name == player_data['name'].replace(',',''):
                rating = player_data['rating']
                name = player_data['name'].replace(',','')
                break
            name = metro_name
        player_data_rankings = { 
                    'id' : metro_id, 
                    'team' : team, 
                    'name' : name, 
                    'price' : price, 
                    'position' : position, 
                    'rating' : rating, 
                    'info' : note
                }
           
        scraperwiki.sqlite.save(unique_keys=['id'], data=player_data_rankings, table_name='players')

def import_manager_standings():
    k = 20
    limit = 2*k
    for offset in range(0,80000,k):
        
        met = urllib2.urlopen(get_metro_manager_rankings_url(offset,limit))
        metro_managers = json.load(met)
        standings = metro_managers['standings'] 
        for person in standings:
            manager_data = {
                'appearance' : person['appearance'],
                'attack' : person['attack'],
                'buyin' : person['buyIn'],
                'customerId' : person['customerId'],
                'defense' : person['defense'],
                'fantasyTeamId' : person['fantasyTeamId'],
                'foul' : person['foul'],
                'payout' : person['payout'],
                'penalty' : person['penalty'],
                'points' : person['points'],
                'rank' : person['rank'],
                'tournamentId' : person['tournamentId'],
            }

            
            scraperwiki.sqlite.save(unique_keys=['fantasyTeamId','tournamentId'], data=manager_data, table_name='standings')

def import_ranks():
    k = 20
    limit = 2*k
    for offset in range(0,20000,k):
        
        met = urllib2.urlopen(get_metro_manager_rankings_url(offset,limit))
        metro_managers = json.load(met)
        standings = metro_managers['standings']
        count = 1
        prev_rank  = 0
        prev_points = 0
        first = True
        for person in standings:
            if first:
                prev_points = int(person['points'])

            curr_rank = int(person['rank'])
            if curr_rank == prev_rank:
                count +=1
            else:
                
                manager_data = {
                    'number' : count,
                    'points' : prev_points,
                    'rank' : prev_rank,
                    'tournamentId' : person['tournamentId'],
                }
                count = 1
                prev_rank = curr_rank
                prev_points = int(person['points'])
            
            scraperwiki.sqlite.save(unique_keys=['rank','points'], data=manager_data, table_name='ranking')

def main():
    import_gameweeks()
    import_players()
    #import_manager_standings()
    #import_ranks()

main()

