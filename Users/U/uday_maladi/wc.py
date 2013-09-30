import scraperwiki
from BeautifulSoup import BeautifulSoup

print "FIFA World-Cup Details with Winner and Runner"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/Football_World_Cup')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Year', 'Host', 'Winner' , 'Score','Runner-up','third-Place','score','Fourth-place'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        WCDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            WCDetails['Year'] = TableColumns[0].text          
            WCDetails    b = TableColumns[3].find("a")
            if b.text!"title":
                WCDetails['Score'] = b.text            
            WCDetails['Runnerup'] = TableColumns[4].text            
            scraperwiki.datastore.save(["Year"], WCDetails)
            print WCDetails
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "FIFA World-Cup Details with Winner and Runner"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/Football_World_Cup')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Year', 'Host', 'Winner' , 'Score','Runner-up','third-Place','score','Fourth-place'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        WCDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            WCDetails['Year'] = TableColumns[0].text          
            WCDetails    b = TableColumns[3].find("a")
            if b.text!"title":
                WCDetails['Score'] = b.text            
            WCDetails['Runnerup'] = TableColumns[4].text            
            scraperwiki.datastore.save(["Year"], WCDetails)
            print WCDetails
