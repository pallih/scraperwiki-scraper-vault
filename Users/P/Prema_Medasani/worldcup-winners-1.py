import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Worldcup Winners"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals')
WebPageSource = BeautifulSoup(HtmlPage)
#scraperwiki.metadata.save('data_columns', ['Year', 'Winners','Final score ','Runners-up','Venue','Location'])

TableDetails = WebPageSource.first('table', { "class" : "sortable wikitable" })

TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableDetails
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['Year'] = TableColumns[0].text          
            Details['Winners'] = TableColumns[1].text.replace("&#160;","")
            Details['Final score'] = TableColumns[2].text.replace("&#160;","")
            Details['Runners-up'] = TableColumns[3].text.replace("&#160;","")
            Details['Venue'] = TableColumns[4].text
            Details['Location'] = TableColumns[5].text
            scraperwiki.sqlite.save(["Year"], Details)
            print Details
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Worldcup Winners"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals')
WebPageSource = BeautifulSoup(HtmlPage)
#scraperwiki.metadata.save('data_columns', ['Year', 'Winners','Final score ','Runners-up','Venue','Location'])

TableDetails = WebPageSource.first('table', { "class" : "sortable wikitable" })

TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableDetails
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['Year'] = TableColumns[0].text          
            Details['Winners'] = TableColumns[1].text.replace("&#160;","")
            Details['Final score'] = TableColumns[2].text.replace("&#160;","")
            Details['Runners-up'] = TableColumns[3].text.replace("&#160;","")
            Details['Venue'] = TableColumns[4].text
            Details['Location'] = TableColumns[5].text
            scraperwiki.sqlite.save(["Year"], Details)
            print Details
