import scraperwiki
from BeautifulSoup import BeautifulSoup

print "List of airports in India"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_airports_in_India')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['cityserved/location', 'ICAO', 'IATA' , 'Airport name', 'Role', 'State or Territory'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        ExDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            ExDetails['cityserved/location'] = TableColumns[0].text          
            ExDetails['ICAO'] = TableColumns[1].text
            ExDetails['IATA'] = TableColumns[2].text
            ExDetails['Airport name']= TableColumns[3].text
            ExDetails['Role'] = TableColumns[4].text          
            ExDetails['State or Territory'] = TableColumns[5].text
            scraperwiki.datastore.save(["cityserved/location"], ExDetails)
            print ExDetails


