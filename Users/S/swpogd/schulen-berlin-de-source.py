import scraperwiki
import lxml.html
import random
import urllib2
import mechanize

BASEURL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"
DETAILURLS = [
    "schulportrait.aspx?IDSchulzweig=",
    "schuelerschaft.aspx", "schulpersonal.aspx", "ressourcen.aspx",
    "schulprogramm.aspx", "modellschulversuche.aspx", "management.aspx"
]

SCHULEN = []
LAST_IDSCHULZWEIG = scraperwiki.sqlite.get_var('last_idschulzweig', 0)


# lifted from https://bitbucket.org/ScraperWiki/scraperwiki/src/12572a4caeba/scraperlibs/python/scraperwiki/utils.py
# added timeout parameter and retries
# using mechanize.urlopen to handle asp session crap for us. REMEMBER TO FETCH schulportrait.aspx FIRST, USING local=False.
def scrape (url, params = None, timeout = 30, local = True) :
    data = params and urllib.urlencode(params) or None

    for i in range(1,11):
        try:
            #fin  = urllib2.urlopen(url, data, timeout)
            fin  = mechanize.urlopen(url, data, timeout)
            text = fin.read()
            fin.close()   # get the mimetype here
        
            return text
        except urllib2.URLError as e:
            print "(try %i/10) Failed to scrape %s" % (i, url)
    raise urllib2.URLError


def run_scrape_on_list():
    print "Scraping school list ..."
    dict_IDSchulzweig = dict((d['IDSchulzweig'], d) for d in SCHULEN)
    root = lxml.html.fromstring(scrape(BASEURL + "SchulListe.aspx?rand=" 
            + str(random.randint(100, 999)))) # append bogus argument to prevent caching
    data_list = []
    for tr in root.cssselect("#GridViewSchulen tr[class]"):
        tds = tr.cssselect("td")
        IDSchulzweig = int(tds[0].cssselect("a")[0].attrib.get("href").rsplit('=', 1)[1])
        data = ({'IDSchulzweig' : IDSchulzweig} if not IDSchulzweig in dict_IDSchulzweig else dict_IDSchulzweig[IDSchulzweig])
        data.update({
            'SchulNr' : tds[0].text_content().strip(),
            'SchulName' : tds[1].text_content().strip(),
            'Schulzweig' : tds[2].text_content().strip(),
            'Bezirk' : tds[3].text_content().strip(),
            'Ortsteil' : tds[4].text_content().strip()
        })
        data_list.append(data)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data_list, table_name="schule")


def run_scrape_on_details():
    global LAST_IDSCHULZWEIG

    school_list = [x for x in SCHULEN if x['IDSchulzweig']>LAST_IDSCHULZWEIG]
    print "Scraping detail pages of " + str(len(school_list)) + "/" + str(len(SCHULEN)) + " schools ..."
    for school in school_list:
        root = lxml.html.fromstring(scrape(BASEURL + DETAILURLS[0] + str(school['IDSchulzweig'])))
        html = lxml.html.tostring(root.cssselect("#divAllgemein")[0])
        data = school
        data.update({
            'schulportrait' : html
        })
        scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data, table_name="schule")
        scraperwiki.sqlite.save_var('last_idschulzweig', school['IDSchulzweig'])
        LAST_IDSCHULZWEIG = school['IDSchulzweig']


def main():
    global SCHULEN, LEISTUNGSKURSE

#    print "Dropping all tables and starting over ..."
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swvariables")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schule")

    try:
        SCHULEN = scraperwiki.sqlite.select("* FROM schule ORDER BY IDSchulzweig")
    except:
        print "Looks like we're running the scraper for the first time ..."
#    run_scrape_on_list()
    SCHULEN = scraperwiki.sqlite.select("* FROM schule ORDER BY IDSchulzweig")
    run_scrape_on_details()
    scraperwiki.sqlite.save_var('last_idschulzweig', 0)

main()
