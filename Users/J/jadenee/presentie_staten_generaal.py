import scraperwiki

import lxml.html


totaalPaginas = 1 # we beginnen met 1 pagina te scrapen
huidigePagina = 1


while huidigePagina <= totaalPaginas:

    formatted_tekst = ''
    
    base_url = "https://zoek.officielebekendmakingen.nl"
    
    # presentie vergaderingen 1e en 2e kamer, afgelopen jaar
    # url = base_url + "/zoeken/resultaat?zkt=Uitgebreid&pst=ParlementaireDocumenten&vrt=presentie&zkd=AlleenInDeTitel&dpr=AnderePeriode&spd=20120619&epd=20130619&kmr=&sdt=KenmerkendeDatum&isp=true&pnr=13&rpp=10&_page=" + str(huidigePagina) + "&sorttype=1&sortorder=4"
    
    # presentie vergaderingen 1e Kamer,
    url = base_url + "/zoeken/resultaat/?zkt=Uitgebreid&pst=ParlementaireDocumenten&vrt=presentie&zkd=AlleenInDeTitel&dpr=AnderePeriode&spd=20110607&epd=20130619&kmr=EersteKamerderStatenGeneraal|VerenigdeVergaderingderStatenGeneraal&sdt=KenmerkendeDatum&par=Handeling&dst=Onopgemaakt|Opgemaakt|Opgemaakt+na+onopgemaakt&isp=true&pnr=1&rpp=10&_page=" + str(huidigePagina) + "&sorttype=1&sortorder=4"
        
    print "Ophalen pagina " + str(huidigePagina) + " ..."
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    # als we de eerste pagina bekijken, sla dan het totaal aantal resultaten-pagina's op
    if (huidigePagina == 1):
        totaalPaginas = root.cssselect("p.marge-onder strong")[0]
        print totaalPaginas.text
    
    # alle resultaten op de pagina langslopen en de bijbehorende xml ophalen
    for el in root.cssselect("div.lijst a.hyperlink"):
        
        result_url = el.attrib['href']
        xml_url = base_url + result_url.split(".html?")[0] + ".xml"
        xml = scraperwiki.scrape(xml_url)
        
        root = lxml.html.fromstring(xml)
        
        # eerst de metadata bij deze vergadering opslaan.
        for meta in root.cssselect("meta"):

            if (meta.attrib['name'] == 'DC.identifier'):
        
                vrg_vergadering = meta.attrib['content']
        
            elif (meta.attrib['name'] == 'DC.creator'):
        
                vrg_kamer = meta.attrib['content']
        
            elif (meta.attrib['name'] == 'OVERHEIDop.datumVergadering'):
        
                vrg_datum = meta.attrib['content']
        
            elif (meta.attrib['name'] == 'OVERHEIDop.vergaderjaar'):
        
                vrg_vergaderjaar = meta.attrib['content']
        
            elif (meta.attrib['name'] == 'OVERHEIDop.publicationIssue'):
        
                vrg_volgnummer = meta.attrib['content']


        # nog even de aanvangstijd opslaan: <vergadertijd>Aanvang 13.30 uur</vergadertijd>
        if (len(root.cssselect("vergadertijd")) > 0):
            aanvang = root.cssselect("vergadertijd")[0]
            vrg_aanvang = aanvang.text
        else:
            vrg_aanvang = ''
        
            
        # de aanwezigen opslaan
        i = 0
        formatted_tekst = ''
        alineas = root.cssselect("opening tekst al")
        
        # voor de voorzitter moeten we even iets meer moeite doen
        if (i==0):
            #voorzitter = root.cssselect("opening tekst al nadruk")[0]
            #voorzitter = voorzitter.text
    
            if (len(root.cssselect("opening tekst al nadruk")) > 0):
                voorzitter = root.cssselect("opening tekst al nadruk")[0]
                voorzitter = voorzitter.text
            else:
                voorzitter = ''
            

        if (len(alineas) >= 1):
            vrg_aanwezigen0 = alineas[0].text
        else:
            vrg_aanwezigen0 = ''
        
        if (len(alineas) >= 2):
            vrg_aanwezigen1 = alineas[1].text
        else:
            vrg_aanwezigen1 = ''
        
        if (len(alineas) >= 3):
            vrg_aanwezigen2 = alineas[2].text
        else:
            vrg_aanwezigen2 = ''
        
        if (len(alineas) >= 4):
            vrg_aanwezigen3 = alineas[3].text
        else:
            vrg_aanwezigen3 = ''
        
        if (len(alineas) >= 5):
            vrg_aanwezigen4 = alineas[4].text
        else:
            vrg_aanwezigen4 = ''

        # formatted_tekst = formatted_tekst + lxml.html.tostring(alineas)
        
        # print "XML: " + formatted_tekst
        
        print "Vergadering " + vrg_volgnummer + " " + vrg_vergaderjaar + " ..."
        
        # data opslaan in sqlite-database
        scraperwiki.sqlite.save(unique_keys=["vergadering"], data={"vergadering": vrg_vergadering, "kamer": vrg_kamer, "datum": vrg_datum, "vergaderjaar": vrg_vergaderjaar, "volgnummer": vrg_volgnummer, "voorzitter": voorzitter, "aanwezigen0": vrg_aanwezigen0, "aanwezigen1": vrg_aanwezigen1, "aanwezigen2": vrg_aanwezigen2, "aanwezigen3": vrg_aanwezigen3, "aanwezigen4": vrg_aanwezigen4})
        
        # output the data CSV-style
        '''
        print "vergadering|kamer|datum|vergaderjaar|volgnummer|voorzitter|aanwezigen0|aanwezigen1|aanwezigen2|aanwezigen3|aanwezigen4"
        
        print vrg_vergadering
        print "|"
        print vrg_kamer
        print "|"
        print vrg_datum
        print "|"
        print vrg_vergaderjaar
        print "|"
        print vrg_volgnummer
        print "|"
        print voorzitter
        print "|"
        print vrg_aanwezigen0
        print "|"
        print vrg_aanwezigen1
        print "|"
        print vrg_aanwezigen2
        print "|"
        print vrg_aanwezigen3
        print "|"
        print vrg_aanwezigen4
        print "NEWLINE"
        '''
        
        print "...opgeslagen."


    huidigePagina += 1

    # exit() # dit is voor tijdens het testen


exit()


