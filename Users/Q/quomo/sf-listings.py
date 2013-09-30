import scraperwiki
import mechanize
import lxml.html


start_url = 'http://www.skaddenfellowships.org/fellows-list/'





myData = []


for z in range(1989, 2014):

    curr_url = start_url + str(z)
    
    
    
    scrape = scraperwiki.scrape(curr_url)

    root = lxml.html.fromstring(scrape)

    for el in root.cssselect("div.wrap"):
    
        for de in el.cssselect("div.summary > h2 > a"):
            name = de.text #name
            
            for ve in el.cssselect("div.summary > div:first-of-type"):
                school = ve.text #firm-summary
        
            for le in el.cssselect("div.summary div.xmall"):
                location = le.text #location-summary
    
            for pe in el.cssselect("div.summary div.italic"):
                org = pe.text #org-summary
    
            for ze in el.cssselect("div.details"):
                if ze.text.strip() != '':
                    proj_deets = ze.text #project details text
                    #print proj_deets
                else:
                    for ue in el.cssselect("div.details>p"):
                        proj_deets = ue.text
                        #print proj_deets


    
            for cre in el.cssselect("div.year"):
                year = cre.text
    
    
                #print name, name_summ, proj_deets, year
    
    
                
                myData.append({
                        "name" : name,
                        "school" : school,
                        "location" : location,
                        "org" : org,
                        "proj-details": proj_deets,
                        "year" : year
                    
                    })  
            
            


scraperwiki.sqlite.save(unique_keys=["proj-details"], data=myData, table_name="sf-peeps")

import scraperwiki
import mechanize
import lxml.html


start_url = 'http://www.skaddenfellowships.org/fellows-list/'





myData = []


for z in range(1989, 2014):

    curr_url = start_url + str(z)
    
    
    
    scrape = scraperwiki.scrape(curr_url)

    root = lxml.html.fromstring(scrape)

    for el in root.cssselect("div.wrap"):
    
        for de in el.cssselect("div.summary > h2 > a"):
            name = de.text #name
            
            for ve in el.cssselect("div.summary > div:first-of-type"):
                school = ve.text #firm-summary
        
            for le in el.cssselect("div.summary div.xmall"):
                location = le.text #location-summary
    
            for pe in el.cssselect("div.summary div.italic"):
                org = pe.text #org-summary
    
            for ze in el.cssselect("div.details"):
                if ze.text.strip() != '':
                    proj_deets = ze.text #project details text
                    #print proj_deets
                else:
                    for ue in el.cssselect("div.details>p"):
                        proj_deets = ue.text
                        #print proj_deets


    
            for cre in el.cssselect("div.year"):
                year = cre.text
    
    
                #print name, name_summ, proj_deets, year
    
    
                
                myData.append({
                        "name" : name,
                        "school" : school,
                        "location" : location,
                        "org" : org,
                        "proj-details": proj_deets,
                        "year" : year
                    
                    })  
            
            


scraperwiki.sqlite.save(unique_keys=["proj-details"], data=myData, table_name="sf-peeps")

import scraperwiki
import mechanize
import lxml.html


start_url = 'http://www.skaddenfellowships.org/fellows-list/'





myData = []


for z in range(1989, 2014):

    curr_url = start_url + str(z)
    
    
    
    scrape = scraperwiki.scrape(curr_url)

    root = lxml.html.fromstring(scrape)

    for el in root.cssselect("div.wrap"):
    
        for de in el.cssselect("div.summary > h2 > a"):
            name = de.text #name
            
            for ve in el.cssselect("div.summary > div:first-of-type"):
                school = ve.text #firm-summary
        
            for le in el.cssselect("div.summary div.xmall"):
                location = le.text #location-summary
    
            for pe in el.cssselect("div.summary div.italic"):
                org = pe.text #org-summary
    
            for ze in el.cssselect("div.details"):
                if ze.text.strip() != '':
                    proj_deets = ze.text #project details text
                    #print proj_deets
                else:
                    for ue in el.cssselect("div.details>p"):
                        proj_deets = ue.text
                        #print proj_deets


    
            for cre in el.cssselect("div.year"):
                year = cre.text
    
    
                #print name, name_summ, proj_deets, year
    
    
                
                myData.append({
                        "name" : name,
                        "school" : school,
                        "location" : location,
                        "org" : org,
                        "proj-details": proj_deets,
                        "year" : year
                    
                    })  
            
            


scraperwiki.sqlite.save(unique_keys=["proj-details"], data=myData, table_name="sf-peeps")

import scraperwiki
import mechanize
import lxml.html


start_url = 'http://www.skaddenfellowships.org/fellows-list/'





myData = []


for z in range(1989, 2014):

    curr_url = start_url + str(z)
    
    
    
    scrape = scraperwiki.scrape(curr_url)

    root = lxml.html.fromstring(scrape)

    for el in root.cssselect("div.wrap"):
    
        for de in el.cssselect("div.summary > h2 > a"):
            name = de.text #name
            
            for ve in el.cssselect("div.summary > div:first-of-type"):
                school = ve.text #firm-summary
        
            for le in el.cssselect("div.summary div.xmall"):
                location = le.text #location-summary
    
            for pe in el.cssselect("div.summary div.italic"):
                org = pe.text #org-summary
    
            for ze in el.cssselect("div.details"):
                if ze.text.strip() != '':
                    proj_deets = ze.text #project details text
                    #print proj_deets
                else:
                    for ue in el.cssselect("div.details>p"):
                        proj_deets = ue.text
                        #print proj_deets


    
            for cre in el.cssselect("div.year"):
                year = cre.text
    
    
                #print name, name_summ, proj_deets, year
    
    
                
                myData.append({
                        "name" : name,
                        "school" : school,
                        "location" : location,
                        "org" : org,
                        "proj-details": proj_deets,
                        "year" : year
                    
                    })  
            
            


scraperwiki.sqlite.save(unique_keys=["proj-details"], data=myData, table_name="sf-peeps")

