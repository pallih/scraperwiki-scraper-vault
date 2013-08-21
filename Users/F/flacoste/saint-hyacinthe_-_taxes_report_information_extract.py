# -*- coding: utf-8 -*-
## author: Francis Lacoste
## date: 22 january 2013
## scrap taxes report information from Saint-Hyacinthe city website

import scraperwiki     
import lxml.html        
import urllib, urllib2

scraperwiki.sqlite.attach("saint-hyacinthe_street_name")
urllist = scraperwiki.sqlite.select("* from [saint-hyacinthe_street_name].swdata")

for row in urllist:
    print row
    url = row['taxreport'].encode('utf8')
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    ## select the form
    for form in root.cssselect("form"):
        tables = form.cssselect("table")
        data = {
            'url' : url,
            'matricule' : '',
            'annee' : '',
            'typebatiment' : '',
            'condo' : '',
            'nbrelogement' : '',
            'superficie' : '',
            'profondeur' : '',
            'front' : '',
            'zoneagricole' : '',
            'dateentre' : '', ## autre table
            'valeurterrain' : '', ## autre table
            'valeurbatiment' : '', ## autre table
            'valeurimmeuble' : '' ## autre table
        }
        for table in tables:
            tds = table.cssselect("td")
            if len(tds) == 47:
                data['matricule'] = tds[4].text_content().strip()
                data['annee'] = tds[6].text_content().strip()
                data['typebatiment'] = tds[8].text_content().strip()
                data['condo'] = tds[10].text_content().strip()
                data['nbrelogement'] = tds[12].text_content().strip()
                data['superficie'] = tds[36].text_content().strip()
                data['profondeur'] = tds[38].text_content().strip()
                data['front'] = tds[40].text_content().strip()
                data['zoneagricole'] = tds[44].text_content().strip()

            if len(tds) == 48:
                data['matricule'] = tds[4].text_content().strip()
                data['annee'] = tds[6].text_content().strip()
                data['typebatiment'] = tds[8].text_content().strip()
                data['condo'] = tds[10].text_content().strip()
                data['nbrelogement'] = tds[12].text_content().strip()
                data['superficie'] = tds[37].text_content().strip()
                data['profondeur'] = tds[39].text_content().strip()
                data['front'] = tds[41].text_content().strip()
                data['zoneagricole'] = tds[45].text_content().strip()

            if len(tds) == 9:
                txt = tds[1].text_content()
                if txt == "Valeur du terrain":
                    data['valeurterrain'] = tds[6].text_content().strip()
                    data['valeurbatiment'] = tds[7].text_content().strip() 
                    data['valeurimmeuble'] = tds[8].text_content().strip() 
    
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)