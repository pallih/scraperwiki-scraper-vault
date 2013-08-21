# TODO:
# * scrape the other school subpages
# * handle occasionally mangled HTML on SchulListe.aspx
# * recover from disruptions (save_var, get_var)
#   - partially fixed
# * make integrating new data easy
# *

import scraperwiki
import lxml.html
import random
import re
from geopy import geocoders
import urllib2
import mechanize
import time
import unicodedata


##### CONSTANTS ##################################################


BASEURL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"
DETAILURLS = [
    "schulportrait.aspx?IDSchulzweig=",
    "schuelerschaft.aspx", "schulpersonal.aspx", "ressourcen.aspx",
    "schulprogramm.aspx", "modellschulversuche.aspx", "management.aspx"
]

LAST_IDSCHULZWEIG = scraperwiki.sqlite.get_var('last_idschulzweig', 0)

SCHULEN = []
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
FREMDSPRACHEN = [
    {u'FSID' : u"AGRC", u'FSName' : u"Alt-Griechisch"},
    {u'FSID' : u"CHIN", u'FSName' : u"Chinesisch"},
    {u'FSID' : u"ENGL", u'FSName' : u"Englisch"},
    {u'FSID' : u"FRAN", u'FSName' : u"Franz\u00f6sisch"},
    {u'FSID' : u"GRIE", u'FSName' : u"Griechisch"},
    {u'FSID' : u"ITAL", u'FSName' : u"Italienisch"},
    {u'FSID' : u"JAPN", u'FSName' : u"Japanisch"},
    {u'FSID' : u"LATN", u'FSName' : u"Latein"},
    {u'FSID' : u"POLN", u'FSName' : u"Polnisch"},
    {u'FSID' : u"PORT", u'FSName' : u"Portugiesisch"},
    {u'FSID' : u"RUSS", u'FSName' : u"Russisch"},
    {u'FSID' : u"SPAN", u'FSName' : u"Spanisch"},
    {u'FSID' : u"TRKS", u'FSName' : u"T\u00fcrkisch"}
]


scraperwiki.sqlite.attach("schulen-berlin-de-source", "source")
DICT_SOURCE = dict((d['IDSchulzweig'], d) for d in scraperwiki.sqlite.select("* FROM source.schule"))


##### UTILITY FUNCTIONS ##################################################


# initially lifted from https://bitbucket.org/ScraperWiki/scraperwiki/src/12572a4caeba/scraperlibs/python/scraperwiki/utils.py
# optional timeout, retries and delay parameters
# to speed up testing, tries to retrieve html fragments from our source scraper schulen-berlin-de-source first
# uses mechanize.urlopen to handle asp session crap for us. REMEMBER TO FETCH schulportrait.aspx FIRST, USING local=False
# optional fallbackurl param to request a second url before trying to refetch a url (as ugly fix for berlin.de asp stuff)
def scrape (url, fallbackurl=None, timeout=30, retries=5, delay=0, local=True) :
    match = re.match(str(re.escape(BASEURL + DETAILURLS[0]) + r"(\d+)"), url)
    if local and match:
        return DICT_SOURCE[int(match.group(1))]['schulportrait']

    url += "&rand="+str(random.randint(100, 999))  # append bogus argument to prevent caching
    for i in range(1,retries+1):
        try:
            fin  = mechanize.urlopen(url, timeout=timeout)
            text = fin.read()
            fin.close()   # get the mimetype here

            return text
        except urllib2.URLError as e:
            print "(try %i/10)%s Failed to retrieve %s" % (i, (" ["+str(e.code)+"]" if hasattr(e,'code') else ""), url)
            if i==retries: raise urllib2.URLError, e
            time.sleep(delay)
            mechanize.CookieJar().clear()
            if bool(fallbackurl):
                scrape(fallbackurl, local=False)


def scrape_and_assert_school(url, school, local=False):
    try:
        root = lxml.html.fromstring(scrape(url, BASEURL + DETAILURLS[0] + str(school['IDSchulzweig']), delay=30, local=local))
    # handle berlin.de internal server error issue on some pages
    except Exception as e:
        if url.endswith("?view=fehl&jahr=2005/06") and (hasattr(e,'code') and e.code==500):
            print "Skipped " + url + " on " + str(school['IDSchulzweig']) + "/" + school['SchulNr']
            return lxml.html.fromstring("<html></html>")
        else:
            raise e
    expected_school_str = school['SchulName'] + " - " + school['SchulNr']
    actual_school_str = root.cssselect('#ctl00_ContentPlaceHolderMenuListe_lblUebSchule, #ctl00_ContentPlaceHolderMenuListe_lblSchulname')[0].text_content()
    assert expected_school_str == actual_school_str, expected_school_str + " != " + unicodedata.normalize('NFKD', unicode(actual_school_str)).encode('ascii','ignore')
    error = root.cssselect('#ctl00_ContentPlaceHolderMenuListe_lblFehlermeldung')
    assert len(error) == 0 or not bool(error[0].text_content()), unicodedata.normalize('NFKD', unicode(error[0].text_content())).encode('ascii','ignore')
    return root


