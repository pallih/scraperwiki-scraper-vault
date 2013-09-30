# Raapija joka etsii Tekes-tuen saaneiden yritysten tiedot Kauppalehden yrityshausta

import scraperwiki
import urllib
import csv
import time
import sys
from lxml import etree

# how many companies to fetch data for (takes >5 secs wall clock time per company!)
LIMIT = 5
#LIMIT = 100

# delay between requests
DELAY = 1 # be nice and follow what robots.txt says
#DELAY = 0 # for quicker testing with small runs

SEARCHURL = 'http://www.kauppalehti.fi/5/i/yritykset/yrityshaku/hakutulos.jsp?from=0&amount=25&query='
parser = etree.HTMLParser()


#scraperwiki.metadata.save('lastidx', 0)
scraperwiki.metadata.save('data_columns', ['Idx','Tekes-nimi','Nykyinen nimi','Y-tunnus',
                                           'KR alkanut','KR päättynyt','Toimiala',
                                           'Tila','Yhtiömuoto','Kotipaikka'])             

# more robust version of etree.parse(), tries up to 3 times
def try_parse(url):
    for i in range(3):
        try:
            return etree.parse(url, parser=parser)
        except:
            pass
    # ei onnistunut...
    return None
    

# Selvitä ja palauta yrityksen sivun URL nimen perusteella käyttäen Kauppalehden hakutoimintoa.
def hae_url(nimi):
    # Kauppalehti vaatii Latin1-merkistön...
    nimi_latin1 = nimi.decode('utf-8').encode('latin1', 'replace')
    url = SEARCHURL + urllib.quote_plus(nimi_latin1)
    tree = try_parse(url)
    if tree is None or tree.getroot() is None: return []
    time.sleep(DELAY)

    results = tree.findall("//p[@class='cs-results-company']")

    return [res[0].get('href') + "?print=true" for res in results]


# Hae tarkat yritystiedot tietystä URL:stä ja tallenna scraperwikin kantaan
def hae_tiedot(alkupnimi, url):
    tree = try_parse(url)
    if tree is None or tree.getroot() is None:
        return None
    time.sleep(DELAY)
    nykynimi   = tree.findtext("//dd[@id='cs-company-name']")
    ytunnus    = tree.findtext("//dd[@id='cs-company-bid']")
    toimiala   = tree.findtext("//dd[@id='cs-company-industry']")
    tila       = tree.findtext("//dd[@id='cs-company-state']")
    yhtiomuoto = tree.findtext("//dd[@id='cs-company-cform']")
    kieli      = tree.findtext("//dd[@id='cs-company-lang']")
    kotipaikka = tree.findtext("//dd[@id='cs-company-location']")

    # selvitä kaupparekisterimerkinnän alkamis- ja loppumispäivä
    # näitä tietoja ei aina ole joten yritetään olla hajoamatta...
    kr_alkanut = None
    kr_paattynyt = None

    try:
        rekisteroinnit = tree.findall("//h3")[3].getnext()
    except:
        rekisteroinnit = None

    if rekisteroinnit is not None:
        try:
            kr_alkanut = rekisteroinnit[4][1].text
        except:
            pass

        try:
            kr_paattynyt = rekisteroinnit[4][2].text
        except:
            pass

    return {"Tekes-nimi": alkupnimi,
            "Nykyinen nimi": nykynimi,
            "Y-tunnus": ytunnus,
            "Toimiala": toimiala,
            "Tila": tila,
            "Yhtiömuoto": yhtiomuoto,
            "Kotipaikka": kotipaikka,
            "KR alkanut": kr_alkanut,
            "KR päättynyt": kr_paattynyt,
}


# Main program starts here...

# Get a list of Tekes funding
url = "https://spreadsheets.google.com/pub?hl=en&hl=en&key=0AjQc06lkm17CdGJ5R241aDh4LW5rS1JfeURjYWItdWc&output=csv"
f = urllib.urlopen(url)
lines = f.readlines()
clist = list(csv.reader(lines[1:]))

