import scraperwiki
from BeautifulSoup import BeautifulSoup

print "LIST OF COUNTRIES BY POPULATION"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_countries_by_population')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Rank', 'Country / Territory','Population', 'Data of estimate' , '% of World population','Source'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        WCDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            WCDetails['Rank'] = TableColumns[0].text          
            WCDetails['Country / Territory'] = TableColumns[1].text
            WCDetails['Population'] = TableColumns[2].text
            WCDetails['Source'] = TableColumns[3].text            
            WCDetails['% of World population'] = TableColumns[4].text            
            scraperwiki.datastore.save(["Rank"], WCDetails)
            print WCDetails