def merge_lists_of_dicts(l1, l2, key):
    d1 = dict((d[key], d) for d in l1)
    d2 = dict((d[key], d) for d in l2)
    dr = {}
    for k in d1.keys():
        try: dr[k].update(d1[k])
        except: dr[k] = dict(d1[k])
    for k in d2.keys():
        try: dr[k].update(d2[k])
        except: dr[k] = dict(d2[k])
    return dr.values()


def parse_table_row(rowhtml, cols):
    tds = rowhtml.cssselect("td")
    data = dict()
    col_index = 0
    for col in cols:
        if col:
            data[col] = tds[col_index].text_content().strip()
        col_index += 1
    return data


def scrape_tables_from_each_year_in_subpage(baseurl, urlparams, tablerow_css, tablerow_datacols, school):
    root = scrape_and_assert_school(baseurl+"?"+urlparams, school)
    year_list = root.cssselect('a[href*="'+urlparams+'&jahr="]')
    data_list = []
    data = school
    for year in year_list:
        year_str = year.text_content().strip().split()[0]
        root = scrape_and_assert_school(baseurl+"?"+urlparams+"&jahr="+year_str, school)
        rows = root.cssselect(tablerow_css)
        for row in rows:
            data = {
                'IDSchulzweig' : school['IDSchulzweig'],
                'SchulNr' : school['SchulNr'],
                'Schulzweig' : school['Schulzweig'],
                'Jahr' : year_str
            }
            data.update(parse_table_row(row, tablerow_datacols))
            data_list.append(data)
    return data_list


# zwei Strings mit Komma getrennt verbinden
def str_add_str (a, b):
    if len(a) and len(b):
        return a + ", " + b
    elif len(a):
        return a
    elif len(b):
        return b
    else:
        return ""


##### MAIN FUNCTIONS ##################################################


def run_scrape_on_list():
    print "Scraping school list ..."
    dict_IDSchulzweig = dict((d['IDSchulzweig'], d) for d in SCHULEN)
    root = lxml.html.fromstring(scrape(BASEURL + "SchulListe.aspx", local=False)) 
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
    SCHULEN = scraperwiki.sqlite.select("* FROM schule ORDER BY IDSchulzweig")


def scrape_leistungskurse(root, school):
    dict_LKName = dict((d['LKName'], d['LKID']) for d in LEISTUNGSKURSE)
    data_list = []
    lk_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblLeistungskurse")
    if len(lk_str):
        lk_str = lk_str[0].text_content().split(', ')
    for lk in lk_str:
        data_list.append({'IDSchulzweig' : school['IDSchulzweig'], 'LKID' : dict_LKName[lk]})
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'LKID'], data=data_list, table_name="schule_hat_lk")


def scrape_fremdsprachen(root, school):
    dict_FSName = dict((d['FSName'], d['FSID']) for d in FREMDSPRACHEN)
    data_list = []
    fs_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblSprachen")
    if len(fs_str):
        fs_str = fs_str[0].text_content().split(', ')
    for fs in fs_str:
        match = re.match(r"^S\d (.+)/(.+)$", fs)
        if match:
            data_list.append({'IDSchulzweig' : school['IDSchulzweig'], 'FSID' : dict_FSName[match.group(1)], 'FSTyp' : "1. Fremdsprache"})
            data_list.append({'IDSchulzweig' : school['IDSchulzweig'], 'FSID' : dict_FSName[match.group(2)], 'FSTyp' : "2. Fremdsprache"})
        else:
            li = fs.rsplit(' ', 1)
            if len(li) == 1:
                data_list.append({'IDSchulzweig' : school['IDSchulzweig'], 'FSID' : dict_FSName[li.pop()]})
            else:
                data_list.append({'IDSchulzweig' : school['IDSchulzweig'], 'FSID' : dict_FSName[li.pop()], 'FSTyp' : li.pop().strip()})
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'FSID'], data=data_list, table_name="schule_hat_fs")


