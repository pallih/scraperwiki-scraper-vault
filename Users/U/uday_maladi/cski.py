import scraperwiki
from BeautifulSoup import BeautifulSoup

print "county-cricket-championship-fixtures-2011"

HtmlPage = scraperwiki.scrape('http://www.guardian.co.uk/sport/blog/2010/dec/14/county-cricket-championship-fixtures-2011')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['NO', 'Date','Duration (days)' , 'Home','Away','Venu','Comp','Flood Lit'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("td")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['NO'] = TableColumns[0].text          
            Details['Date'] = TableColumns[1].text
            Details['Duration (days)'] = TableColumns[2].text
            Details['Home']= TableColumns[3].text
            Details['Away']= TableColumns[4].text
            Details['Venu'] = TableColumns[5].text
            Details['Comp']= TableColumns[6].text
            Details['Flood lit']= TableColumns[7].text
            scraperwiki.datastore.save(["Date"], Details)
            print Detailsimport scraperwiki
from BeautifulSoup import BeautifulSoup

print "county-cricket-championship-fixtures-2011"

HtmlPage = scraperwiki.scrape('http://www.guardian.co.uk/sport/blog/2010/dec/14/county-cricket-championship-fixtures-2011')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['NO', 'Date','Duration (days)' , 'Home','Away','Venu','Comp','Flood Lit'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable sortable" })
TableRows = TableDetails.findAll("td")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['NO'] = TableColumns[0].text          
            Details['Date'] = TableColumns[1].text
            Details['Duration (days)'] = TableColumns[2].text
            Details['Home']= TableColumns[3].text
            Details['Away']= TableColumns[4].text
            Details['Venu'] = TableColumns[5].text
            Details['Comp']= TableColumns[6].text
            Details['Flood lit']= TableColumns[7].text
            scraperwiki.datastore.save(["Date"], Details)
            print Details