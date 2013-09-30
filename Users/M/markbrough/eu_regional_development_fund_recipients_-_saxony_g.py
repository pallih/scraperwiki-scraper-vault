import scraperwiki
import re

#Get the HTML from the Saxony data table
html = scraperwiki.scrape("http://www.statistik.sachsen.de/foerderportal/VZB_20110701_20110630_2007DE051PO004.html")

import lxml.html
root = lxml.html.fromstring(html) 

count = 0
for tr in root.cssselect("tr"):
    #Ignore first two rows - they're headers
    if (count > 1) :
        tds = tr.cssselect("td")
        # Construct the values
        # Remove EUR from the end and change values to a float.
        gesamtbetraege_in_euro= tds[4].text_content()
        gesamtbetraege_in_euro = re.sub(' EUR$', '', gesamtbetraege_in_euro)
        gesamtbetraege_in_euro = re.sub('\.', '', gesamtbetraege_in_euro)
        gesamtbetraege_in_euro = re.sub(',', '.', gesamtbetraege_in_euro)
        gewaehrte_betraege_in_euro= tds[3].text_content()
        gewaehrte_betraege_in_euro = re.sub(' EUR$', '', gewaehrte_betraege_in_euro)
        gewaehrte_betraege_in_euro = re.sub('\.', '', gewaehrte_betraege_in_euro)
        gewaehrte_betraege_in_euro = re.sub(',', '.', gewaehrte_betraege_in_euro)

        data = {
            'rowid' : (count-2),
            'beguenstigten' : tds[0].text_content(),
            'bezeichnung_des_vorhabens' : tds[1].text_content(),
            'jahr_der_bewilligung' : tds[2].text_content(),
            'gewaehrte_betraege_in_euro' : gewaehrte_betraege_in_euro,
            'gesamtbetraege_in_euro' : gesamtbetraege_in_euro
        } 
        scraperwiki.sqlite.save(unique_keys=['rowid'], data=data)
    count = (count + 1)
    print count
import scraperwiki
import re

#Get the HTML from the Saxony data table
html = scraperwiki.scrape("http://www.statistik.sachsen.de/foerderportal/VZB_20110701_20110630_2007DE051PO004.html")

import lxml.html
root = lxml.html.fromstring(html) 

count = 0
for tr in root.cssselect("tr"):
    #Ignore first two rows - they're headers
    if (count > 1) :
        tds = tr.cssselect("td")
        # Construct the values
        # Remove EUR from the end and change values to a float.
        gesamtbetraege_in_euro= tds[4].text_content()
        gesamtbetraege_in_euro = re.sub(' EUR$', '', gesamtbetraege_in_euro)
        gesamtbetraege_in_euro = re.sub('\.', '', gesamtbetraege_in_euro)
        gesamtbetraege_in_euro = re.sub(',', '.', gesamtbetraege_in_euro)
        gewaehrte_betraege_in_euro= tds[3].text_content()
        gewaehrte_betraege_in_euro = re.sub(' EUR$', '', gewaehrte_betraege_in_euro)
        gewaehrte_betraege_in_euro = re.sub('\.', '', gewaehrte_betraege_in_euro)
        gewaehrte_betraege_in_euro = re.sub(',', '.', gewaehrte_betraege_in_euro)

        data = {
            'rowid' : (count-2),
            'beguenstigten' : tds[0].text_content(),
            'bezeichnung_des_vorhabens' : tds[1].text_content(),
            'jahr_der_bewilligung' : tds[2].text_content(),
            'gewaehrte_betraege_in_euro' : gewaehrte_betraege_in_euro,
            'gesamtbetraege_in_euro' : gesamtbetraege_in_euro
        } 
        scraperwiki.sqlite.save(unique_keys=['rowid'], data=data)
    count = (count + 1)
    print count
