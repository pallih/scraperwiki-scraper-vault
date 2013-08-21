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
        Details = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            Details['Rank'] = TableColumns[0].text          
            Details['Country'] = TableColumns[1].text.replace("&#160;", "")
            Details['Electricity consumption (MW·h/yr)'] = TableColumns[2].text
            Details['Population']= TableColumns[3].text
            Details['As of']= TableColumns[4].text
            Details['Average power per capita (<a href="/wiki/Watt" title="Watt">watts</a> per person)']= TableColumns[5].text
            b = TableColumns[6].find("a")
            if (b):
                if b.text != "title":
                    Details['year of Data'] = b.text            
            Details['Source'] = TableColumns[7].text            
            scraperwiki.datastore.save(["Rank"], Details)
            print Details