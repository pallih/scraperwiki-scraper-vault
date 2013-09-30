# forked from https://scraperwiki.com/scrapers/test_web_scraper_2/
# during discussion on the mailing list: https://groups.google.com/forum/#!topic/scraperwiki/xz2ftanNb7o

import scraperwiki
import lxml.html
import string

urlToScrape = "http://tracking.ironmanlive.com/newathlete.php?rid=1143239978&race=arizona&bib=%s&v=3.0&beta=&1363727700"
#pageToScrape = scraperwiki.scrape("urlToScrape")
#html = lxml.html.fromstring(pageToScrape)

samplehtml = """<html><body>
<div>
    <div>
    <h2>Craig WIDNESS</h2>
    </div>
    <div id="ranks" class="right">
        <div id="rank"><strong>Rank:</strong> 3</div>
        <div id="div-rank"><strong>Overall Rank:</strong> 38</div>
    </div>
</div>
<table width="350" id="general-info" class="left" border="0" style="margin-right: 10px !important;">
<tbody><tr>
        <td><strong>BIB:</strong></td>
    <td>2078</td>
</tr><tr>
    <td><strong>Division:</strong></td>
    <td>M40-44</td>
</tr><tr>
    <td><strong>Age:</strong></td>
    <td>42</td>
</tr><tr>
    <td><strong>State:</strong></td>
    <td>Manchester NH</td>
</tr><tr>
    <td><strong>Country:</strong></td>
    <td>USA</td>
</tr><tr>
    <td><strong>Profession:</strong></td>
    <td>Physician</td>
</tr>
</tbody></table>
<table width="175" id="athelete-details" class="right" border="0">
<tbody><tr>
    <td><strong>Swim:</strong></td>
    <td>56:38</td>
</tr><tr>
    <td><strong>Bike:</strong></td>
    <td>4:50:37</td>
</tr><tr>
    <td><strong>Run:</strong></td>
    <td>3:17:24</td>
</tr><tr>
    <td><strong>Overall:</strong></td>
    <td>9:12:33</td>
</tr>
</tbody></table>

</body>
</html>
"""
html = lxml.html.fromstring(samplehtml)

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
bibId = 1000
while bibId < 1100 :
    bibId += 1
    #call scrape and send to parseHTML 
    pageToScrape = scraperwiki.scrape(urlToScrape % bibId)
    html = lxml.html.fromstring(pageToScrape)  
    try:
        parsePage(html)
    except IndexError:
        #scraperwiki.sqlite.save(unique_keys=['bibId'], data={"BIB":bibId,"YEAR":2013,"EVENT":"test"}, table_name="NO_DATA_FOUND")
        print "problem with bibID %d " % bibId
    
# forked from https://scraperwiki.com/scrapers/test_web_scraper_2/
# during discussion on the mailing list: https://groups.google.com/forum/#!topic/scraperwiki/xz2ftanNb7o

import scraperwiki
import lxml.html
import string

urlToScrape = "http://tracking.ironmanlive.com/newathlete.php?rid=1143239978&race=arizona&bib=%s&v=3.0&beta=&1363727700"
#pageToScrape = scraperwiki.scrape("urlToScrape")
#html = lxml.html.fromstring(pageToScrape)

samplehtml = """<html><body>
<div>
    <div>
    <h2>Craig WIDNESS</h2>
    </div>
    <div id="ranks" class="right">
        <div id="rank"><strong>Rank:</strong> 3</div>
        <div id="div-rank"><strong>Overall Rank:</strong> 38</div>
    </div>
</div>
<table width="350" id="general-info" class="left" border="0" style="margin-right: 10px !important;">
<tbody><tr>
        <td><strong>BIB:</strong></td>
    <td>2078</td>
</tr><tr>
    <td><strong>Division:</strong></td>
    <td>M40-44</td>
</tr><tr>
    <td><strong>Age:</strong></td>
    <td>42</td>
</tr><tr>
    <td><strong>State:</strong></td>
    <td>Manchester NH</td>
</tr><tr>
    <td><strong>Country:</strong></td>
    <td>USA</td>
</tr><tr>
    <td><strong>Profession:</strong></td>
    <td>Physician</td>
</tr>
</tbody></table>
<table width="175" id="athelete-details" class="right" border="0">
<tbody><tr>
    <td><strong>Swim:</strong></td>
    <td>56:38</td>
</tr><tr>
    <td><strong>Bike:</strong></td>
    <td>4:50:37</td>
</tr><tr>
    <td><strong>Run:</strong></td>
    <td>3:17:24</td>
</tr><tr>
    <td><strong>Overall:</strong></td>
    <td>9:12:33</td>
</tr>
</tbody></table>

</body>
</html>
"""
html = lxml.html.fromstring(samplehtml)

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
bibId = 1000
while bibId < 1100 :
    bibId += 1
    #call scrape and send to parseHTML 
    pageToScrape = scraperwiki.scrape(urlToScrape % bibId)
    html = lxml.html.fromstring(pageToScrape)  
    try:
        parsePage(html)
    except IndexError:
        #scraperwiki.sqlite.save(unique_keys=['bibId'], data={"BIB":bibId,"YEAR":2013,"EVENT":"test"}, table_name="NO_DATA_FOUND")
        print "problem with bibID %d " % bibId
    
