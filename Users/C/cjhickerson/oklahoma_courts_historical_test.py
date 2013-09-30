import scraperwiki
import lxml.html           

counter = 1 # Incremented after each successful scraped page. Used to generate case number and url to scrape

#counties = ['Rogers', 'Oklahoma', 'Payne', 'Pushmataha']
counties = ['Tulsa']
years = [2004] # restart at 1991

exists = 0 # Stops the scraper after x non-existant case number/page

for year in years:
    counter = 1
    
    for county in counties:
        exists = 0
        counter = 2284 # Put number of last page scraped here

        print 'Beginning ' + str(county) + ' ' + str(year)

        while exists <= 10:
            html = scraperwiki.scrape("http://www.oscn.net/applications/oscn/GetCaseInformation.asp?number=cf-" + str(year) + "-" + str(counter) + "&db=" + str(county) + "&submitted=true")
            root = lxml.html.fromstring(html)

            if len(root.cssselect("table")) != 8: # Check if page is a case record page or the 404 page (record pages have 8 tables, errors have 11)
                exists += 1
                print 'Failure: ' + county + ' county record cf-' + str(year) + '-' + str(counter) + ' does not exist (' + str(exists) + ' of 10)'
                counter += 1

            else:
                exists = 0
                for tr in root.cssselect("center table"):
                    tds = tr.cssselect("td")
                    name = tds[0].text_content().replace("\r","").replace("\t"," ").replace("\n","").replace(u'\xa0','')
                    judge = tds[1].text_content().replace("\r","").replace("\t"," ").replace("\n","").replace(u'\xa0','')

                parties = []
                for table in root.cssselect("table")[3]:
                    parties.append(table.text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))
    
                attornies = []
                for tr in root.cssselect("table")[4]:
                    tds = tr.cssselect("td")
                    if len(tds) > 0:
                        attornies.append(tds[0].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))

                counts = []
                for tr in root.cssselect("table")[6]:
                    d = 0
                    tds = tr.cssselect("tr")
                    if tds[d].text_content().startswith("Count #"): 
                        counts.append(tds[d].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))
                        d += 1
                    else:
                        d += 1

                data = {        
                       'uniq_case_number' : county + " cf-" + str(year) + "-" + str(counter),
                       'case_number' : "cf-" + str(year) + "-" + str(counter),
                       'name' : name,
                       'judge' : judge,
                       'county' : county,
                       'parties' : parties,
                       'attornies' : attornies,
                       'counts' : counts,
                       }
        
                print data
                scraperwiki.sqlite.save(unique_keys=['uniq_case_number'], data=data)
                counter += 1import scraperwiki
import lxml.html           

counter = 1 # Incremented after each successful scraped page. Used to generate case number and url to scrape

#counties = ['Rogers', 'Oklahoma', 'Payne', 'Pushmataha']
counties = ['Tulsa']
years = [2004] # restart at 1991

exists = 0 # Stops the scraper after x non-existant case number/page

for year in years:
    counter = 1
    
    for county in counties:
        exists = 0
        counter = 2284 # Put number of last page scraped here

        print 'Beginning ' + str(county) + ' ' + str(year)

        while exists <= 10:
            html = scraperwiki.scrape("http://www.oscn.net/applications/oscn/GetCaseInformation.asp?number=cf-" + str(year) + "-" + str(counter) + "&db=" + str(county) + "&submitted=true")
            root = lxml.html.fromstring(html)

            if len(root.cssselect("table")) != 8: # Check if page is a case record page or the 404 page (record pages have 8 tables, errors have 11)
                exists += 1
                print 'Failure: ' + county + ' county record cf-' + str(year) + '-' + str(counter) + ' does not exist (' + str(exists) + ' of 10)'
                counter += 1

            else:
                exists = 0
                for tr in root.cssselect("center table"):
                    tds = tr.cssselect("td")
                    name = tds[0].text_content().replace("\r","").replace("\t"," ").replace("\n","").replace(u'\xa0','')
                    judge = tds[1].text_content().replace("\r","").replace("\t"," ").replace("\n","").replace(u'\xa0','')

                parties = []
                for table in root.cssselect("table")[3]:
                    parties.append(table.text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))
    
                attornies = []
                for tr in root.cssselect("table")[4]:
                    tds = tr.cssselect("td")
                    if len(tds) > 0:
                        attornies.append(tds[0].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))

                counts = []
                for tr in root.cssselect("table")[6]:
                    d = 0
                    tds = tr.cssselect("tr")
                    if tds[d].text_content().startswith("Count #"): 
                        counts.append(tds[d].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))
                        d += 1
                    else:
                        d += 1

                data = {        
                       'uniq_case_number' : county + " cf-" + str(year) + "-" + str(counter),
                       'case_number' : "cf-" + str(year) + "-" + str(counter),
                       'name' : name,
                       'judge' : judge,
                       'county' : county,
                       'parties' : parties,
                       'attornies' : attornies,
                       'counts' : counts,
                       }
        
                print data
                scraperwiki.sqlite.save(unique_keys=['uniq_case_number'], data=data)
                counter += 1