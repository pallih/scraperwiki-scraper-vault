import scraperwiki
import lxml.html
import re

def str_add_str (a, b): #zwei Strings mit Komma getrennt verbinden
    if len(a) and len(b):
        return a + ", " + b
    elif len(a):
        return a
    elif len(b):
        return b
    else:
        return ""

def get_accessibility_text (a, b, c, d): #Text für Barrierefreiheit generieren
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

data_list = []
scraperwiki.sqlite.attach("schulen-berlin-de-source", "source")
all = scraperwiki.sqlite.select("* FROM source.schule")

for school in all:
    print school['SchulName']
    data = {'IDSchulzweig' : school['IDSchulzweig'], 'SchulName' : school['SchulName']}
    html = school['schulportrait']
    page = lxml.html.fromstring(html)

    angebote = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAngebote")
    angebote_extrakt = ("", 0)
    if len(angebote):
        angebote_extrakt = re.subn("(Schule mit Teilnahme an der Budgetierung, )|((, )?Schule mit Teilnahme an der Budgetierung$)", "", angebote[0].text_content())
        if angebote_extrakt[1] > 0:
            data['Budgetierung'] = u"Schule mit Teilnahme an der Budgetierung"

    zusatz = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblZusatz")
    zs_extrakt_clean = ""
    if len(zusatz):
        zs_extrakt_1 = re.subn("(Parkplatz f\xfcr Schwerbehinderte vorhanden, )|((, )?Parkplatz f\xfcr Schwerbehinderte vorhanden$)", "", zusatz[0].text_content())
        zs_extrakt_2 = re.subn("(rollstuhlgerechter Aufzug, )|((, )?rollstuhlgerechter Aufzug$)", "", zs_extrakt_1[0])
        zs_extrakt_3 = re.subn("(rollstuhlgerechtes WC, )|((, )?rollstuhlgerechtes WC$)", "", zs_extrakt_2[0])
        zs_extrakt_4 = re.subn("(zug\xe4nglich f\xfcr Rollstuhlbenutzer \(ebenerdig oder mit Rampe\), )|((, )?zug\xe4nglich f\xfcr Rollstuhlbenutzer \(ebenerdig oder mit Rampe\)$)", "", zs_extrakt_3[0])
        zs_extrakt_clean = re.sub("^[ \n\r\t]*[,]?[ ]*", "", zs_extrakt_4[0])
        data['Barrierefreiheit'] = get_accessibility_text (zs_extrakt_1[1], zs_extrakt_2[1], zs_extrakt_3[1], zs_extrakt_4[1])

    data['Angebote'] = str_add_str(angebote_extrakt[0], zs_extrakt_clean)
    data_list.append(data)

scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data_list, table_name="angebote")

import scraperwiki
import lxml.html
import re

def str_add_str (a, b): #zwei Strings mit Komma getrennt verbinden
    if len(a) and len(b):
        return a + ", " + b
    elif len(a):
        return a
    elif len(b):
        return b
    else:
        return ""

def get_accessibility_text (a, b, c, d): #Text für Barrierefreiheit generieren
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

data_list = []
scraperwiki.sqlite.attach("schulen-berlin-de-source", "source")
all = scraperwiki.sqlite.select("* FROM source.schule")

for school in all:
    print school['SchulName']
    data = {'IDSchulzweig' : school['IDSchulzweig'], 'SchulName' : school['SchulName']}
    html = school['schulportrait']
    page = lxml.html.fromstring(html)

    angebote = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAngebote")
    angebote_extrakt = ("", 0)
    if len(angebote):
        angebote_extrakt = re.subn("(Schule mit Teilnahme an der Budgetierung, )|((, )?Schule mit Teilnahme an der Budgetierung$)", "", angebote[0].text_content())
        if angebote_extrakt[1] > 0:
            data['Budgetierung'] = u"Schule mit Teilnahme an der Budgetierung"

    zusatz = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblZusatz")
    zs_extrakt_clean = ""
    if len(zusatz):
        zs_extrakt_1 = re.subn("(Parkplatz f\xfcr Schwerbehinderte vorhanden, )|((, )?Parkplatz f\xfcr Schwerbehinderte vorhanden$)", "", zusatz[0].text_content())
        zs_extrakt_2 = re.subn("(rollstuhlgerechter Aufzug, )|((, )?rollstuhlgerechter Aufzug$)", "", zs_extrakt_1[0])
        zs_extrakt_3 = re.subn("(rollstuhlgerechtes WC, )|((, )?rollstuhlgerechtes WC$)", "", zs_extrakt_2[0])
        zs_extrakt_4 = re.subn("(zug\xe4nglich f\xfcr Rollstuhlbenutzer \(ebenerdig oder mit Rampe\), )|((, )?zug\xe4nglich f\xfcr Rollstuhlbenutzer \(ebenerdig oder mit Rampe\)$)", "", zs_extrakt_3[0])
        zs_extrakt_clean = re.sub("^[ \n\r\t]*[,]?[ ]*", "", zs_extrakt_4[0])
        data['Barrierefreiheit'] = get_accessibility_text (zs_extrakt_1[1], zs_extrakt_2[1], zs_extrakt_3[1], zs_extrakt_4[1])

    data['Angebote'] = str_add_str(angebote_extrakt[0], zs_extrakt_clean)
    data_list.append(data)

scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data_list, table_name="angebote")

