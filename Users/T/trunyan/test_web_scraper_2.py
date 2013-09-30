import scraperwiki
import lxml.html
import string

urlToScrape = "http://tracking.ironmanlive.com/newathlete.php?rid=1143239978&race=arizona&bib=%s&v=3.0&beta=&1363727700"

def databaseSetup():
    scraperwiki.sqlite.execute("drop table if exists RESULTS")
    scraperwiki.sqlite.execute("drop table if exists NO_DATA_FOUND")
    scraperwiki.sqlite.commit()

    scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS "RESULTS" (AthleteName, Bib INT,Division INT, Age INT,State,Country,Profession,DivisionRank INT,OverallRank  INT,TotalSwim,TotalBike,TotalRun,TotalTime)""")
    scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS "NO_DATA_FOUND" (Bib INT,Year INT, Event)""")
    scraperwiki.sqlite.commit()

def parsePage(html):
    
    # Dictionary to store info
    athInfo = {}
    
    #Now start populating our data object
    athInfo['AthleteName'] = html.cssselect("h2")[0].text
    athInfo['DivisionRank'] = html.cssselect("#rank *")[0].tail.strip()
    athInfo['OverallRank'] = html.cssselect("#div-rank *")[0].tail.strip()    

    infoFields = ['Bib', 'Division', 'Age', 'State', 'Country', 'Profession']
    detailsFields = ['TotalSwim', 'TotalBike', 'TotalRun', 'TotalTime']
    
    rows = html.cssselect("table#general-info tr")
    for i, stat in enumerate(infoFields):
        athInfo[stat] = rows[i][1].text
    
    rows = html.cssselect("table#athelete-details tr")
    for i, stat in enumerate(detailsFields):
        athInfo[stat] = rows[i][1].text

    scraperwiki.sqlite.save(unique_keys=['Bib'], data=athInfo, table_name="RESULTS")

#Setup the database
databaseSetup()



#This is the main loop that controls which URL to scrape
bibId = 1
while bibId < 500 :
    bibId += 1
    #call scrape and send to parseHTML 
    pageToScrape = scraperwiki.scrape(urlToScrape % bibId)
    html = lxml.html.fromstring(pageToScrape)  
    try:
        parsePage(html)
    except IndexError:
        scraperwiki.sqlite.save(unique_keys=['Bib'], data={'Bib':bibId,'Year':2013,'Event':"test"}, table_name="NO_DATA_FOUND")
        #scraperwiki.sqlite.commit()
        print "problem with bibID %d " % bibId
    
import scraperwiki
import lxml.html
import string

urlToScrape = "http://tracking.ironmanlive.com/newathlete.php?rid=1143239978&race=arizona&bib=%s&v=3.0&beta=&1363727700"

def databaseSetup():
    scraperwiki.sqlite.execute("drop table if exists RESULTS")
    scraperwiki.sqlite.execute("drop table if exists NO_DATA_FOUND")
    scraperwiki.sqlite.commit()

    scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS "RESULTS" (AthleteName, Bib INT,Division INT, Age INT,State,Country,Profession,DivisionRank INT,OverallRank  INT,TotalSwim,TotalBike,TotalRun,TotalTime)""")
    scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS "NO_DATA_FOUND" (Bib INT,Year INT, Event)""")
    scraperwiki.sqlite.commit()

def parsePage(html):
    
    # Dictionary to store info
    athInfo = {}
    
    #Now start populating our data object
    athInfo['AthleteName'] = html.cssselect("h2")[0].text
    athInfo['DivisionRank'] = html.cssselect("#rank *")[0].tail.strip()
    athInfo['OverallRank'] = html.cssselect("#div-rank *")[0].tail.strip()    

    infoFields = ['Bib', 'Division', 'Age', 'State', 'Country', 'Profession']
    detailsFields = ['TotalSwim', 'TotalBike', 'TotalRun', 'TotalTime']
    
    rows = html.cssselect("table#general-info tr")
    for i, stat in enumerate(infoFields):
        athInfo[stat] = rows[i][1].text
    
    rows = html.cssselect("table#athelete-details tr")
    for i, stat in enumerate(detailsFields):
        athInfo[stat] = rows[i][1].text

    scraperwiki.sqlite.save(unique_keys=['Bib'], data=athInfo, table_name="RESULTS")

#Setup the database
databaseSetup()



#This is the main loop that controls which URL to scrape
bibId = 1
while bibId < 500 :
    bibId += 1
    #call scrape and send to parseHTML 
    pageToScrape = scraperwiki.scrape(urlToScrape % bibId)
    html = lxml.html.fromstring(pageToScrape)  
    try:
        parsePage(html)
    except IndexError:
        scraperwiki.sqlite.save(unique_keys=['Bib'], data={'Bib':bibId,'Year':2013,'Event':"test"}, table_name="NO_DATA_FOUND")
        #scraperwiki.sqlite.commit()
        print "problem with bibID %d " % bibId
    
