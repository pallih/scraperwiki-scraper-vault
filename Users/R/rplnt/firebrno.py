import re
import time
import scraperwiki
from BeautifulSoup import BeautifulSoup as bs


href_match = re.compile(r'filter\[id\]=(\d+)\&district_id=(\d+)')
type_match = re.compile(r'type-(\d)')
input_format = '%d. %m %Y, %H:%M'
date_format = '%Y-%m-%d %H:%M'

cz_months = {
    u'leden':1,
    u'\xfanor':2,
    u'b\u0159ezen':3,
    u'duben':4,
    u'kv\u011bten':5,
    u'\u010derven':6,
    u'\u010dervenec':7,
    u'srpen':8,
    u'z\xe1\u0159\xed':9,
    u'\u0159\xedjen':10,
    u'listopad':11,
    u'prosinec':12
}

incident_types = {
    1: "Požár",
    2: "Dopravní nehoda",
    3: "Živelní pohroma",
    4: "Chemické látky",
    5: "Technická pomoc",
    6: "Záchrana osob/zvířat",
    7: "Ostatní"
}

district_ids = {
    3701: "Blansko",
    3702: "Brno-město",
    3703: "Brno-venkov",
    3704: "Břeclav",
    3706: "Hodonín",
    3712: "Vyškov",
    3713: "Znojmo",
}

def scrape(page):
    html = scraperwiki.scrape('http://www.firebrno.cz/modules/incidents/index.php?page=%s' % str(page))
    soup = bs(html)

    for div in soup.fetch('div', 'inc-item'):
        date = div.fetch('div', 'inc-date')[0].string
        date = '%s %d %s' % (date.split()[0], cz_months[date.split()[1]], ' '.join(date.split()[2:]))
        date = time.strptime(date, input_format)
        href = div.fetch('div', 'inc-detail-link')[0].a['href']
        inc_id, loc = map(int, re.search(href_match, href).groups())
        type_class = div.fetch('div', 'inc-type')[0]['class']
        inc_type = re.search(type_match, type_class).group(1)
        inc_content = div.fetch('div', 'inc-content')[0].string[:-8]
        inc_summary = div.h3.a.string
    
        data = {'id': inc_id, 'date': time.strftime(date_format, date), 'type': int(inc_type), 
                'location': loc, 'summary': inc_summary, 'details': inc_content}

        scraperwiki.sqlite.save(unique_keys=["id"], data=data)

        time.sleep(1/2)

# enough for 24 hours, no need to check further
scrape(1)
scrape(2)
import re
import time
import scraperwiki
from BeautifulSoup import BeautifulSoup as bs


href_match = re.compile(r'filter\[id\]=(\d+)\&district_id=(\d+)')
type_match = re.compile(r'type-(\d)')
input_format = '%d. %m %Y, %H:%M'
date_format = '%Y-%m-%d %H:%M'

cz_months = {
    u'leden':1,
    u'\xfanor':2,
    u'b\u0159ezen':3,
    u'duben':4,
    u'kv\u011bten':5,
    u'\u010derven':6,
    u'\u010dervenec':7,
    u'srpen':8,
    u'z\xe1\u0159\xed':9,
    u'\u0159\xedjen':10,
    u'listopad':11,
    u'prosinec':12
}

incident_types = {
    1: "Požár",
    2: "Dopravní nehoda",
    3: "Živelní pohroma",
    4: "Chemické látky",
    5: "Technická pomoc",
    6: "Záchrana osob/zvířat",
    7: "Ostatní"
}

district_ids = {
    3701: "Blansko",
    3702: "Brno-město",
    3703: "Brno-venkov",
    3704: "Břeclav",
    3706: "Hodonín",
    3712: "Vyškov",
    3713: "Znojmo",
}

def scrape(page):
    html = scraperwiki.scrape('http://www.firebrno.cz/modules/incidents/index.php?page=%s' % str(page))
    soup = bs(html)

    for div in soup.fetch('div', 'inc-item'):
        date = div.fetch('div', 'inc-date')[0].string
        date = '%s %d %s' % (date.split()[0], cz_months[date.split()[1]], ' '.join(date.split()[2:]))
        date = time.strptime(date, input_format)
        href = div.fetch('div', 'inc-detail-link')[0].a['href']
        inc_id, loc = map(int, re.search(href_match, href).groups())
        type_class = div.fetch('div', 'inc-type')[0]['class']
        inc_type = re.search(type_match, type_class).group(1)
        inc_content = div.fetch('div', 'inc-content')[0].string[:-8]
        inc_summary = div.h3.a.string
    
        data = {'id': inc_id, 'date': time.strftime(date_format, date), 'type': int(inc_type), 
                'location': loc, 'summary': inc_summary, 'details': inc_content}

        scraperwiki.sqlite.save(unique_keys=["id"], data=data)

        time.sleep(1/2)

# enough for 24 hours, no need to check further
scrape(1)
scrape(2)
