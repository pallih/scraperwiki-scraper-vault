import html5lib
import scraperwiki
from lxml import html
from urlparse import parse_qs, urlparse

PARL_BASE_URL = 'http://www.parl.gc.ca'
SENATORS_BASE_URL = '/'.join([PARL_BASE_URL, 'SenatorsMembers/Senate/SenatorsBiography'])
SENATORS_URL = '/'.join([SENATORS_BASE_URL, 'isenator.asp?Language=E'])
FIELDS = ('external_id', 'url', 'name', 'party')

index_page = scraperwiki.scrape(SENATORS_URL)
root = html.fromstring(index_page)

for bio_table in root.cssselect('div[id="bio-table"] table'):
    for element, attribute, link, pos in bio_table.iterlinks():
        if not link.startswith('isenator_det'):
            continue
        profile_url = urlparse('/'.join([SENATORS_BASE_URL, link]))
        senator_id = int(parse_qs(profile_url.query).get('senator_id')[0])
        data = [senator_id, profile_url.geturl()]
        profile_page = scraperwiki.scrape(profile_url.geturl())
        profile = html.fromstring(profile_page)
        header = profile.xpath('//body/table')[0]
        title = header.xpath('./tr/td[2]/font')[0].text
        data += map(unicode.strip, title.rsplit(' - ', 1))
        scraperwiki.sqlite.save(unique_keys=['external_id'],
                                data=dict(zip(FIELDS, data)))import html5lib
import scraperwiki
from lxml import html
from urlparse import parse_qs, urlparse

PARL_BASE_URL = 'http://www.parl.gc.ca'
SENATORS_BASE_URL = '/'.join([PARL_BASE_URL, 'SenatorsMembers/Senate/SenatorsBiography'])
SENATORS_URL = '/'.join([SENATORS_BASE_URL, 'isenator.asp?Language=E'])
FIELDS = ('external_id', 'url', 'name', 'party')

index_page = scraperwiki.scrape(SENATORS_URL)
root = html.fromstring(index_page)

for bio_table in root.cssselect('div[id="bio-table"] table'):
    for element, attribute, link, pos in bio_table.iterlinks():
        if not link.startswith('isenator_det'):
            continue
        profile_url = urlparse('/'.join([SENATORS_BASE_URL, link]))
        senator_id = int(parse_qs(profile_url.query).get('senator_id')[0])
        data = [senator_id, profile_url.geturl()]
        profile_page = scraperwiki.scrape(profile_url.geturl())
        profile = html.fromstring(profile_page)
        header = profile.xpath('//body/table')[0]
        title = header.xpath('./tr/td[2]/font')[0].text
        data += map(unicode.strip, title.rsplit(' - ', 1))
        scraperwiki.sqlite.save(unique_keys=['external_id'],
                                data=dict(zip(FIELDS, data)))