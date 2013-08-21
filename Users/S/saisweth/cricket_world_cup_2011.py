# Blank Python
# Creator : Sainath Varanasi
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "World Cup 2011 Circket"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/2011_Cricket_World_Cup_schedule')

WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', [ 'Day','Time','Venue','Stage','Team 1','Result','Team 2'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable" })
TableRows = TableDetails.findAll("tr")
print "Cricket World Cup 2011",TableRows
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
                Details['Day'] = TableColumns[0].text  
                #Details['Time'] = TableColumns[1].text
                Details['Venue'] = TableColumns[2].text
                Details['Stage'] = TableColumns[3].text
                Details['Team 1'] = TableColumns[4].text
                Details['Result'] = TableColumns[5].text 
                #Details['Team 2'] = TableColumns[6].text    
                scraperwiki.datastore.save(["Day"], Details)     
                print Details



