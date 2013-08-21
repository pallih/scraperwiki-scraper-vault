# Blank Python
import scraperwiki
from BeautifulSoup import BeautifulSoup

print "The top-paying universities"

HtmlPage = scraperwiki.scrape('http://www.guardian.co.uk/news/datablog/2010/mar/12/universities-high-pay-top-data?INTCMP=SRCH')
WebPageSource = BeautifulSoup(HtmlPage)
scraperwiki.metadata.save('data_columns', ['Instituitions', 'Vice chancellor earnings 2008-09,£000s', 'No. of staff earning morethan £100k' ,'Ratio of high paid staff per 1000','Ratio of high paid non clinical staff per 1000','Last years rise in vice chancellor earnings, %', '10-yr rise in vice chancellor earnings,%','Notes'])
TableDetails = WebPageSource.find("table", { "class" : "wikitable" })
TableRows = TableDetails.findAll("tr")
print "Total Records in the Dictionary are:--",TableRows
for TableRow in TableRows:
        WCDetails = {}
        TableColumns = TableRow.findAll("td")
        if TableColumns:
            WCDetails['Instituitions'] = TableColumns[0].text          
            WCDetails['Vice chancellors earnings 2008-09,£000s'] = TableColumns[1].text
            WCDetails['No of staff earnings more than £100k'] = TableColumns[2].text
            WCDetails['Ratio of high paid staff per 1000'] = TableColumns[3].text
            WCDetails['Ratio of high paid non clinical staff per 1000'] = TableColumns[4].text
            WCDetails['Last years rising vice chancellor earnings,%'] = TableColumns[5].text
            WCDetails['10-yr rise in vice chancellor earnings,%'] = TableColumns[6].text
            WCDetails['Notes'] = TableColumns[7].text
            b = TableColumns[0].find("a")
            if b.text!="title":
                WCDetails['Instituitions'] = b.text            
            WCDetails['Ratio of high paid non clinical staff per 1000'] = TableColumns[4].text            
            scraperwiki.datastore.save(["10-yr rise in vice chancellor earnings,%"], WCDetails)
            print WCDetails