# find unique company names and sort alphabetically by name
yritysnimet = sorted(set([tuensaaja[0] for tuensaaja in clist]))

# find out where scraping stopped last time and continue from there
lastidx = scraperwiki.metadata.get('lastidx', default=0)


# skip through every company name, find out its URL, retrieve company information and save in datastore
for i in xrange(LIMIT):
    idx = (lastidx + 1 + i) % len(yritysnimet)
    nimi = yritysnimet[idx]
#    print "nimi:", nimi
    alkupnimi = nimi

    if nimi.find('(') != -1:
        nimi = nimi.split('(')[0].strip()
        print "muunnettiin haettava nimi: '%s' -> '%s'" % (alkupnimi, nimi)
    if nimi.find(' - ') != -1:
        nimi = nimi.replace(' - ',' ')
        print "muunnettiin haettava nimi: '%s' -> '%s'" % (alkupnimi, nimi)

    urls = hae_url(nimi)
    if len(urls) == 0:
        print "Yritystä ei löytynyt:", nimi
        continue
    for url in urls:
        data = hae_tiedot(alkupnimi, url)
        if data is None:
            print "Tarkkoja tietoja ei saatu:", nimi, url
            continue
        data['Idx'] = idx

        tries = 10
        while tries > 0: # try many times, since the method occasionally fails
            try:
                scraperwiki.datastore.save(unique_keys=["Y-tunnus"], data=data)
                break
            except Exception as exc:
                print "scraperwiki.datastore.save() failed, trying again. Exception:", exc
                time.sleep(1)
                tries -= 1
        if tries == 0:
            print "datastore failed, exiting"
            sys.exit(1)

    # occasionally mark where we are in the list so the next scrape can continue from that point
    if idx % 10 == 0:
        try:
            scraperwiki.metadata.save('lastidx', idx)
        except Exception as exc:
            print "periodic metadata save failed, skipping. Exception:", exc

print "All done!"
# Raapija joka etsii Tekes-tuen saaneiden yritysten tiedot Kauppalehden yrityshausta

import scraperwiki
import urllib
import csv
import time
import sys
from lxml import etree

# how many companies to fetch data for (takes >5 secs wall clock time per company!)
LIMIT = 5
#LIMIT = 100

# delay between requests
DELAY = 1 # be nice and follow what robots.txt says
#DELAY = 0 # for quicker testing with small runs

SEARCHURL = 'http://www.kauppalehti.fi/5/i/yritykset/yrityshaku/hakutulos.jsp?from=0&amount=25&query='
parser = etree.HTMLParser()


#scraperwiki.metadata.save('lastidx', 0)
scraperwiki.metadata.save('data_columns', ['Idx','Tekes-nimi','Nykyinen nimi','Y-tunnus',
                                           'KR alkanut','KR päättynyt','Toimiala',
                                           'Tila','Yhtiömuoto','Kotipaikka'])             

# more robust version of etree.parse(), tries up to 3 times
def try_parse(url):
    for i in range(3):
        try:
            return etree.parse(url, parser=parser)
        except:
            pass
    # ei onnistunut...
    return None
    

# Selvitä ja palauta yrityksen sivun URL nimen perusteella käyttäen Kauppalehden hakutoimintoa.
def hae_url(nimi):
    # Kauppalehti vaatii Latin1-merkistön...
    nimi_latin1 = nimi.decode('utf-8').encode('latin1', 'replace')
    url = SEARCHURL + urllib.quote_plus(nimi_latin1)
    tree = try_parse(url)
    if tree is None or tree.getroot() is None: return []
    time.sleep(DELAY)

    results = tree.findall("//p[@class='cs-results-company']")

    return [res[0].get('href') + "?print=true" for res in results]