# Text für Barrierefreiheit generieren
def get_accessibility_text (a, b, c, d):
    text = u""
    if a:
        text = str_add_str(text, u"Parkplatz f\xfcr Schwerbehinderte vorhanden")
    if b:
        text = str_add_str(text, u"rollstuhlgerechter Aufzug")
    if c:
        text = str_add_str(text, u"rollstuhlgerechtes WC")
    if d:
        text = str_add_str(text, u"zug\xe4nglich f\xfcr Rollstuhlbenutzer (ebenerdig oder mit Rampe)")
    return text


def scrape_schuldetails(root, school):
    data = school
    # address
    adr_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblStrasse")
    if len(adr_str):
        data['Adresse'] = adr_str[0].text_content().strip()
    ort_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblOrt")
    if len(ort_str) and len(ort_str[0].text_content().strip()):
        data['Adresse'] += ", " + re.sub(" \(" + school['Ortsteil'] + "\)" , "", ort_str[0].text_content().strip())
    # telephone no.
    tel_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblTelefon")
    if len(tel_str) and len(tel_str[0].text_content().strip()):
        data['tel'] = tel_str[0].text_content().strip()
    # web address
    www_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_HLinkWeb")
    if len(www_str) and len(www_str[0].text_content().strip()) and www_str[0].text_content().strip() != "[HLinkWeb]":
        data['www'] = www_str[0].text_content().strip()
    # school type (private/public)
    typ_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblSchulart")
    if len(typ_str):
        match = re.search(r"\( (.+) \)$", typ_str[0].text_content())
        if match:
            data['Schultyp'] = match.group(1).strip()
    # Ausstattung
    aut_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblAusstattung")
    if len(aut_str):
        data['Ausstattung'] = aut_str[0].text_content().strip()
    # Angebote und Budgetierung
    angebote = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAngebote")
    angebote_extrakt = ("", 0)
    if len(angebote):
        angebote_extrakt = re.subn("(Schule mit Teilnahme an der Budgetierung, )|((, )?Schule mit Teilnahme an der Budgetierung$)", "", angebote[0].text_content())
        if angebote_extrakt[1] > 0:
            data['Budgetierung'] = u"Schule mit Teilnahme an der Budgetierung"
    # Barrierefreiheit (aus Feld Zusätzliche Angebote)
    zusatz = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblZusatz")
    zs_extrakt_clean = ""
    if len(zusatz):
        zs_extrakt_1 = re.subn("(Parkplatz f\xfcr Schwerbehinderte vorhanden, )|((, )?Parkplatz f\xfcr Schwerbehinderte vorhanden$)", "", zusatz[0].text_content())
        zs_extrakt_2 = re.subn("(rollstuhlgerechter Aufzug, )|((, )?rollstuhlgerechter Aufzug$)", "", zs_extrakt_1[0])
        zs_extrakt_3 = re.subn("(rollstuhlgerechtes WC, )|((, )?rollstuhlgerechtes WC$)", "", zs_extrakt_2[0])
        zs_extrakt_4 = re.subn("(zug\xe4nglich  f\xfcr Rollstuhlbenutzer \(ebenerdig oder mit Rampe\), )" +
                "|((,  )?zug\xe4nglich f\xfcr Rollstuhlbenutzer \(ebenerdig oder mit Rampe\)$)", "", zs_extrakt_3[0])
        # jetzt noch vorangestellte Leerzeichen und Komma löschen
        zs_extrakt_clean = re.sub("^[ \n\r\t]*[,]?[ ]*", "", zs_extrakt_4[0])
        # Hinweis: Text der Barrierefreiheit wurde auseinander genommen und wird im nächsten Schritt wieder zusammengefügt,
        #          würde sich deshalb sehr einfach auch anders speichern lassen
        data['Barrierefreiheit'] = get_accessibility_text (zs_extrakt_1[1], zs_extrakt_2[1], zs_extrakt_3[1], zs_extrakt_4[1])
    # Angebote (ohne Budget aber mit Rest von Zusatz)
    data['Angebote'] = str_add_str(angebote_extrakt[0], zs_extrakt_clean)
    # Bemerkungen Schulzweig
    bem_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblBemerkungenSchulzweig")
    if len(bem_str):
        data['BemerkungenSchulzweig'] = bem_str[0].text_content().strip()
    # Arbeitsgemeinschaften
    ags_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAGs")
    if len(ags_str):
        data['AGs'] = ags_str[0].text_content().strip()
    # Außerschulische Partner
    par_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblPartner")
    if len(par_str):
        data['Partner'] = par_str[0].text_content().strip()
    # Duales Lernen
    dua_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblDualesLernen")
    if len(dua_str):
        data['DualesLernen'] = dua_str[0].text_content().strip()
    # Ganztagsschule
    gan_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblGanztags")
    if len(gan_str):
        data['Ganztagsschule'] = gan_str[0].text_content().strip()
    # Differenzierung
    dif_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblDiff")
    if len(dif_str):
        data['Differenzierung'] = dif_str[0].text_content().strip()
    # Mittagessen
    mit_str = root.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblMittag")
    if len(mit_str):
        data['Mittagessen'] = mit_str[0].text_content().strip()
    # fax no.
    fax_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblFax")
    if len(fax_str) and len(fax_str[0].text_content().strip()):
        data['fax'] = fax_str[0].text_content().strip()
    # email
    email_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_HLinkEMail")
    if len(email_str) and len(email_str[0].text_content().strip()) and email_str[0].text_content().strip() != "[HLinkEMail]":
        data['email'] = email_str[0].text_content().strip()
    # leitung
    leitung_str = root.cssselect("#ctl00_ContentPlaceHolderMenuListe_lblLeitung")
    if len(leitung_str):
        data['leitung'] = leitung_str[0] = leitung_str[0].text_content().strip()

    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data, table_name="schule")            


