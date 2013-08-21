import scraperwiki
from BeautifulSoup import BeautifulSoup



def generateOutput(obj):
    scraperwiki.metadata.save('data_columns', ['Rank','Country', 'Users (thousands)'])
    HtmlTable = obj.find("table",{"class":"wikitable sortable"})
    #To identify each row of the table:
    TableRows = HtmlTable.findAll("tr")
    for row in TableRows:
        record = {}
        #To identify each cell of the table
        TableColumns = row.findAll("td")
        #The number of cells in each row:
        if len(TableColumns) == 3:
            record['Rank'] = TableColumns[0].text
            record['Country'] = TableColumns[1].text
            record['Users (thousands)'] = TableColumns[2].text
            
            

            print record,
            print "-------------"
            #Saving the data with the unique key :
            scraperwiki.datastore.save(["Country"], record)



dataSource="http://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users"
getHTML=scraperwiki.scrape(dataSource)
Object = BeautifulSoup(getHTML)
generateOutput(Object)
