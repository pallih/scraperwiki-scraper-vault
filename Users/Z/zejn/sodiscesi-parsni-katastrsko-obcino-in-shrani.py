import scraperwiki
import json
import datetime
from BeautifulSoup import BeautifulSoup
import re
import urllib
import urllib2
from pprint import pprint
from urllib import urlencode
import csv
from StringIO import StringIO

cols = ["sodisce", "datum", "tip", "sodnik", "lokacija", "opravilna_st", "zadeva", "tozeci", "tozeni", "dodatno"]


def find_ko(txt):
    m = re.search("k\.\s*o\.\s*([^\.,-;!?]+)", txt)
    if m:
        ko_ime = m.group(1).lower()
        return ko_ime

def parsepdf(pdfurl):
    a = scraperwiki.scrape(pdfurl)
    s = BeautifulSoup(scraperwiki.pdftoxml(a))
    kobcine = {}
    for t in s.findAll('text'):
        if t.text != " ":
            ko_ime = find_ko(t.text)
            if ko_ime:
                ko = kobcine.setdefault(ko_ime, 0)
                kobcine[ko_ime] = ko + 1
    return kobcine

def fetch_entries():
    "fetches records from sodisce.si"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; sl; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
        'Accept': 'text/html, */*',
        'Accept-Language': 'sl,en-gb;q=0.7,en;q=0.3',
        #'Accept-Encoding': 'gzip,deflate',
        'Accept-Charset': 'ISO-8859-2,utf-8;q=0.7,*;q=0.7',
        'X-Requested-With': 'XMLHttpRequest',
        }

    params = {
        'drc': 'desc',
        'func': 'allTrials',
        'messages-sections-selector-gizmo': 'undefined',
        'ord': 2,
        'page': 1,
        'search_field': 'undefined',
        'vPath': 'sodni_postopki/javne_obravnave/seznami_glavnih_obravnav/',
        }
    
    # init
    start_url = 'http://www.sodisce.si/sodni_postopki/javne_obravnave/seznami_glavnih_obravnav/'
    ajax_url = 'http://www.sodisce.si/util/ajaxresponse.php'
    
    req = urllib2.Request(start_url, headers=headers)
    response = urllib2.urlopen(req)
    content = response.read()
    
    cookie = response.headers['set-cookie'] + '; results_per_page=2000;'
    
    headers.update({
        'Cookie': cookie,
        'Referrer': start_url,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    })

    data = urlencode(params)

    req = urllib2.Request(ajax_url, data, headers)
    response = urllib2.urlopen(req)
    content = response.read()
    return content

def parse_records(content):
    "parses ajax response and pulls out content"
    import lxml.html
    h = lxml.html.fromstring(content)
    h.make_links_absolute('http://www.sodisce.si/')

    data = []
    cnt = 0
    for row in h.xpath('//tr')[2:]:
        r = []
        for n, td in enumerate(row.xpath('./td')):
            v = td.text and td.text.strip().encode('raw_unicode_escape') or ''
            if n == 1:
                v = datetime.datetime.strptime(v, '%d.%m.%Y ob %H:%M:%S')
            if n == 9:
                a = td.find('a')
                if a is not None:
                    v = a.attrib['href']
            r.append(v)
        if r:
            data.append(r)
    return data

def get_ko(ime_ko):
    url = 'http://spreadsheets.google.com/a/google.com/tq?key=tlfZZ4G0qJoLF43A7zVdjNA&tqx=out:csv&tq='
    try:
        ime = ime_ko.upper().encode("utf-8")
    except UnicodeDecodeError:
        ime = ime_ko.upper()
    param = 'SELECT * WHERE B="%s"' % (ime,)
    url += urllib.quote(param)
    data = scraperwiki.scrape(url)
    rdr = csv.DictReader(StringIO(data))
    
    return [r for r in rdr]

def run_scraper():
    content = fetch_entries()
    entries = parse_records(content)
    for e in entries:
        if not e[2].startswith('dra'):
            continue # samo drazbe!
        print e[2]
        kodict = {}
        # pdf
        print e
        if len(e) > 9:
            if e[9]:
                kodict.update(parsepdf(e[9]))
        # zadeva
        ko = find_ko(e[6])
        if ko:
            n = kodict.setdefault(ko, 0)
            kodict[ko] = n + 1
        # date
        date = e[1]
        today = datetime.date.today()
        today = datetime.datetime(today.year, today.month, today.day, 0, 0)
        if date > today:
            for ko in kodict.keys():
                for ll in get_ko(ko):
                    data = dict(zip(cols, e))
                    latlng = (float(ll['latitude']), float(ll['longitude']))
                    data['latitude'] = ll['latitude']
                    data['longitude'] = ll['longitude']
                    data['date'] = date.strftime("%Y-%m-%d %H:%M")
                    unique = ('dodatno','latitude','longitude','date')
                    scraperwiki.datastore.save(unique, data, date=date, latlng=latlng)

run_scraper()