def scrape_schuelerschaft(school):
    # Jahrgangsstufen
    jgs = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[1], "view=jgs",
            "#ctl00_ContentPlaceHolderMenuListe_GridViewJahrgansstufen tr[class]", ["Jahrgangsstufe", "W", "M"], school)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'Jahr', 'Jahrgangsstufe'], data=jgs, table_name="jahrgangsstufe")            

    # Staatsangehörigkeit
    nat = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[1], "view=nat",
            "#ctl00_ContentPlaceHolderMenuListe_GridviewStaaten tr[class]", ["Staatsangehoerigkeit", "W", "M"], school)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'Jahr', 'Staatsangehoerigkeit'], data=nat, table_name="staatsangehoerigkeit")            

    # Nichtdeutsche Herkunftssprache
    ndh = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[1], "view=ndh",
            "#ctl00_ContentPlaceHolderMenuListe_GridViewNDH tr[class]", [None, "NdHS_W", "NdHS_M"], school)

    # Fehlzeiten
    fehl = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[1], "view=fehl",
            "#ctl00_ContentPlaceHolderMenuListe_GridviewFehl tr[class]:nth-of-type(2)", [None, "FQ", "FQU"], school)

    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'Jahr'], data=merge_lists_of_dicts(ndh, fehl, 'Jahr'), table_name="schuelerschaft")            


def scrape_personal(school):
    # Personal
    pers = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[2], "view=pers",
            "#ctl00_ContentPlaceHolderMenuListe_GridViewPersonal tr[class]", ["Bezeichnung", "W_in_prozent", "M_in_prozent", "Insgesamt"], school)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'Jahr', 'Bezeichnung'], data=pers, table_name="personal")            


def scrape_unterrichtsversorgung(school):
    # Unterrichtsversorgung

    UVERS_STRS = [
        {u'Unterrichtsbedarf in Stunden' : u"U_Bedarf_in_h"},
        {u'Lehrerkr\xe4ftebestand in Stunden' : u"L_Bestand_in_h"},
        {u'Bilanz in Stunden' : u"Bilanz_in_h"},
        {u'Bilanz in %' : u"Bilanz_in_Prozent"},
        {u'davon Grundbedarf' : u"davon_Grundbedarf"},
        {u'davon Zusatzbedarf' : u"davon_Zusatzbedarf"},
        {u'nachrichtlich Profilbedarf in Stunden' : u"Profilbedarf_in_h"}
    ]

    uvers = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[2], "view=uvers",
            "#ctl00_ContentPlaceHolderMenuListe_GridviewUVers tr[class]", ["key", "value"], school)
    print uvers
    result = []
    for row in uvers:
        if result[row['Jahr']]:
            result[row['Jahr']].update()



def scrape_ressourcen(school):
    # IT-Ausstattung (PCs)
    itaus = scrape_tables_from_each_year_in_subpage(BASEURL+DETAILURLS[3], "view=itaus",
            "#ctl00_ContentPlaceHolderMenuListe_GridViewITAus tr[class]", ["PCs_Insgesamt", "Multimedia", "nicht_Multimedia", "Fachraum", "Klassenraum", "Mobil"], school)
    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig', 'Jahr'], data=itaus, table_name="ausstattung")            


