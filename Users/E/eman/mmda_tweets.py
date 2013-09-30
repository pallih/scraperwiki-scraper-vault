# MMDA Twitter Scraper

import re
import datetime
import scraperwiki
from BeautifulSoup import BeautifulSoup
from scrapemark import scrape    

pattern = dict(
        all = re.compile(''),
        ago = re.compile('[about ]*([0-9]*|half an?) ((hour|minute)s?) ago', re.IGNORECASE),
    )
hours_ago = 2

def download_for_road(twitter_name, road, limit=10):
    since = datetime.datetime.utcnow() - datetime.timedelta(0, 60 * 60 * hours_ago)
    tmp_url = 'http://search.twitter.com/search?ors=&ands=%(road)s&lang=all&from=%(user)s&rpp=%(limit)i&since=%(since)s&time=%(time)s'
    url = tmp_url % dict(
        user = twitter_name,
        road = road,
        limit = limit,
        since = since.strftime('%Y-%m-%d'),
        time = since.strftime('%H:%M'),
    )
    return scraperwiki.scrape(url)

def get_time(time):
    try:
        updated_at = datetime.datetime.strptime(time, '%b %d, %Y %H:%M %p %Z')
    except ValueError:
        print 'Cannot parse %s' % time
    else:
        return updated_at
    if not pattern['ago'].search(time):
        # Assume that the data is one day old if the pattern is not recognized
        return now - datetime.timedelta(1, seconds)
    now = datetime.datetime.utcnow()
    days = 0
    seconds = 0
    value, unit = pattern['ago'].sub('\\1|\\2', time.lower()).split('|')
    if value.startswith('half a'):
        if unit.startswith('hour'):
            seconds = 30 * 60
        elif unit.startswith('minute'):
            seconds = 30
    else:
        try:
            ival = int(value)
        except ValueError:
            return None
        if unit.startswith('hour'):
            seconds = ival * 60 * 60
        elif unit.startswith('minute'):
            seconds = ival * 60
    updated_at = now - datetime.timedelta(days, seconds)
    return updated_at


# BeautifulSoup methods
def parse_entry(entry):
    time_entries = entry.findAll('div', **{'class': re.compile('info')})
    time = ''.join([t.strip() for t in time_entries[0].fetchText(pattern['ago'])])
    updated_at = get_time(time)
    text_entries = entry.findAll('span', **{'class': re.compile('msgtxt.*')})
    text = ''.join([t.strip() for t in text_entries[0].fetchText(pattern['all'])])
    t_id = int(text_entries[0].get('id').replace('msgtxt', ''))
    return t_id, updated_at, text

def parse_html(html):
    soup = BeautifulSoup(html)
    all_entries = soup.findAll('li', **{'class': re.compile('result.*')})
    for entry in all_entries:
        result = parse_entry(entry)
        if result:
            yield result

def get_road(road, twitter_name='MMDA'):
    html = download_for_road(twitter_name, road)
    data = []
    for t_id, updated_at, text in parse_html(html):
        data.append(dict(
            twitter_name = twitter_name,
            road = road,
            t_id = t_id,
            updated_at = updated_at,
            text = text,
        ))
    scraperwiki.sqlite.save(unique_keys=['t_id'], data=data)
    return data

def test_soup():
    twitter_name = 'MMDA'
    road = 'EDSA'
    return get_road(road, twitter_name)



# Scrapemark methods

def scrape_road(road, twitter_name='MMDA'):
    html = download_for_road(twitter_name, road)
    tmp = '''{*
        <li class="result">
            <span id="msgtxt{{ [data].t_id }}" class="msgtxt">{{ [data].text }}</span>
            <div class="info">{{ [data].info }}<span /></div>
        </li>
    *}'''
    data = scrape(tmp, html)['data']
    for cnt in range(len(data)):
        if data[cnt]['info'].find('GMT') > -1:
            data[cnt]['info'] = re.sub('GMT.*', 'GMT', data[cnt]['info'])
        data[cnt]['updated_at'] = get_time(data[cnt]['info'])
        data[cnt]['road'] = road
        data[cnt]['twitter_name'] = twitter_name
        #print '"%s"' % data[cnt]['info']
    scraperwiki.sqlite.save(unique_keys=['t_id'], data=data)
    return data

def test_scrapemark():
    twitter_name = 'MMDA'
    for road in ('edsa', 'c5', 'slex', ):
    #for road in ('edsa', ):
        data = scrape_road(road, twitter_name,)
    return datetime.datetime.utcnow()


# Comment one of these to test:
#print test_soup()
print test_scrapemark()

