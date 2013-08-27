from datetime import date, datetime
from decimal import Decimal
import itertools
import json
import re

import requests
import scraperwiki

SEASON = (2012, 2013)

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

class Clubs(object):

    names = (
        (1, 'ARS', 'Arsenal'),
        (2, 'AVL', 'Aston Villa'),
        (3, 'CHE', 'Chelsea'),
        (4, 'EVE', 'Everton'),
        (5, 'FUL', 'Fulham'),
        (6, 'LIV', 'Liverpool'),
        (7, 'MCI', 'Man City'),
        (8, 'MUN', 'Man Utd', 'Man United'),
        (9, 'NEW', 'Newcastle'),
        (10, 'NOR', 'Norwich'),
        (11, 'QPR', 'QPR'),
        (12, 'RDG', 'Reading'),
        (13, 'SOU', 'Southampton'),
        (14, 'STK', 'Stoke City', 'Stoke'),
        (15, 'SUN', 'Sunderland'),
        (16, 'SWA', 'Swansea'),
        (17, 'TOT', 'Tottenham'),
        (18, 'WBA', 'West Brom'),
        (19, 'WHU', 'West Ham'),
        (20, 'WIG', 'Wigan'),
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

def fpl_to_date(value):
    dt = datetime.strptime(value, '%d %b %H:%M')
    year = SEASON[0] if dt.month > 6 else SEASON[1]
    return date(year, dt.month, dt.day)

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

def import_season_history(element):
    records = []
    for season in element['season_history']:
        history = dict(
            player_id=element['id'],
            season=season[0],
            minutes_played=season[1],
            goals_scored=season[2],
            assists=season[3],
            clean_sheets=season[4],
            goals_conceded=season[5],
            own_goals=season[6],
            penalties_saved=season[7],
            penalties_missed=season[8],
            yellow_cards=season[9],
            red_cards=season[10],
            saves=season[11],
            bonus=season[12],
            ea_sports_ppi=season[13],
            value=fpl_to_decimal(season[14]),
            points=season[15])
        records.append(history)
    scraperwiki.sqlite.save(['player_id', 'season'], records,
        table_name='season_history')

def import_fixture_history(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixture_history']['all']:
        match = match_re.match(event[2])
        if not match:
            continue
        match = match.groups()
        # other_dt = CLUBS.find_dectech(match[0])
        print event
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=event[1],
            opponent=CLUBS.find_code(match[0]),
            venue=match[1],
            team_goals_scored=match[2],
            team_goals_conceded=match[3],
            minutes_played=event[3],
            goals_scored=event[4],
            assists=event[5],
            clean_sheets=event[6],
            goals_conceded=event[7],
            own_goals=event[8],
            penalties_saved=event[9],
            penalties_missed=event[10],
            yellow_cards=event[11],
            red_cards=event[12],
            saves=event[13],
            bonus=event[14],
            ea_sports_ppi=event[15],
            net_transfers=event[16],
            value=fpl_to_decimal(event[17]),
            points=event[18])
            #dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)

    scraperwiki.sqlite.save(['player_id', 'played_on'], records,table_name='fixture_history')

def import_fixtures(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixtures']['all']:
        if event[2][:-4].strip() == '':
            continue
        other_dt = CLUBS.find_dectech(event[2][:-4])
        
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=int(re.findall('\d{1,2}', event[1])[0]),
            opponent=CLUBS.find_code(event[2][:-4]),
            venue=event[2][-2:-1],
            dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)
    scraperwiki.sqlite.save(['player_id', 'played_on'], records,
        table_name='fixtures')

def main():
    for element in elements(1,601):
        import_player(element)
        import_season_history(element)
        import_fixture_history(element)
        import_fixtures(element)

main()
from datetime import date, datetime
from decimal import Decimal
import itertools
import json
import re

import requests
import scraperwiki

SEASON = (2012, 2013)

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

class Clubs(object):

    names = (
        (1, 'ARS', 'Arsenal'),
        (2, 'AVL', 'Aston Villa'),
        (3, 'CHE', 'Chelsea'),
        (4, 'EVE', 'Everton'),
        (5, 'FUL', 'Fulham'),
        (6, 'LIV', 'Liverpool'),
        (7, 'MCI', 'Man City'),
        (8, 'MUN', 'Man Utd', 'Man United'),
        (9, 'NEW', 'Newcastle'),
        (10, 'NOR', 'Norwich'),
        (11, 'QPR', 'QPR'),
        (12, 'RDG', 'Reading'),
        (13, 'SOU', 'Southampton'),
        (14, 'STK', 'Stoke City', 'Stoke'),
        (15, 'SUN', 'Sunderland'),
        (16, 'SWA', 'Swansea'),
        (17, 'TOT', 'Tottenham'),
        (18, 'WBA', 'West Brom'),
        (19, 'WHU', 'West Ham'),
        (20, 'WIG', 'Wigan'),
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

def fpl_to_date(value):
    dt = datetime.strptime(value, '%d %b %H:%M')
    year = SEASON[0] if dt.month > 6 else SEASON[1]
    return date(year, dt.month, dt.day)

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

def import_season_history(element):
    records = []
    for season in element['season_history']:
        history = dict(
            player_id=element['id'],
            season=season[0],
            minutes_played=season[1],
            goals_scored=season[2],
            assists=season[3],
            clean_sheets=season[4],
            goals_conceded=season[5],
            own_goals=season[6],
            penalties_saved=season[7],
            penalties_missed=season[8],
            yellow_cards=season[9],
            red_cards=season[10],
            saves=season[11],
            bonus=season[12],
            ea_sports_ppi=season[13],
            value=fpl_to_decimal(season[14]),
            points=season[15])
        records.append(history)
    scraperwiki.sqlite.save(['player_id', 'season'], records,
        table_name='season_history')

def import_fixture_history(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixture_history']['all']:
        match = match_re.match(event[2])
        if not match:
            continue
        match = match.groups()
        # other_dt = CLUBS.find_dectech(match[0])
        print event
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=event[1],
            opponent=CLUBS.find_code(match[0]),
            venue=match[1],
            team_goals_scored=match[2],
            team_goals_conceded=match[3],
            minutes_played=event[3],
            goals_scored=event[4],
            assists=event[5],
            clean_sheets=event[6],
            goals_conceded=event[7],
            own_goals=event[8],
            penalties_saved=event[9],
            penalties_missed=event[10],
            yellow_cards=event[11],
            red_cards=event[12],
            saves=event[13],
            bonus=event[14],
            ea_sports_ppi=event[15],
            net_transfers=event[16],
            value=fpl_to_decimal(event[17]),
            points=event[18])
            #dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)

    scraperwiki.sqlite.save(['player_id', 'played_on'], records,table_name='fixture_history')

def import_fixtures(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixtures']['all']:
        if event[2][:-4].strip() == '':
            continue
        other_dt = CLUBS.find_dectech(event[2][:-4])
        
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=int(re.findall('\d{1,2}', event[1])[0]),
            opponent=CLUBS.find_code(event[2][:-4]),
            venue=event[2][-2:-1],
            dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)
    scraperwiki.sqlite.save(['player_id', 'played_on'], records,
        table_name='fixtures')

def main():
    for element in elements(1,601):
        import_player(element)
        import_season_history(element)
        import_fixture_history(element)
        import_fixtures(element)

main()
from datetime import date, datetime
from decimal import Decimal
import itertools
import json
import re

import requests
import scraperwiki

SEASON = (2012, 2013)

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

class Clubs(object):

    names = (
        (1, 'ARS', 'Arsenal'),
        (2, 'AVL', 'Aston Villa'),
        (3, 'CHE', 'Chelsea'),
        (4, 'EVE', 'Everton'),
        (5, 'FUL', 'Fulham'),
        (6, 'LIV', 'Liverpool'),
        (7, 'MCI', 'Man City'),
        (8, 'MUN', 'Man Utd', 'Man United'),
        (9, 'NEW', 'Newcastle'),
        (10, 'NOR', 'Norwich'),
        (11, 'QPR', 'QPR'),
        (12, 'RDG', 'Reading'),
        (13, 'SOU', 'Southampton'),
        (14, 'STK', 'Stoke City', 'Stoke'),
        (15, 'SUN', 'Sunderland'),
        (16, 'SWA', 'Swansea'),
        (17, 'TOT', 'Tottenham'),
        (18, 'WBA', 'West Brom'),
        (19, 'WHU', 'West Ham'),
        (20, 'WIG', 'Wigan'),
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

def fpl_to_date(value):
    dt = datetime.strptime(value, '%d %b %H:%M')
    year = SEASON[0] if dt.month > 6 else SEASON[1]
    return date(year, dt.month, dt.day)

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

def import_season_history(element):
    records = []
    for season in element['season_history']:
        history = dict(
            player_id=element['id'],
            season=season[0],
            minutes_played=season[1],
            goals_scored=season[2],
            assists=season[3],
            clean_sheets=season[4],
            goals_conceded=season[5],
            own_goals=season[6],
            penalties_saved=season[7],
            penalties_missed=season[8],
            yellow_cards=season[9],
            red_cards=season[10],
            saves=season[11],
            bonus=season[12],
            ea_sports_ppi=season[13],
            value=fpl_to_decimal(season[14]),
            points=season[15])
        records.append(history)
    scraperwiki.sqlite.save(['player_id', 'season'], records,
        table_name='season_history')

def import_fixture_history(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixture_history']['all']:
        match = match_re.match(event[2])
        if not match:
            continue
        match = match.groups()
        # other_dt = CLUBS.find_dectech(match[0])
        print event
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=event[1],
            opponent=CLUBS.find_code(match[0]),
            venue=match[1],
            team_goals_scored=match[2],
            team_goals_conceded=match[3],
            minutes_played=event[3],
            goals_scored=event[4],
            assists=event[5],
            clean_sheets=event[6],
            goals_conceded=event[7],
            own_goals=event[8],
            penalties_saved=event[9],
            penalties_missed=event[10],
            yellow_cards=event[11],
            red_cards=event[12],
            saves=event[13],
            bonus=event[14],
            ea_sports_ppi=event[15],
            net_transfers=event[16],
            value=fpl_to_decimal(event[17]),
            points=event[18])
            #dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)

    scraperwiki.sqlite.save(['player_id', 'played_on'], records,table_name='fixture_history')

def import_fixtures(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixtures']['all']:
        if event[2][:-4].strip() == '':
            continue
        other_dt = CLUBS.find_dectech(event[2][:-4])
        
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=int(re.findall('\d{1,2}', event[1])[0]),
            opponent=CLUBS.find_code(event[2][:-4]),
            venue=event[2][-2:-1],
            dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)
    scraperwiki.sqlite.save(['player_id', 'played_on'], records,
        table_name='fixtures')

def main():
    for element in elements(1,601):
        import_player(element)
        import_season_history(element)
        import_fixture_history(element)
        import_fixtures(element)

main()
