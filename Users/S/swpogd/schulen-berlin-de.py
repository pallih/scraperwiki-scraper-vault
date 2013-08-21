# TODO:
# * handle occasionally mangled HTML on SchulListe.aspx
# * find out wtf is causing the scraper to hang itself up randomly
#   - seems to time out in scraperwiki.scrape() - is it possible to set a shorter timeout on this?
# * recover from disruptions (save_var, get_var)
# * make integrating new data easy
# * add multithreading, if feasible
# *

import scraperwiki
import lxml.html
import random
import re
from geopy import geocoders
#import mechanize  # probably needed once we want to scrape the subpages of schools (https://scraperwiki.com/scrapers/new/python?template=advanced-scraping-aspx-pages)

BASEURL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"
DETAILURLS = [
    "schulportrait.aspx?IDSchulzweig=",
    "schuelerschaft.aspx", "schulpersonal.aspx", "ressourcen.aspx",
    "schulprogramm.aspx", "modellschulversuche.aspx", "management.aspx"
]

SCHULEN = []
FREMDSPRACHEN = []
LEISTUNGSKURSE = [
    {u'LKID' : u"BIOL", u'LKName' : u"Biologie"},
    {u'LKID' : u"BTEC", u'LKName' : u"Biotechnologie"},
    {u'LKID' : u"CHEM", u'LKName' : u"Chemie"},
    {u'LKID' : u"DEUT", u'LKName' : u"Deutsch"},
    {u'LKID' : u"ENGL", u'LKName' : u"Englisch"},
    {u'LKID' : u"ERDK", u'LKName' : u"Erdkunde"},
    {u'LKID' : u"ELWI", u'LKName' : u"Ern\xe4hrungs-/Lebensmittelwissenschaft"},
    {u'LKID' : u"EREL", u'LKName' : "Evangelische Religionslehre"},
    {u'LKID' : u"FRAN", u'LKName' : u"Franz\xf6sisch"},
    {u'LKID' : u"GESC", u'LKName' : u"Geschichte"},
    {u'LKID' : u"GESU", u'LKName' : u"Gesundheit"},
    {u'LKID' : u"GMET", u'LKName' : u"Gestaltungs- und Medientechnik"},
    {u'LKID' : u"GRIE", u'LKName' : u"Griechisch"},
    {u'LKID' : u"INFO", u'LKName' : u"Informatik/Informationsverarbeitung"},
    {u'LKID' : u"ITAL", u'LKName' : u"Italienisch"},
    {u'LKID' : u"JAPN", u'LKName' : u"Japanisch"},
    {u'LKID' : u"JREL", u'LKName' : u"J\xfcdische Religion / Philosophie"},
    {u'LKID' : u"KUNS", u'LKName' : u"Bildende Kunst/Kunst"},
    {u'LKID' : u"LATN", u'LKName' : u"Latein"},
    {u'LKID' : u"MATH", u'LKName' : u"Mathematik"},
    {u'LKID' : u"MUSI", u'LKName' : u"Musik"},
    {u'LKID' : u"PHIL", u'LKName' : u"Philosophie"},
    {u'LKID' : u"PHYS", u'LKName' : u"Physik"},
    {u'LKID' : u"PORT", u'LKName' : u"Portugiesisch"},
    {u'LKID' : u"POWE", u'LKName' : u"Politische Weltkunde"},
    {u'LKID' : u"RECH", u'LKName' : u"Recht"},
    {u'LKID' : u"RUSS", u'LKName' : u"Russisch"},
    {u'LKID' : u"SOZW", u'LKName' : u"Sozialwissenschaften"},
    {u'LKID' : u"SPAN", u'LKName' : u"Spanisch"},
    {u'LKID' : u"SPRT", u'LKName' : u"Sport/ Leibes\xfcbungen"},
    {u'LKID' : u"TRKS", u'LKName' : u"T\xfcrkisch"},
    {u'LKID' : u"WINF", u'LKName' : u"Wirtschaftsinformatik"},
    {u'LKID' : u"WIWI", u'LKName' : u"Wirtschaftswissenschaft/-lehre"}
]

LAST_IDSCHULZWEIG = scraperwiki.sqlite.get_var('last_idschulzweig', 0)