'Please run this using a view.'
# MMDA Twitter Scraper

import re
import datetime
import scraperwiki
from BeautifulSoup import BeautifulSoup
from scrapemark import scrape    

pattern = dict(
        all = re.compile(''),
        ago = re.compile('[about ]*([0-9]*|half an?) ((hour|minute)s?) ago', re.IGNORECASE),
    )
hours_ago = 2

def download_for_road(twitter_name, road, limit=10):
    since = datetime.datetime.utcnow() - datetime.timedelta(0, 60 * 60 * hours_ago)
    tmp_url = 'http://search.twitter.com/search?ors=&ands=%(road)s&lang=all&from=%(user)s&rpp=%(limit)i&since=%(since)s&time=%(time)s'
    url = tmp_url % dict(
        user = twitter_name,
        road = road,
        limit = limit,
        since = since.strftime('%Y-%m-%d'),
        time = since.strftime('%H:%M'),
    )
    return scraperwiki.scrape(url)

def get_time(time):
    try:
        updated_at = datetime.datetime.strptime(time, '%b %d, %Y %H:%M %p %Z')
    except ValueError:
        print 'Cannot parse %s' % time
    else:
        return updated_at
    if not pattern['ago'].search(time):
        # Assume that the data is one day old if the pattern is not recognized
        return now - datetime.timedelta(1, seconds)
    now = datetime.datetime.utcnow()
    days = 0
    seconds = 0
    value, unit = pattern['ago'].sub('\\1|\\2', time.lower()).split('|')
    if value.startswith('half a'):
        if unit.startswith('hour'):
            seconds = 30 * 60
        elif unit.startswith('minute'):
            seconds = 30
    else:
        try:
            ival = int(value)
        except ValueError:
            return None
        if unit.startswith('hour'):
            seconds = ival * 60 * 60
        elif unit.startswith('minute'):
            seconds = ival * 60
    updated_at = now - datetime.timedelta(days, seconds)
    return updated_at


# BeautifulSoup methods
def parse_entry(entry):
    time_entries = entry.findAll('div', **{'class': re.compile('info')})
    time = ''.join([t.strip() for t in time_entries[0].fetchText(pattern['ago'])])
    updated_at = get_time(time)
    text_entries = entry.findAll('span', **{'class': re.compile('msgtxt.*')})
    text = ''.join([t.strip() for t in text_entries[0].fetchText(pattern['all'])])
    t_id = int(text_entries[0].get('id').replace('msgtxt', ''))
    return t_id, updated_at, text

def parse_html(html):
    soup = BeautifulSoup(html)
    all_entries = soup.findAll('li', **{'class': re.compile('result.*')})
    for entry in all_entries:
        result = parse_entry(entry)
        if result:
            yield result

def get_road(road, twitter_name='MMDA'):
    html = download_for_road(twitter_name, road)
    data = []
    for t_id, updated_at, text in parse_html(html):
        data.append(dict(
            twitter_name = twitter_name,
            road = road,
            t_id = t_id,
            updated_at = updated_at,
            text = text,
        ))
    scraperwiki.sqlite.save(unique_keys=['t_id'], data=data)
    return data

def test_soup():
    twitter_name = 'MMDA'
    road = 'EDSA'
    return get_road(road, twitter_name)



# Scrapemark methods

def scrape_road(road, twitter_name='MMDA'):
    html = download_for_road(twitter_name, road)
    tmp = '''{*
        <li class="result">
            <span id="msgtxt{{ [data].t_id }}" class="msgtxt">{{ [data].text }}</span>
            <div class="info">{{ [data].info }}<span /></div>
        </li>
    *}'''
    data = scrape(tmp, html)['data']
    for cnt in range(len(data)):
        if data[cnt]['info'].find('GMT') > -1:
            data[cnt]['info'] = re.sub('GMT.*', 'GMT', data[cnt]['info'])
        data[cnt]['updated_at'] = get_time(data[cnt]['info'])
        data[cnt]['road'] = road
        data[cnt]['twitter_name'] = twitter_name
        #print '"%s"' % data[cnt]['info']
    scraperwiki.sqlite.save(unique_keys=['t_id'], data=data)
    return data

def test_scrapemark():
    twitter_name = 'MMDA'
    for road in ('edsa', 'c5', 'slex', ):
    #for road in ('edsa', ):
        data = scrape_road(road, twitter_name,)
    return datetime.datetime.utcnow()


# Comment one of these to test:
#print test_soup()
print test_scrapemark()

'Please run this using a view.'
