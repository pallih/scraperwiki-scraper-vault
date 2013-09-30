import scraperwiki
from BeautifulSoup import BeautifulSoup

print "List of countries by electricity"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Rank', 'Country','Electricity consumption (MW·h/yr)' , 'Year of Data','Source','population','As of','Average power per capita (<a href="/wiki/Watt" title="Watt">watts</a> per person)'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        WCDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            WCDetails['Rank'] = TableColumns[0].text          
            WCDetails['Country'] = TableColumns[1].text
            WCDetails['Electricity consumption (MW·h/yr)'] = TableColumns[2].text
            WCDetails['Population']= TableColumns[3].text
            b = TableColumns[4].find("a")
            if b.text!="title":
                WCDetails['year of Data'] = b.text            
            WCDetails['Source'] = TableColumns[5].text            
            scraperwiki.datastore.save(["Rank"], WCDetails)
            print WCDetailsimport scraperwiki
from BeautifulSoup import BeautifulSoup

print "List of countries by electricity"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Rank', 'Country','Electricity consumption (MW·h/yr)' , 'Year of Data','Source','population','As of','Average power per capita (<a href="/wiki/Watt" title="Watt">watts</a> per person)'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        WCDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            WCDetails['Rank'] = TableColumns[0].text          
            WCDetails['Country'] = TableColumns[1].text
            WCDetails['Electricity consumption (MW·h/yr)'] = TableColumns[2].text
            WCDetails['Population']= TableColumns[3].text
            b = TableColumns[4].find("a")
            if b.text!="title":
                WCDetails['year of Data'] = b.text            
            WCDetails['Source'] = TableColumns[5].text            
            scraperwiki.datastore.save(["Rank"], WCDetails)
            print WCDetails