import scraperwiki
import lxml.html

def scrape_from_root(urlToScrape, dId):
    print "Scraping from: " + urlToScrape + "."
    print "Starting with " + str(dId) + " entries."
    html = scraperwiki.scrape(urlToScrape)
    root = lxml.html.fromstring(html)
    #create an id to be used as unique ID for our Data

    for div in root.cssselect("div .itemtitle"):
        #print lxml.etree.tostring(div)
        for theLink in div.cssselect("a"):
            #print lxml.etree.tostring(theLink)
            #help(theLink)
    
    
            #print dId
            #create a clean data record (hopefully)
            record = {}
    
            SessionTitle = theLink.text_content()
            record['SessionTitle'] = SessionTitle
            #print SessionTitle
            Url = "http://aaas.confex.com/aaas/2013/webprogram/" + theLink.attrib.get('href')
            record['Url'] = Url
            #print Url
    
            subhtml = scraperwiki.scrape(Url)
            subroot = lxml.html.fromstring(subhtml)
            
            for datPoint in subroot.cssselect("div .datetime"):
                DateTime = datPoint.text_content() # session datetime
                record['DateTime'] = DateTime
                #print DateTime
    
            for datPoint in subroot.cssselect("div .location"):
                Location = datPoint.text_content() # session location
                record['Location'] = Location
                #print Location
        
            for organizers in subroot.cssselect("div .persongroup"): 
                for datPoint in organizers.cssselect("div .group"):
                    Position = datPoint.text_content()
                    Position = Position.strip(":")
                    record['Position'] = Position
                    #print Position
                
                for datPoint in organizers.cssselect("div .people"):
                    Name = datPoint.text_content()
                    Name = Name.strip()
                    
                    if Name.find("\n\t\t\t\t\t\t and") == -1:
                        NameSplit = Name.split(',', 1)
                        Name = NameSplit[0]
                        #print NameSplit
                        affiliation = NameSplit[1].strip()
                        record['Name'] = Name
                        record['Affiliation'] = affiliation
                    else:
                        # if it is "Name, Affiliation \n and Name, Affiliation"
                        NameSpliter = Name.split('\n\t\t\t\t\t\t and', 1)
                        #print NameSpliter
                        NameSplit = NameSpliter[1].split(',', 1)
                        Name = NameSplit[0].strip()
                        affiliation = NameSplit[1].strip()
                        record['Name'] = Name
                        record['Affiliation'] = affiliation
    
                        #save record
                        dId = dId+1
                        record['ID'] = dId
                        #print record
                        #subroot.cssselect("div .persongroup").text_content() #throw an error to have a breakpoint
                        scraperwiki.sqlite.save(["ID"], record)
                        
                        #print NameSpliter[0] 
                        #print NameSpliter[0].find("\n\t\t\t\t\t\t ,")
                        #print NameSpliter[0].find("\n\t\t\t\t\t\t,")

                        if NameSpliter[0].find("\n\t\t\t\t\t\t,") != -1:
                            NameSpliter = NameSpliter[0].split('\n\t\t\t\t\t\t,')
                            for NameEntries in NameSpliter:
                                NameSplit = NameEntries.split(',', 1)
                                Name = NameSplit[0].strip()
                                affiliation = NameSplit[1].strip()
                                record['Name'] = Name
                                record['Affiliation'] = affiliation
            
                                #save record
                                dId = dId+1
                                record['ID'] = dId
                                #print record
                                #subroot.cssselect("div .persongroup").text_content() #throw an error to have a breakpoint
                                scraperwiki.sqlite.save(["ID"], record)
                        else:
                            NameSplit = NameSpliter[0].split(',', 1)
                            Name = NameSplit[0].strip()
                            affiliation = NameSplit[1].strip()
                            record['Name'] = Name
                            record['Affiliation'] = affiliation
                        
                    #print Name
                
                if Position == "Speakers":
                    #doStuff
                    for papers in subroot.cssselect("div .paper"):
                        for paperLink in papers.cssselect("a"):
                            paperUrl = "http://aaas.confex.com/aaas/2013/webprogram/" + paperLink.attrib.get('href')
                            record['PaperUrl'] = paperUrl
                        for datPoint in papers.cssselect("span .name"):
                            Name = datPoint.text_content()
                            record['Name'] = Name
                        for datPoint in papers.cssselect("span .affiliation"):
                            affiliation = datPoint.text_content()
                            record['Affiliation'] = affiliation
                        #save record
                        dId = dId+1
                        record['ID'] = dId           
                        #print dId
                        #print record
                        #subroot.cssselect("div .persongroup").text_content() #throw an error to have a breakpoint
                        #save scrapped data record
                        scraperwiki.sqlite.save(["ID"], record)
                        #clear record:
                        paperUrl = ""
                        record['PaperUrl'] = paperUrl
                        Name = ""
                        record['Name'] = Name
                        affiliation = ""
                        record['Affiliation'] = affiliation
                        Position = ""
                        record['Position'] = Position
                else:
                    #save record
                    dId = dId+1
                    record['ID'] = dId
                    #print dId
                    #print record
                    #subroot.cssselect("div .persongroup").text_content() #throw an error to have a breakpoint
                    #save scrapped data record
                    scraperwiki.sqlite.save(["ID"], record)
                    #clear record:
                    paperUrl = ""
                    record['PaperUrl'] = paperUrl
                    Name = ""
                    record['Name'] = Name
                    affiliation = ""
                    record['Affiliation'] = affiliation
                    Position = ""
                    record['Position'] = Position
    print "Now at " + str(dId) + " entries."
    return dId

def preScrape(page, dataId):
    url = "http://aaas.confex.com/aaas/2013/webprogram/start.html#srch=words%7C*%7Cmethod%7Cand%7Cpge%7C" + str(page)
    print url
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    print root
    for div in root.cssselect("div .resulttitle"):
        scrapeurl = "http://aaas.confex.com/aaas/2013/webprogram/" + div.attrib.get('href')
        print scrapeurl
        dataId = scrape_from_root(scrapeurl, dataId)

    return dataId
    
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
dataId = 0
i=1

while(i<=116):
    dataId = preScrape(i, dataId)
    i = i+1

