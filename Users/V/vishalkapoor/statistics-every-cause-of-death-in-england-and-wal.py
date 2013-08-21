import scraperwiki
from BeautifulSoup import BeautifulSoup



def generateOutput(obj):
    scraperwiki.metadata.save('data_columns', ['Cause Of Death','Male', 'Female','2009 Total','Rate per 100,000 pop, 2009','2008 Total','Rate per 100,000 pop, 2009'])
    HtmlTable = obj.find("table", {"class": "in-article sortable"})
    #To identify each row of the table:
    TableRows = HtmlTable.findAll("tr")
    for row in TableRows:
        record = {}
        #To identify each cell of the table 
        TableColumns = row.findAll("td")
        #The number of cells in each row:
        if len(TableColumns) == 7:
            record['Cause Of Death'] = TableColumns[0].text
            record['Male'] = TableColumns[1].text
            record['Female'] = TableColumns[2].text
            record['2009 Total'] = TableColumns[3].text
            record['2009 Rate Per 100000'] = TableColumns[4].text
            record['2008 Total'] = TableColumns[5].text
            record['2008 Rate Per 100000'] = TableColumns[6].text

            print record,
            print "-------------"
            #Saving the data with the unique key :
            scraperwiki.datastore.save(["Cause Of Death"], record)



dataSource="http://www.guardian.co.uk/news/datablog/2011/jan/14/mortality-statistics-causes-death-england-wales-2009"
getHTML=scraperwiki.scrape(dataSource)
Object = BeautifulSoup(getHTML)
generateOutput(Object)

