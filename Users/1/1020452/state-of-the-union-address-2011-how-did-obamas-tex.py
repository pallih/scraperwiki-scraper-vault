import scraperwiki
from BeautifulSoup import BeautifulSoup
def anil():
    scraperwiki.metadata.save('data_columns', ['Word', 'Washington', 'Lincoln' ,'Roosevelt','Kennedy','Reagan', 'GW Bush','Obama'])#Inserting the column details
    TableDetails = WebPageSource.find("table", { "class" : "wikitable" })
    TableRows = TableDetails.findAll("tr")
    print "Total Records in the Dictionary are:--",TableRows
    #Inserting the rows of the table
    for TableRow in TableRows:
        UNDetails = {}
#inserting the rows
        TableColumns = TableRow.findAll("td")
        if len(TableColumns)==8:
            UNDetails['Word'] = TableColumns[0].text          
            UNDetails['Washington'] = TableColumns[1].text
            UNDetails['Lincoln'] = TableColumns[2].text
            UNDetails['Roosevelt'] = Tablecolumns[3].text
            UNDetails['Kennedy'] = Tablecolumns[4].text
            UNDetails['Reagan'] = Tablecolumns[5].text
            UNDetails['GW Bush'] = Tablecolumns[6].text
            UNDetails['Obama'] = Tablecolumns[7].text
            b = TableColumns[0].find("a")
            if b.text!="title":
                UNDetails['Obama'] = b.text            
                UNDetails['Washington'] = TableColumns[4].text            
                scraperwiki.datastore.save(["Kennedy"], UNDetails)#saving the data
                print UNDetails
 

print "State of the union address 2011: how did Obama's text compare to other US presidents ?"

HtmlPage = scraperwiki.scrape('http://www.guardian.co.uk/news/datablog/2011/jan/25/state-of-the-union-text-obama')#describing the HTML page,where the data was taken
WebPageSource = BeautifulSoup(HtmlPage)