# Hae tarkat yritystiedot tietystä URL:stä ja tallenna scraperwikin kantaan
def hae_tiedot(alkupnimi, url):
    tree = try_parse(url)
    if tree is None or tree.getroot() is None:
        return None
    time.sleep(DELAY)
    nykynimi   = tree.findtext("//dd[@id='cs-company-name']")
    ytunnus    = tree.findtext("//dd[@id='cs-company-bid']")
    toimiala   = tree.findtext("//dd[@id='cs-company-industry']")
    tila       = tree.findtext("//dd[@id='cs-company-state']")
    yhtiomuoto = tree.findtext("//dd[@id='cs-company-cform']")
    kieli      = tree.findtext("//dd[@id='cs-company-lang']")
    kotipaikka = tree.findtext("//dd[@id='cs-company-location']")

    # selvitä kaupparekisterimerkinnän alkamis- ja loppumispäivä
    # näitä tietoja ei aina ole joten yritetään olla hajoamatta...
    kr_alkanut = None
    kr_paattynyt = None

    try:
        rekisteroinnit = tree.findall("//h3")[3].getnext()
    except:
        rekisteroinnit = None

    if rekisteroinnit is not None:
        try:
            kr_alkanut = rekisteroinnit[4][1].text
        except:
            pass

        try:
            kr_paattynyt = rekisteroinnit[4][2].text
        except:
            pass

    return {"Tekes-nimi": alkupnimi,
            "Nykyinen nimi": nykynimi,
            "Y-tunnus": ytunnus,
            "Toimiala": toimiala,
            "Tila": tila,
            "Yhtiömuoto": yhtiomuoto,
            "Kotipaikka": kotipaikka,
            "KR alkanut": kr_alkanut,
            "KR päättynyt": kr_paattynyt,
}


# Main program starts here...

# Get a list of Tekes funding
url = "https://spreadsheets.google.com/pub?hl=en&hl=en&key=0AjQc06lkm17CdGJ5R241aDh4LW5rS1JfeURjYWItdWc&output=csv"
f = urllib.urlopen(url)
lines = f.readlines()
clist = list(csv.reader(lines[1:]))

# find unique company names and sort alphabetically by name
yritysnimet = sorted(set([tuensaaja[0] for tuensaaja in clist]))

# find out where scraping stopped last time and continue from there
lastidx = scraperwiki.metadata.get('lastidx', default=0)


# skip through every company name, find out its URL, retrieve company information and save in datastore
for i in xrange(LIMIT):
    idx = (lastidx + 1 + i) % len(yritysnimet)
    nimi = yritysnimet[idx]
#    print "nimi:", nimi
    alkupnimi = nimi

    if nimi.find('(') != -1:
        nimi = nimi.split('(')[0].strip()
        print "muunnettiin haettava nimi: '%s' -> '%s'" % (alkupnimi, nimi)
    if nimi.find(' - ') != -1:
        nimi = nimi.replace(' - ',' ')
        print "muunnettiin haettava nimi: '%s' -> '%s'" % (alkupnimi, nimi)

    urls = hae_url(nimi)
    if len(urls) == 0:
        print "Yritystä ei löytynyt:", nimi
        continue
    for url in urls:
        data = hae_tiedot(alkupnimi, url)
        if data is None:
            print "Tarkkoja tietoja ei saatu:", nimi, url
            continue
        data['Idx'] = idx

        tries = 10
        while tries > 0: # try many times, since the method occasionally fails
            try:
                scraperwiki.datastore.save(unique_keys=["Y-tunnus"], data=data)
                break
            except Exception as exc:
                print "scraperwiki.datastore.save() failed, trying again. Exception:", exc
                time.sleep(1)
                tries -= 1
        if tries == 0:
            print "datastore failed, exiting"
            sys.exit(1)

    # occasionally mark where we are in the list so the next scrape can continue from that point
    if idx % 10 == 0:
        try:
            scraperwiki.metadata.save('lastidx', idx)
        except Exception as exc:
            print "periodic metadata save failed, skipping. Exception:", exc

print "All done!"
