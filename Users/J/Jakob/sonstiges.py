import scraperwiki
import lxml.html
import re

scraperwiki.sqlite.attach("schulen-berlin-de-source", "source")
all = scraperwiki.sqlite.select("* FROM source.schule")
for school in all:
    print school['SchulName']
    data = {'IDSchulzweig' : school['IDSchulzweig'], 'SchulName' : school['SchulName']}
    html = school['schulportrait']
    page = lxml.html.fromstring(html)

    dif = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblDiff")
    if len(dif):
         data['Differenzierung'] = dif[0].text_content()
    ang = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAngebote")
    if len(ang):
        data['Angebote'] = ang[0].text_content()
    zus = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblZusatz")
    if len(zus):
         data['Zusatz'] = zus[0].text_content()
    aus = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAusstattung")
    if len(aus):
        data['Ausstattung'] = aus[0].text_content()
    bem = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblBemerkungenSchulzweig")
    if len(bem):
        data['Bemerkung'] = bem[0].text_content()

    ags = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblAGs")
    if len(ags):
        data['AGs'] = ags[0].text_content()
    par = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblPartner")
    if len(par):
        data['Partner'] = par[0].text_content()

    mit = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblMittag")
    if len(mit):
        data['Mittag'] = mit[0].text_content()
    dua = page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblDualesLernen")
    if len(dua):
        data['DualesLernen'] = dua[0].text_content()
    gan= page.cssselect("span#ctl00_ContentPlaceHolderMenuListe_lblGanztags")
    if len(gan):
        data['Ganztags'] = gan[0].text_content()

    scraperwiki.sqlite.save(unique_keys=['IDSchulzweig'], data=data, table_name="sonstiges")
    
