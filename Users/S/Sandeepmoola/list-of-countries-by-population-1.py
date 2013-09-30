# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "List of Countries by Population"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_countries_by_population')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Rank', 'Country / Territory','Population' , 'Date of estimate',' % of World population','Source'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['Rank'] = TableColumns[0].text          
            Details['Country / Territory'] = TableColumns[1].text
            Details['Population'] = TableColumns[2].text
            Details['Date of estimate']= TableColumns[3].text
            Details['Percentage World population']= TableColumns[4].text
            scraperwiki.datastore.save(["Population"], Details)
            print Details


# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "List of Countries by Population"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_countries_by_population')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Rank', 'Country / Territory','Population' , 'Date of estimate',' % of World population','Source'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['Rank'] = TableColumns[0].text          
            Details['Country / Territory'] = TableColumns[1].text
            Details['Population'] = TableColumns[2].text
            Details['Date of estimate']= TableColumns[3].text
            Details['Percentage World population']= TableColumns[4].text
            scraperwiki.datastore.save(["Population"], Details)
            print Details


