# Scraper for BBC Proms 2011

import re, sys, time
import scraperwiki
import lxml.etree
import lxml.html           
import urlparse
import urllib

def scrape(url):
    f = urllib.urlopen(url)
    r = f.read()
    f.close()
    return r

def parse_time(s):
    m = re.match(' *(\d+\.\d\d[ap]m) *&#8211; *c. (\d+\.\d\d[ap]m)', s)
    from_time, to_time = m.groups()
    return from_time, to_time

def parse_performance(p):
    strong = p.cssselect('strong')[0]
    if p.text_content() == 'INTERVAL':
        return { 'title': 'Interval' }
    return {
        'composer': p.cssselect('h3')[0].text.strip(),
        'title': strong.text.strip(),
        'rest': strong.tail.strip(),
    }

def parse_contributor(c):
    strong = c.cssselect('strong')[0]
    return {
        'name': strong.text.strip(),
        'instrument': strong.tail.strip(),
    }

def first(s):
    return s[0].text_content().strip() if s else ''

def scrape_event(html):
    root = lxml.html.fromstring(html)
    out = {}
    out['title'] = root.cssselect('h1')[0].text.strip()
    out['desc_short'] = root.cssselect('#desc_short')[0].text_content()
    out['desc_long'] = first(root.cssselect('#desc_long'))
    out['performances'] = [ parse_performance(x) for x in root.cssselect('#performances li') ]
    out['contributors'] = [ parse_contributor(x) for x in root.cssselect('#contributors li') ]
    out['categories'] = re.findall('/proms/whats-on/2011/categories/(.*?)"', html)
    meta_elt = root.cssselect('#event_performances h2')[0]
    meta = lxml.etree.tostring(meta_elt)
    meta = re.sub('</?h2>', '', meta)
    meta = meta.split('<br />')
    out['time_start'], out['time_end'] = parse_time(meta[1])
    out['feature'] = meta_elt.cssselect('a')[0].text.strip()
    return out

def scrape_week(root):
    div = root.cssselect('div.whatson_listing')[0]
    days = div[0::2]
    events = div[1::2]
    for i in range(0, len(days)):
        day = days[i].text
        events_day = events[i].cssselect('span a')
        for event in events_day:
            href = event.attrib.get('href')
            m = re.search('/(\d+)$', href)
            id = m.group(1)
            print "Fetching %s" % href
            html = scrape(urlparse.urljoin(url, href))
            data = scrape_event(html)
            data['day'] = time.strptime( day + ' 2011', '%A %d %B %Y' )
            data['id'] = id
            data['url'] = urlparse.urljoin(url, href)
            scraperwiki.sqlite.save(unique_keys=['id'], data=data)

def fetch_week(url):
    print "Fetching %s" % url
    html = scrape(url)
    root = lxml.html.fromstring(html)
    scrape_week(root)
    next_link = root.cssselect("p.next a")
    if next_link:
        next_url = urlparse.urljoin(url, next_link[0].attrib.get('href'))
        fetch_week(next_url)

url = "http://www.bbc.co.uk/proms/whats-on/2011/july-15"
fetch_week(url)