def run_scrape_on_list():
    """

    """

    print "Scraping school list ..."
    root = lxml.html.fromstring(scraperwiki.scrape( BASEURL + "SchulListe.aspx?rand=" + str(random.randint(100, 999)) ))  # append bogus argument to prevent caching
    data_list = []
    for tr in root.cssselect("#GridViewSchulen tr[class]"):
        tds = tr.cssselect("td")
        print tds
        data = {
            'SchulNr' : tds[0].text_content().strip(),
            'IDSchulzweig' : int(tds[0].cssselect("a")[0].attrib.get("href").rsplit('=', 1)[1]),
            'SchulName' : tds[1].text_content().strip(),
            'Schulzweig' : tds[2].text_content().strip(),
            'Bezirk' : tds[3].text_content().strip(),
            'Ortsteil' : tds[4].text_content().strip()
        }
        data_list.append(data)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data_list, table_name="schule")


def scrape_leistungskurse(root, school, lk_name_map):
    """

    """

    data_list = []
    lk_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblLeistungskurse")
    if len(lk_str):
        lk_str = lk_str[0].text_content().split(', ')
    for lk in lk_str:
        data = {
            'IDSchulzweig' : school['IDSchulzweig'],
            'LKID' : lk_name_map[lk]
        }
        data_list.append(data)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'LKID'], data=data_list, table_name="schule_hat_lk")


def scrape_adresse(root, school):
    """

    """

    data = school
    adr_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblStrasse")
    if len(adr_str):
        data['Adresse'] = adr_str[0].text_content()
    ort_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblOrt")
    if len(ort_str) and len(ort_str[0]):
        data['Adresse'] += ", " + re.sub(" \("+school['Ortsteil']+"\)" , "", ort_str[0].text_content())
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data, table_name="schule")


def run_scrape_on_details():
    """

    """

    global LAST_IDSCHULZWEIG

    lk_name_map = dict((d['LKName'], d['LKID']) for d in LEISTUNGSKURSE)
    school_list = [x for x in SCHULEN if x['IDSchulzweig']>LAST_IDSCHULZWEIG]
    print "Scraping detail pages of " + str(len(school_list)) + "/" + str(len(SCHULEN)) + " schools ..."
    for school in school_list:
        root = lxml.html.fromstring(scraperwiki.scrape(BASEURL + DETAILURLS[0] + str(school['IDSchulzweig'])))
        scrape_leistungskurse(root, school, lk_name_map)
        scrape_adresse(root, school)

        scraperwiki.sqlite.save_var('last_idschulzweig', school['IDSchulzweig'])
        LAST_IDSCHULZWEIG = school['IDSchulzweig']


def geocode():
    """

    """

    print "Geocoding school addresses ..."
    for school in [x for x in SCHULEN if not x['lat'] or not x['lon']]:
        try:
            g = geocoders.Google(domain='maps.google.de')
            _, (school['lat'],school['lon']) = g.geocode(school['Adresse'])
            print "%s: %s [%f,%f]" % (school['SchulNr'], school['Adresse'], school['lat'], school['lon'])
            scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=school, table_name="schule")
        except:
            print school['SchulNr'] + ": " + "ERROR - couldn't get geodata.", school


def main():
    """

    """

    global SCHULEN, LEISTUNGSKURSE

#    if not LAST_IDSCHULZWEIG:
#        print "Dropping all tables and starting over ..."
#        scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swvariables")
#        scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schule")
#        scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schule_hat_lk")
#        scraperwiki.sqlite.execute("CREATE TABLE schule_hat_lk (IDSchulzweig integer, LKID text)")
#        run_scrape_on_list()

    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS lk")
    scraperwiki.sqlite.save(unique_keys=["LKID"], data=LEISTUNGSKURSE, table_name="lk")
    LEISTUNGSKURSE = scraperwiki.sqlite.select("* FROM lk")
    SCHULEN = scraperwiki.sqlite.select("* FROM schule ORDER BY IDSchulzweig")
    run_scrape_on_details()
#    geocode()
    scraperwiki.sqlite.save_var('last_idschulzweig', 0)

main()