def run_scrape_on_details():
    global LAST_IDSCHULZWEIG

    school_list = [x for x in SCHULEN if x['IDSchulzweig']>LAST_IDSCHULZWEIG]
    print "Scraping detail pages of " + str(len(school_list)) + "/" + str(len(SCHULEN)) + " schools ..."
    for school in school_list:
        print "Scraping " + school['SchulNr'] + " : " + BASEURL + DETAILURLS[0] + str(school['IDSchulzweig'])
        root = scrape_and_assert_school(BASEURL + DETAILURLS[0] + str(school['IDSchulzweig']), school)
#        scrape_schuldetails(root, school)
#        scrape_leistungskurse(root, school)
#        scrape_fremdsprachen(root, school)
#        scrape_schuelerschaft(school)
#        scrape_personal(school)
        scrape_unterrichtsversorgung(school)
#        scrape_ressourcen(school)

        scraperwiki.sqlite.save_var('last_idschulzweig', school['IDSchulzweig'])
        LAST_IDSCHULZWEIG = school['IDSchulzweig']


def geocode():
    print "Geocoding school addresses ..."
    for school in [x for x in SCHULEN if not x['lat'] or not x['lon']]:
        try:
            g = geocoders.Google(domain='maps.google.de')
            _, (school['lat'],school['lon']) = g.geocode(unicodedata.normalize('NFKD', unicode(school['Adresse'])).encode('ascii','ignore'))
            print "%s: %s [%f,%f]" % (school['SchulNr'], school['Adresse'], school['lat'], school['lon'])
            scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=school, table_name="schule")
        except:
            print school['SchulNr'] + ": " + "ERROR - couldn't get geodata.", school


def main():
    global SCHULEN, LEISTUNGSKURSE

#    print "Dropping all tables and starting over ..."
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS swvariables")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schule")
#    scraperwiki.sqlite.execute("CREATE TABLE schule (IDSchulzweig integer, SchulNr text, SchulName text, " +
#            "Schulzweig text, Schultyp text, Adresse text, Bezirk text, Ortsteil text, lat real, lon real, " +
#            "tel text, www text, Ausstattung text)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schule_hat_lk")
#    scraperwiki.sqlite.execute("CREATE TABLE schule_hat_lk (IDSchulzweig integer, LKID text)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schule_hat_fs")
#    scraperwiki.sqlite.execute("CREATE TABLE schule_hat_fs (IDSchulzweig integer, FSID text, FSTyp text)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS lk")
#    scraperwiki.sqlite.save(unique_keys=["LKID"], data=LEISTUNGSKURSE, table_name="lk")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS fs")
#    scraperwiki.sqlite.save(unique_keys=["FSID"], data=FREMDSPRACHEN, table_name="fs")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS jahrgangsstufe")
#    scraperwiki.sqlite.execute("CREATE TABLE jahrgangsstufe (IDSchulzweig integer, SchulNr text, Schulzweig text, Jahr text, Jahrgangsstufe text, W text, M text)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS staatsangehoerigkeit")
#    scraperwiki.sqlite.execute("CREATE TABLE staatsangehoerigkeit (IDSchulzweig integer, SchulNr text, " +
#            "Schulzweig text, Jahr text, Staatsangehoerigkeit text, W integer, M integer)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS schuelerschaft")
#    scraperwiki.sqlite.execute("CREATE TABLE schuelerschaft (IDSchulzweig integer, SchulNr text, Schulzweig text, " +
#            "Jahr text, NdHS_W integer, NdHS_M integer, FQ real, FQU real)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS personal")
#    scraperwiki.sqlite.execute("CREATE TABLE personal (IDSchulzweig integer, SchulNr text, Schulzweig text, Jahr text, " +
#            "Bezeichnung text, W_in_prozent integer, M_in_prozent integer, Insgesamt integer)")
#    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS ausstattung")
#    scraperwiki.sqlite.execute("CREATE TABLE ausstattung (IDSchulzweig integer, SchulNr text, Schulzweig text, Jahr text, " +
#            "PCs_Insgesamt integer, Multimedia integer, nicht_Multimedia integer, Mobil integer, Fachraum integer, Klassenraum integer)")

    try:
        SCHULEN = scraperwiki.sqlite.select("* FROM schule ORDER BY IDSchulzweig")
    except:
        print "Looks like we're running the scraper for the first time ..."
#    run_scrape_on_list()
#    run_scrape_on_details()
    geocode()
    scraperwiki.sqlite.save_var('last_idschulzweig', 0)

main()
