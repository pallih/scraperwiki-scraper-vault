from collections import namedtuple
from cookielib import CookieJar
from datetime import date, datetime, timedelta
from lxml.html import document_fromstring
import re
from textwrap import dedent
from urllib2 import build_opener, HTTPCookieProcessor, Request

import scraperwiki

def iso_to_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()

scraperwiki.sqlite.execute('''
    create table if not exists weeks (season_code string,
        ordinal int, starts_on string, scraped_on string);
''')
scraperwiki.sqlite.execute('''
    create table if not exists matches (id int,
        league string, season int, week int, division int,
        played_on string);
''')
scraperwiki.sqlite.execute('''
    create table if not exists teams (match_id int,
        name string, venue string, chalks int, points int);
''')
scraperwiki.sqlite.execute('''
    create table if not exists players (match_id int,
        game int, venue string, chalks int, player_id int,
        name string);
''')

class Site(object):

    base_url = 'http://www.online-bowls.com/index'
    opener = build_opener(HTTPCookieProcessor(CookieJar()))
    
    def _get(self, url, referer=None):
        url = '%s/%s' % (self.base_url, url)
        headers = {'Referer': referer} if referer else {}
        request = Request(url, headers=headers)
        response = self.opener.open(request)
        html = response.read()
        response.close()
        return html

    def _fixtures_url(self, season_code, week=None):
        url = 'league.php?LEAGUE=%s&pg=4' % season_code
        if week:
            url = '%s&week=%d' % (url, week)
        return url
    
    def fixtures(self, season_code, week=None):
        return self._get(self._fixtures_url(season_code, week))

    def match(self, season_code, week, id):
        fixtures_url = self._fixtures_url(season_code, week)
        match_url = 'match_result.php?match=%d' % int(id)
        return self._get(match_url, referer=fixtures_url)
        

class Week(object):

    rows = scraperwiki.sqlite.select('* from weeks')
    regexp = re.compile(r'match_result\.php\?match=(\d+)')

    def __init__(self, season, ordinal, starts_on):
        self.season = season
        self.ordinal = ordinal
        self.starts_on = starts_on
        self.scraped_on = date.min
        for row in self.rows:   
            if row['season_code'] == season.code and row['ordinal'] == ordinal:
                self.scraped_on = iso_to_date(row['scraped_on'])
        self.matches = []
        self.teams = []
        self.players = []
        
    @property
    def is_due(self):
        today = date.today()
        if self.scraped_on < today - timedelta(days=28):
            # hasn't been scraped for at least 28 days (or ever!)
            return True
        if self.starts_on >= today - timedelta(days=14):
            # rescrape the last couple of weeks (and all future weeks)
            return True
        return False

    def _scrape_player(self, match_id, game, venue, cells):
        player = {
            'match_id': match_id,
            'game': game,
            'venue': venue,
            'chalks': int(cells[1].text)
        }
        if len(cells[0]) and cells[0][0].tag == 'a':
            match = re.search('\d+', cells[0][0].get('href'))
            player['player_id'] = int(match.group())
            player['name'] = cells[0][0].text.strip()
        else:
            player['player_id'] = None
            player['name'] = 'Walkover'
        return player

    def _scrape_match(self, id, html):
        dtstamp = re.search(r'\d{2}/\d{2}/\d{4}', html).group()
        match = {
            'id': id,
            'league': self.season.league,
            'season': self.season.year,
            'week': self.ordinal,
            'division': int(re.search(r'Division (\d)', html).group(1)),
            'played_on': datetime.strptime(dtstamp, '%d/%m/%Y').date()
        }
        self.matches.append(match)
        table = document_fromstring(html).xpath('//center//table')[0]
        players = []
        for i, row in enumerate(table.iterfind(".//tr[@height='20']"), 1):
            players.append(self._scrape_player(match['id'], i, 'H', row[0:2]))
            players.append(self._scrape_player(match['id'], i, 'A', row[2:4]))
        self.players.extend(players)
        # work out the teams involved as series of (home, away) tuples
        names = table[1].xpath(".//b/text()")
        points = (int(table[-1][1][0].text), int(table[-1][3][0].text))
        chalks = (
            sum(p['chalks'] for p in players if p['venue'] == 'H'),
            sum(p['chalks'] for p in players if p['venue'] == 'A')
            )
        self.teams.append({
            'match_id': match['id'],
            'name': names[0],
            'venue': 'H',
            'chalks': chalks[0],
            'points': points[0]})
        self.teams.append({
            'match_id': match['id'],
            'name': names[1],
            'venue': 'A',
            'chalks': chalks[1],
            'points': points[1]})

    def scrape(self, match_ids=None):
        site = Site()
        html = site.fixtures(self.season.code, self.ordinal)
        for id in set(m.group(1) for m in self.regexp.finditer(html)):
            if match_ids and int(id) not in match_ids:
                continue
            html = site.match(self.season.code, self.ordinal, id)
            self._scrape_match(id, html)

    def save(self):
        if not self.matches or not self.teams or not self.players:
            return
        scraperwiki.sqlite.save(['id'], self.matches, table_name='matches')
        scraperwiki.sqlite.save(['match_id', 'venue'], self.teams,
            table_name='teams')
        scraperwiki.sqlite.save(['match_id', 'game', 'venue'], self.players,
            table_name='players')
        scraperwiki.sqlite.save(['season_code', 'ordinal'], {
            'season_code': self.season.code,
            'ordinal': self.ordinal,
            'starts_on': self.starts_on,
            'scraped_on': date.today()}, table_name='weeks')
            

class Season(namedtuple('Season', 'code league year')):

    __slots__ = ()
    
    regexp = re.compile(r'(\d{2}/\d{2}/\d{2})[ -]+Week (\d{1,2})')

    def weeks(self):
        html = Site().fixtures(self.code)
        for g in (x.groups() for x in self.regexp.finditer(html)):
            nominal_date = datetime.strptime(g[0], '%d/%m/%y').date()
            monday = nominal_date - timedelta(days=nominal_date.weekday())
            yield Week(self, int(g[1]), monday)

    def scrape(self, week_numbers=None, match_ids=None, force=False):
        for week in self.weeks():
            if week_numbers and week.ordinal not in week_numbers:
                continue
            if not force and not week.is_due:
                continue
            week.scrape(match_ids)
            week.save()

SEASONS = (
    Season('FABA2011', 'FABA', 2011),
    #Season('FABA2010', 'FABA', 2010),
    #Season('FABA2009', 'FABA', 2009),
)

TESTS = (
#    (Season('FABA2011', 'FABA', 2011), (7,), (15015,), True),
)

def main(seasons, tests):
    if len(tests):
        for test in tests:
            season = test[0]
            season.scrape(test[1], test[2], test[3])
    else:
        for season in seasons:
            season.scrape()

main(SEASONS, TESTS)
