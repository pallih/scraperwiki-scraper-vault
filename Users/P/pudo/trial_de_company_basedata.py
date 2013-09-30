import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
from hashlib import sha1
from StringIO import StringIO 
import re, csv

REGISTERS = [
    'Genossenschaftsregister',
    'HRA',
    'HRB',
    'Partnerschaftsregister'
    ]

NAME_MAP = {
    "Rechtsform": "EntityType", 
    u'L\xc3\xb6schdatum': "DeletionDate",
    "Kapital": "FoundingCapital"
    }

BASE = "https://www.unternehmensregister.de/ureg/registerdocument.html?submitaction=registerdocument&ausdruckart=UT&gkz=%(xj_id)s&rtype=%(register)s&rnr=%(rnr)s&state=%(state)s&location="

TEST = "https://www.unternehmensregister.de/ureg/registerdocument.html?submitaction=registerdocument&iddok=null&ausdruckart=UT&gkz=D2601&gkzalt=&rtype=HRB&rnr=70438&cname=Microsoft+Deutschland+GmbH&state=2&location="

COURTS = "http://opendatalabs.org/flockscrape/amtsgerichte.csv"

def gerichte(_CTS=[]):
    if not len(_CTS):
        fh = StringIO(scraperwiki.scrape(COURTS))
        for row in csv.reader(fh, dialect='excel'):
            _CTS.append(row)
        fh.close()
    return _CTS

def generate_urls(consecutive_failures=0):
    for state_name, state_id, name, xj_id in gerichte():
        print "\n", "-" * 72
        print state_name, name
        for register in REGISTERS:
            print "\n", register
            for i in xrange(2000000):
                url = BASE % {
                    'state': state_id,
                    'xj_id': xj_id,
                    'register': register,
                    'rnr': i
                }
                if load_entry(url):
                    consecutive_failures = 0
                else: 
                    consecutive_failures += 1
                if consecutive_failures > 10000:
                    return


def load_entry(url):
    html = scraperwiki.scrape(url)
    html = html.replace("<br/>", "\n")
    if not "ureg-utdocument2.xsl" in html:
        return False
    doc = lxml.html.fromstring(html)
    last_key = None
    base = doc.find(".//div/div/div").xpath("string()").split("\n")
    base = [b.replace(u"\xc2\xa0", "").replace("  - ", "").strip() for b in base]
    base = [b for b in base if len(b)]
    data = {"Court": base[1], "CompanyRegister": base[2], "CompanyNumber": base[3], "CompanyName": base[4]}
    id = data.get("Court") + data.get("CompanyRegister") + data.get("CompanyNumber")
    data['UniqueID'] = sha1(id.encode("ascii", "ignore")).hexdigest()
    for elem in doc.findall(".//div"):
        if elem.get('class') == 'col1':
            last_key = elem.xpath("string()").strip()
            last_key = last_key.replace(":", "")
            if 'Eintragsdatum' in last_key: last_key = 'CreationDate'
            last_key = NAME_MAP.get(last_key, last_key)
        if elem.get('class') == 'col2':
            if 'Bilanz vorhanden' in last_key:
                opts = elem.findall('.//option')
                opts = [o.text for o in opts]
                if None in opts:
                    continue
                data['BalanceDates'] = "/".join(opts)
            elif 'Anschrift' in last_key:
                data['Address'] = elem.xpath("string()")
            elif last_key == 'CreationDate':
                cd, _ = elem.xpath("string()").strip().split("(", 1)
                data[last_key] = cd.strip()
            else:
                data[last_key] = elem.xpath("string()").strip()
    scraperwiki.datastore.save(["UniqueID"], data)
    return True

generate_urls()
#load_entry(TEST)import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
from hashlib import sha1
from StringIO import StringIO 
import re, csv

REGISTERS = [
    'Genossenschaftsregister',
    'HRA',
    'HRB',
    'Partnerschaftsregister'
    ]

NAME_MAP = {
    "Rechtsform": "EntityType", 
    u'L\xc3\xb6schdatum': "DeletionDate",
    "Kapital": "FoundingCapital"
    }

BASE = "https://www.unternehmensregister.de/ureg/registerdocument.html?submitaction=registerdocument&ausdruckart=UT&gkz=%(xj_id)s&rtype=%(register)s&rnr=%(rnr)s&state=%(state)s&location="

TEST = "https://www.unternehmensregister.de/ureg/registerdocument.html?submitaction=registerdocument&iddok=null&ausdruckart=UT&gkz=D2601&gkzalt=&rtype=HRB&rnr=70438&cname=Microsoft+Deutschland+GmbH&state=2&location="

COURTS = "http://opendatalabs.org/flockscrape/amtsgerichte.csv"

def gerichte(_CTS=[]):
    if not len(_CTS):
        fh = StringIO(scraperwiki.scrape(COURTS))
        for row in csv.reader(fh, dialect='excel'):
            _CTS.append(row)
        fh.close()
    return _CTS

def generate_urls(consecutive_failures=0):
    for state_name, state_id, name, xj_id in gerichte():
        print "\n", "-" * 72
        print state_name, name
        for register in REGISTERS:
            print "\n", register
            for i in xrange(2000000):
                url = BASE % {
                    'state': state_id,
                    'xj_id': xj_id,
                    'register': register,
                    'rnr': i
                }
                if load_entry(url):
                    consecutive_failures = 0
                else: 
                    consecutive_failures += 1
                if consecutive_failures > 10000:
                    return


def load_entry(url):
    html = scraperwiki.scrape(url)
    html = html.replace("<br/>", "\n")
    if not "ureg-utdocument2.xsl" in html:
        return False
    doc = lxml.html.fromstring(html)
    last_key = None
    base = doc.find(".//div/div/div").xpath("string()").split("\n")
    base = [b.replace(u"\xc2\xa0", "").replace("  - ", "").strip() for b in base]
    base = [b for b in base if len(b)]
    data = {"Court": base[1], "CompanyRegister": base[2], "CompanyNumber": base[3], "CompanyName": base[4]}
    id = data.get("Court") + data.get("CompanyRegister") + data.get("CompanyNumber")
    data['UniqueID'] = sha1(id.encode("ascii", "ignore")).hexdigest()
    for elem in doc.findall(".//div"):
        if elem.get('class') == 'col1':
            last_key = elem.xpath("string()").strip()
            last_key = last_key.replace(":", "")
            if 'Eintragsdatum' in last_key: last_key = 'CreationDate'
            last_key = NAME_MAP.get(last_key, last_key)
        if elem.get('class') == 'col2':
            if 'Bilanz vorhanden' in last_key:
                opts = elem.findall('.//option')
                opts = [o.text for o in opts]
                if None in opts:
                    continue
                data['BalanceDates'] = "/".join(opts)
            elif 'Anschrift' in last_key:
                data['Address'] = elem.xpath("string()")
            elif last_key == 'CreationDate':
                cd, _ = elem.xpath("string()").strip().split("(", 1)
                data[last_key] = cd.strip()
            else:
                data[last_key] = elem.xpath("string()").strip()
    scraperwiki.datastore.save(["UniqueID"], data)
    return True

generate_urls()
#load_entry(TEST)