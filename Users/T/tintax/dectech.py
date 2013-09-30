import json

import requests
import scraperwiki

url = 'http://www.dectech.org/cgi-bin/new_site/GetTeamRankingsIntl.pl?divID=0'
referer = 'http://www.dectech.org/football_sites/football_dectech/rankings.php'

fpl_teams = { 'Stoke': 'Stoke City', 'Man United': 'Man Utd' }

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

records = []
data = json.loads(requests.get(url, headers=dict(referer=referer)).content)
for ranking in data['rankings']:
    records.append(dict(
        team=fpl_teams.get(ranking['name'], ranking['name']),
        defence=percentage(data['bounds']['minDef'], ranking['def']),
        attack=percentage(ranking['atk'], data['bounds']['maxAtk']),
        overall=percentage(ranking['overall'], data['bounds']['maxOvr'])))
scraperwiki.sqlite.save(['team'], records, table_name='teams')
    

import json

import requests
import scraperwiki

url = 'http://www.dectech.org/cgi-bin/new_site/GetTeamRankingsIntl.pl?divID=0'
referer = 'http://www.dectech.org/football_sites/football_dectech/rankings.php'

fpl_teams = { 'Stoke': 'Stoke City', 'Man United': 'Man Utd' }

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

records = []
data = json.loads(requests.get(url, headers=dict(referer=referer)).content)
for ranking in data['rankings']:
    records.append(dict(
        team=fpl_teams.get(ranking['name'], ranking['name']),
        defence=percentage(data['bounds']['minDef'], ranking['def']),
        attack=percentage(ranking['atk'], data['bounds']['maxAtk']),
        overall=percentage(ranking['overall'], data['bounds']['maxOvr'])))
scraperwiki.sqlite.save(['team'], records, table_name='teams')
    

