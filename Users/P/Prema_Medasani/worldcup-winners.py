import scraperwiki
from BeautifulSoup import BeautifulSoup

print "world cup winners"

HtmlPage = scraperwiki.scrape('http://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Year',    'Winners',    'Final score',    'Runners-up',    'Venue',    'Location',    'Refs'])

FinalsHeading = WebPageSource.find('span', {'id':'Finals'}).parent
TableDetails = FinalsHeading.findNextSibling(
    lambda tag: 
        (tag.name == 'table') and \
        ('wikitable' in tag['class']) and \
        ('sortable' in tag['class']))
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        Details = {}
        TableColumns = TableRow.findAll("td")
        
        if len(TableColumns) < 7:
            print len(TableColumns)
            continue
        
        if TableColumns:
            Details['Year'] = TableColumns[0].text          
            Details['Winners'] = TableColumns[1].text
            Details['Final score'] = TableColumns[2].text
            Details['Runners-up']= TableColumns[3].text
            Details['Venue'] = TableColumns[4].text          
            Details['Location'] = TableColumns[5].text
            Details['Refs'] = TableColumns[6].text
            scraperwiki.datastore.save(["Year"], Details)
            print Details

            



