import scraperwiki
import lxml.html           

counter = 1 # Incremented after each successful scraped page. Used to generate case number and url to scrape

#counties = ['Rogers', 'Oklahoma', 'Payne', 'Pushmataha']
counties = ['Tulsa']
years = [2008] # restart at 1991

exists = 0 # Stops the scraper after x non-existant case number/page

for year in years:
    counter = 1
    
    for county in counties:
        exists = 0
        counter = 51# Put number of last page scraped here

        print 'Beginning ' + str(county) + ' ' + str(year)

        while exists <= 15:
            html = scraperwiki.scrape("http://www.oscn.net/applications/oscn/GetCaseInformation.asp?number=cf-" + str(year) + "-" + str(counter) + "&db=" + str(county) + "&submitted=true")
            root = lxml.html.fromstring(html)

            if len(root.cssselect("table")) != 8: # Check if page is a case record page or the 404 page (record pages have 8 tables, errors have 11) The method len() gives the total length of the dictionary. This would be equal to the number of items in the dictionary.
                exists += 1
                print 'Failure: ' + county + ' county record cf-' + str(year) + '-' + str(counter) + ' does not exist (' + str(exists) + ' of 15)'
                counter += 1 #This is the console data

            else:
                exists = 0
                for tr in root.cssselect("center table"):
                    tds = tr.cssselect("td")
                    name = tds[0].text_content().replace("\r","").replace("\t"," ").replace("\n","").replace(u'\xa0','').replace("Plaintiff","Plaintiff [@& ").replace("Defendant","Defendant [@& ") + str(county) + str(year) + "-" + str(counter)
                    judge = tds[1].text_content().replace("\r","").replace("\t"," ").replace("\n","").replace(u'\xa0','').replace("Filed:"," [@& Filed:").replace("Closed:"," [@& Closed:").replace("Judge:"," [@& Judge:")

                parties = []
                for table in root.cssselect("table")[3]:
                    parties.append(table.text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))
    
                attorneys = []
                for tr in root.cssselect("table")[4]:
                    tds = tr.cssselect("td")
                    if len(tds) > 0:
                        attorneys.append(tds[0].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))

                disposition = []
                for tr in root.cssselect("table")[6]: #/html/body/table[6]/tbody/tr[3]/td[3]/font[1]/b
                    f = 0
                    tds = tr.cssselect("tr")
                    if tds[f].text_content().rfind("Disposed:  "):
                        disposition.append(tds[f].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0','').replace("Count #"," [@& " + str(county) + str(year) + "-" + str(counter) + " [@& Count #").replace("Count as Filed:"," [@& Count as Filed:").replace("Date Of Offense:"," [@& Date Of Offense:").replace("Defendant:"," [@& Defendant:").replace("Disposed: "," [@& Disposed: ").replace("Count as Disposed:"," [@& Count as Disposed:").replace("Party Name:","").replace("Disposition Information:",""))
                        f += 1
                    else:
                        f += 1
#                counts = []
#                for tr in root.cssselect("table")[6]: #/html/body/table[6]/tbody/tr[1]/td[2]/font/text()[1]
#                    f = 0
#                    tds = tr.cssselect("td")
#                    if tds[f].text_content().startswith("Count #"):
#                        counts.append(tds[f].text_content().replace("\r"," ").replace("\t","").replace("\n","").replace(u'\xa0',''))
#                        f += 1
#                    else:
#                        f += 1

                data = {        
                       'uniq_case_number' : county + " cf-" + str(year) + "-" + str(counter),
                       'case_number' : "cf-" + str(year) + "-" + str(counter),
                       'name' : name,
                       'judge' : judge,
                       'county' : county,
                       'parties' : parties,
                       'attorneys' : attorneys,
                       'disposition' : disposition, #'counts' : counts,
                       }
        
                print data
                scraperwiki.sqlite.save(unique_keys=['uniq_case_number'], data=data)
                counter += 1