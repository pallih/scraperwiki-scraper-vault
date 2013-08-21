import scraperwiki
import lxml.html           

counter = 1 # Incremented after each successful scraped page. Used to generate case number and url to scrape
exists = True # Stops the scraper after first non-existant case number/page

while exists == True:
    html = scraperwiki.scrape("http://www.oscn.net/applications/oscn/getcaseinformation.asp?query=true&srch=0&web=true&db=Tulsa&number=cm-2013-" + str(counter) + "&iLAST=&iFIRST=&iMIDDLE=&iID=&iDOBL=&iDOBH=&SearchType=0&iDCPT=&iapcasetype=All&idccasetype=All&iDATEL=&iDATEH=&iCLOSEDL=&iCLOSEDH=&iDCType=0&iYear=&iNumber=&icitation=&submitted=true")
    root = lxml.html.fromstring(html)

    if len(root.cssselect("table")) != 8: # Check if page is a case record page or the 404 page (record pages have 8 tables, errors have 11)
        exists = False

    else:
        for tr in root.cssselect("center table"):
            tds = tr.cssselect("td")
            name = tds[0].text_content().replace("\r","").replace("\t","").replace("\n","").replace(u'\xa0','')
            judge = tds[1].text_content().replace("\r","").replace("\t","").replace("\n","").replace(u'\xa0','')

        parties = []
        for table in root.cssselect("table")[3]:
            parties.append(table.text_content().replace("\r","").replace("\t","").replace("\n","").replace(u'\xa0',''))
    
        attornies = []
        for tr in root.cssselect("table")[4]:
            tds = tr.cssselect("td")
            if len(tds) > 0:
                attornies.append(tds[0].text_content().replace("\r","").replace("\t","").replace("\n","").replace(u'\xa0',''))

        counts = []
        for tr in root.cssselect("table")[6]:
            d = 0
            tds = tr.cssselect("tr")
            if tds[d].text_content().startswith("Count #"): 
                counts.append(tds[d].text_content().replace("\r","").replace("\t","").replace("\n","").replace(u'\xa0',''))
                d += 1
            else:
                d += 1



        data = {        
               'case_number' : "cm-2013-" + str(counter),
               'name' : name,
               'judge' : judge,
               'county' : "Tulsa",
               'parties' : parties,
               'attornies' : attornies,
               'counts' : counts,
               }
        
        scraperwiki.sqlite.save(unique_keys=['case_number'], data=data)
        counter += 1