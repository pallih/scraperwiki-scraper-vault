import scraperwiki
from BeautifulSoup import BeautifulSoup



def generateOutput(obj):
    scraperwiki.metadata.save('data_columns', ['Country','Currency', 'Pair','Yearly%Chq'])
    #HtmlTable = obj.find("table")
    HtmlTable = obj.find(id='ctl00_ContentPlaceHolder1_CurrencyMatrixChanges1_GridView1')
    #To identify each row of the table:
    TableRows = HtmlTable.findAll("tr")
    for row in TableRows:
        record = {}
        #To identify each cell of the table
        TableColumns = row.findAll("td")
        #The number of cells in each row:
        if len(TableColumns) == 4:
            record['Country'] = TableColumns[0].text
            record['currency'] = TableColumns[1].text
            record['Pair'] = TableColumns[2].text
            record['Yearly % Chq'] = TableColumns[3].text
            

            print record,
            print "-------------"
            #Saving the data with the unique key :
            scraperwiki.datastore.save(["Country"], record)



dataSource="http://www.tradingeconomics.com/analytics.aspx"
getHTML=scraperwiki.scrape(dataSource)
Object = BeautifulSoup(getHTML)
generateOutput(Object)

import scraperwiki
from BeautifulSoup import BeautifulSoup



def generateOutput(obj):
    scraperwiki.metadata.save('data_columns', ['Country','Currency', 'Pair','Yearly%Chq'])
    #HtmlTable = obj.find("table")
    HtmlTable = obj.find(id='ctl00_ContentPlaceHolder1_CurrencyMatrixChanges1_GridView1')
    #To identify each row of the table:
    TableRows = HtmlTable.findAll("tr")
    for row in TableRows:
        record = {}
        #To identify each cell of the table
        TableColumns = row.findAll("td")
        #The number of cells in each row:
        if len(TableColumns) == 4:
            record['Country'] = TableColumns[0].text
            record['currency'] = TableColumns[1].text
            record['Pair'] = TableColumns[2].text
            record['Yearly % Chq'] = TableColumns[3].text
            

            print record,
            print "-------------"
            #Saving the data with the unique key :
            scraperwiki.datastore.save(["Country"], record)



dataSource="http://www.tradingeconomics.com/analytics.aspx"
getHTML=scraperwiki.scrape(dataSource)
Object = BeautifulSoup(getHTML)
generateOutput(Object)

