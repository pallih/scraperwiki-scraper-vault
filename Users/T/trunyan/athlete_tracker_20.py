import scraperwiki
import lxml.html
import datetime

#urlToScrape = "http://tracking.ironmanlive.com/newathlete.php?rid=1143239978&race=arizona&bib=%s&v=3.0&beta=&1363727700"
urlToScrape = "http://tracking.ironmanlive.com/newathlete.php?rid=1143239972&race=loscabos&bib=%s&v=3.0&beta=&1364297400"

#Global flag indicating we are scraping for first time
isReset = True
maxBibID = 1500

def databaseSetup():
        print "Resetting database and prepopulating Bibs"
        scraperwiki.sqlite.execute("drop table if exists RESULTS")
        scraperwiki.sqlite.commit()
    
        scraperwiki.sqlite.execute("""CREATE TABLE IF NOT EXISTS "RESULTS" (Bib INT,Scraped,HasResults INT,AthleteName, Division INT, Age INT,State,Country,Profession,DivisionRank INT,OverallRank  INT,TotalSwim,TotalBike,TotalRun,TotalTime,T1,T2)""")
        scraperwiki.sqlite.commit()

        #prepopulate table with bibId's to scrape
        bibIDs = [ {"Bib":x}  for x in range(1,maxBibID +1) ]           
        scraperwiki.sqlite.save(unique_keys=['Bib'], data=bibIDs, table_name="RESULTS")

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

    #have to use xpath to get T1 and T2 data
    athInfo['T1'] = html.xpath("//tr[contains(td/text(), 'T1:')]/td[2]")[0].text_content()
    athInfo['T2'] = html.xpath("//tr[contains(td/text(), 'T2:')]/td[2]")[0].text_content()

    athInfo['HasResults'] = 1
    athInfo['Scraped'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scraperwiki.sqlite.save(unique_keys=['Bib'], data=athInfo, table_name="RESULTS", verbose=0)

#Setup the database
if isReset:
    databaseSetup()

#fetch out bibs to process
athletesToScrape = scraperwiki.sqlite.select('* from "RESULTS" where Scraped is null')
print "About to process %s bibs" % len(athletesToScrape);


#This is the main loop that controls which URL to scrape
for athlete in athletesToScrape:
    #call scrape and send to parseHTML 
    pageToScrape = scraperwiki.scrape(urlToScrape % athlete['Bib'])
    html = lxml.html.fromstring(pageToScrape)  
    try:
        parsePage(html)
    except IndexError:
        scraperwiki.sqlite.save(unique_keys=['Bib'], data={'Bib':athlete['Bib'],'HasResults':0,'Scraped':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, table_name="RESULTS", verbose=0)
        scraperwiki.sqlite.commit()

    
