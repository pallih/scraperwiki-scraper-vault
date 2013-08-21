from datetime import date, datetime
from decimal import Decimal
import itertools
import json
import re

import requests
import scraperwiki

SEASON = (2013, 2014)

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

class Clubs(object):

    names = (
        (1, 'ARS', 'Arsenal'),
        (2, 'AVL', 'Aston Villa'),
        (3, 'CAR', 'Cardiff'),
        (4, 'CHE', 'Chelsea'),
        (5, 'CRY', 'Crystal Palace'),
        (6, 'EVE', 'Everton'),
        (7, 'FUL', 'Fulham'),
        (8, 'HUL', 'Hull'),
        (9, 'LIV', 'Liverpool'),
        (10, 'MCI', 'Man City'),
        (11, 'MUN', 'Man Utd', 'Man United'),
        (12, 'NEW', 'Newcastle'),
        (13, 'NOR', 'Norwich'),
        (14, 'SOU', 'Southampton'),
        (15, 'STK', 'Stoke City', 'Stoke'),
        (16, 'SUN', 'Sunderland'),
        (17, 'SWA', 'Swansea'),
        (18, 'TOT', 'Tottenham'),
        (19, 'WBA', 'West Brom'),
        (20, 'WHU', 'West Ham'),
        )
        
    def __init__(self):
        self._codes = {}
        
        base_url = 'http://www.dectech.org'
        url = '%s/cgi-bin/new_site/GetTeamRankingsIntl.pl?divID=0' % base_url
        referer = '%s/football_sites/football_dectech/rankings.php' % base_url
        html = requests.get(url, headers=dict(referer=referer)).content

        self._dectech = {}
        data = json.loads(html)
        for ranking in data['rankings']:
            club = dict(
                name=self.find_code(ranking['name']),
                defence=percentage(data['bounds']['minDef'], ranking['def']),
                attack=percentage(ranking['atk'], data['bounds']['maxAtk']),
                overall=percentage(ranking['overall'], data['bounds']['maxOvr']))
            self._dectech[club['name']] = club
        scraperwiki.sqlite.save(['name'], self._dectech.values(), table_name='club')
        
    def find_code(self, name):
        code = self._codes.get(name)
        if code:
            return code
        for club in self.names:
            if name in club:
                self._codes[name] = club[1]
                return club[1]

    def find_dectech(self, name):
        return self._dectech[self.find_code(name)]
        
CLUBS = Clubs()

POSITIONS = {
    1: 'Goalkeeper', 2: 'Defender',
    3: 'Midfielder', 4: 'Forward'}

match_re = re.compile(r'(\w\w\w)\((\w)\) (\d{1,2})-(\d{1,2})')

def fpl_to_decimal(value):
    return Decimal((0, [int(c) for c in str(value)], -1))


def dectech_score(position, own, other):
    if position in (1, 2):
        return own['defence'] - other['attack']
    else:
        return own['attack'] - other['defence']

def elements(start=None, end=None):
    url = 'http://fantasy.premierleague.com/web/api/elements/%d/'
    start = start or scraperwiki.sqlite.get_var('next_element', default=1)
    for i in itertools.count(start):
        if end and i > end:
            break
        response = requests.get(url % i)
        if not response.ok:
            break
        yield json.loads(response.content)
        scraperwiki.sqlite.save_var('next_element', i + 1)
    scraperwiki.sqlite.save_var('next_element', 1)

def import_player(element):
    player = dict(
        id=element['id'],
        code=element['code'],
        forename=element['first_name'],
        surname=element['second_name'],
        web_name=element['web_name'],
        club=CLUBS.find_code(element['team_id']),
        position=POSITIONS[element['element_type_id']],
        cost=fpl_to_decimal(element['now_cost']))
    scraperwiki.sqlite.save(['id'], player, table_name='player')



def main():
    for element in elements(1, 529):
        import_player(element)


main()
from datetime import date, datetime
from decimal import Decimal
import itertools
import json
import re

import requests
import scraperwiki

SEASON = (2013, 2014)

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

class Clubs(object):

    names = (
        (1, 'ARS', 'Arsenal'),
        (2, 'AVL', 'Aston Villa'),
        (3, 'CAR', 'Cardiff'),
        (4, 'CHE', 'Chelsea'),
        (5, 'CRY', 'Crystal Palace'),
        (6, 'EVE', 'Everton'),
        (7, 'FUL', 'Fulham'),
        (8, 'HUL', 'Hull'),
        (9, 'LIV', 'Liverpool'),
        (10, 'MCI', 'Man City'),
        (11, 'MUN', 'Man Utd', 'Man United'),
        (12, 'NEW', 'Newcastle'),
        (13, 'NOR', 'Norwich'),
        (14, 'SOU', 'Southampton'),
        (15, 'STK', 'Stoke City', 'Stoke'),
        (16, 'SUN', 'Sunderland'),
        (17, 'SWA', 'Swansea'),
        (18, 'TOT', 'Tottenham'),
        (19, 'WBA', 'West Brom'),
        (20, 'WHU', 'West Ham'),
        )
        
    def __init__(self):
        self._codes = {}
        
        base_url = 'http://www.dectech.org'
        url = '%s/cgi-bin/new_site/GetTeamRankingsIntl.pl?divID=0' % base_url
        referer = '%s/football_sites/football_dectech/rankings.php' % base_url
        html = requests.get(url, headers=dict(referer=referer)).content

        self._dectech = {}
        data = json.loads(html)
        for ranking in data['rankings']:
            club = dict(
                name=self.find_code(ranking['name']),
                defence=percentage(data['bounds']['minDef'], ranking['def']),
                attack=percentage(ranking['atk'], data['bounds']['maxAtk']),
                overall=percentage(ranking['overall'], data['bounds']['maxOvr']))
            self._dectech[club['name']] = club
        scraperwiki.sqlite.save(['name'], self._dectech.values(), table_name='club')
        
    def find_code(self, name):
        code = self._codes.get(name)
        if code:
            return code
        for club in self.names:
            if name in club:
                self._codes[name] = club[1]
                return club[1]

    def find_dectech(self, name):
        return self._dectech[self.find_code(name)]
        
CLUBS = Clubs()

POSITIONS = {
    1: 'Goalkeeper', 2: 'Defender',
    3: 'Midfielder', 4: 'Forward'}

match_re = re.compile(r'(\w\w\w)\((\w)\) (\d{1,2})-(\d{1,2})')

def fpl_to_decimal(value):
    return Decimal((0, [int(c) for c in str(value)], -1))


def dectech_score(position, own, other):
    if position in (1, 2):
        return own['defence'] - other['attack']
    else:
        return own['attack'] - other['defence']

def elements(start=None, end=None):
    url = 'http://fantasy.premierleague.com/web/api/elements/%d/'
    start = start or scraperwiki.sqlite.get_var('next_element', default=1)
    for i in itertools.count(start):
        if end and i > end:
            break
        response = requests.get(url % i)
        if not response.ok:
            break
        yield json.loads(response.content)
        scraperwiki.sqlite.save_var('next_element', i + 1)
    scraperwiki.sqlite.save_var('next_element', 1)

def import_player(element):
    player = dict(
        id=element['id'],
        code=element['code'],
        forename=element['first_name'],
        surname=element['second_name'],
        web_name=element['web_name'],
        club=CLUBS.find_code(element['team_id']),
        position=POSITIONS[element['element_type_id']],
        cost=fpl_to_decimal(element['now_cost']))
    scraperwiki.sqlite.save(['id'], player, table_name='player')



def main():
    for element in elements(1, 529):
        import_player(element)


main()
