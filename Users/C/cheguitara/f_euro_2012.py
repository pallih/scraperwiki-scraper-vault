from datetime import date, datetime
from decimal import Decimal
import itertools
import json
import re

import requests
import scraperwiki

SEASON = (2011, 2012)

def percentage(part, whole):
    return int(float(part) / float(whole) * 100)

class Clubs(object):

    names = (
        (1, 'CRO', 'Croatia'),
        (2, 'CZE', 'Czech Republic'),
        (3, 'DEN', 'Denmark'),
        (4, 'ENG', 'England'),
        (5, 'FRA', 'France'),
        (6, 'GER', 'Germany'),
        (7, 'GRE', 'Greece'),
        (8, 'ITA', 'Italy'),
        (9, 'NED', 'Netherlands'),
        (10, 'POL', 'Poland'),
        (11, 'POR', 'Portugal'),
        (12, 'IRL', 'Republic of Ireland'),
        (13, 'RUS', 'Russia'),
        (14, 'ESP', 'Spain'),
        (15, 'SWE', 'Sweden'),
        (16, 'UKR', 'Ukraine'),
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
    dt = datetime.strptime(value, '%d %b')
    year = SEASON[0] if dt.month > 6 else SEASON[1]
    return date(year, dt.month, dt.day)

def dectech_score(position, own, other):
    if position in (1, 2):
        return own['defence'] - other['attack']
    else:
        return own['attack'] - other['defence']

def elements(start=None, end=None):
    url = 'http://en.euro2012fantasy.uefa.com/web/api/elements/%d/'
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
            penalties_saved=season[6],
            penalties_missed=season[7],
            yellow_cards=season[8],
            red_cards=season[9],
            saves=season[10],
            penalties_earned=season[11],
            penalties_conceded=season[12],
            recovered_balls=season[13],
            net_transfers=season[14],
            value=fpl_to_decimal(season[15]),
            points=season[16])
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
        other_dt = CLUBS.find_dectech(match[0])
        fixture = dict(
            player_id=element['id'],
            played_on=fpl_to_date(event[0]),
            round=event[1],
            opponent=CLUBS.find_code(match[0]),
            team_goals_scored=match[2],
            team_goals_conceded=match[3],
            minutes_played=event[3],
            goals_scored=event[4],
            assists=event[5],
            clean_sheets=event[6],
            goals_conceded=event[7],
            penalties_saved=season[8],
            penalties_missed=season[9],
            yellow_cards=season[10],
            red_cards=season[11],
            saves=season[12],
            penalties_earned=season[13],
            penalties_conceded=season[14],
            recovered_balls=season[15],
            net_transfers=season[16],
            value=fpl_to_decimal(season[17]),
            points=season[18])
            dt_diff=dectech_score(element['element_type_id'], own_dt, other_dt))
        records.append(fixture)
    scraperwiki.sqlite.save(['player_id', 'played_on'], records,
        table_name='fixture_history')

def import_fixtures(element):
    own_dt = CLUBS.find_dectech(element['team_id'])
    records = []
    for event in element['fixtures']['all']:
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
    for element in elements(1, 20):
        import_player(element)
        import_season_history(element)
        import_fixture_history(element)
#       import_fixtures(element)

main()
