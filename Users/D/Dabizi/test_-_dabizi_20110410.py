import urllib2
import scraperwiki

# use the following variables to set scraper behavior
# a 1 means do that
scrape = 1
popTable = 1
printTable = 0
display = 0


# parse and parseTable copied from http://ariffwambeck.co.uk/2010/11/20/html-table-parser-in-python/
# Simple HtmlTableParser module
# Author: Ariff Wambeck
# Year: 2010

import lxml.html

def parse(url, missingCell="NA"):
    """
    Parses all HTML tables found at the given url. Missing data or those 
    without text content will be replaced with the missingCell string.
    
    Returns a list of lists of strings, corresponding to rows within all 
    found tables.
    """
    doc = lxml.html.parse(url)
    tableList = doc.xpath("/html//table")
    dataList = []
    for table in tableList:
        dataList.append(parseTable(table, missingCell))
    return dataList

def parseTable(table, missingCell):
    """
    Parses the individual HTML table, returning a list of its rows.
    """
    rowList = []
    for row in table.xpath('.//tr'):
        colList = []
        cells = row.xpath('.//th') + row.xpath('.//td')
        for cell in cells:
            # The individual cell's content
            content = cell.text_content().encode("utf8")
            content = content.strip("\t")
            if content == "":
                content = missingCell
            colList.append(content)
        rowList.append(colList)
    return rowList

urlBase = "http://www.nwhc.usgs.gov/publications/quarterly_reports/"
# as of now no report for q4 2010
lastQuarter = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4]

if scrape == 1:
    for year in range(1995, 2011):
        for quarter in range (1, lastQuarter [year - 1995]):
            url = urlBase + str(year) + "_qtr_" + str(quarter) + ".jsp"
            print url
            tableList = parse(url, "-")
            tableList = [year] + tableList
            print tableList


#url = "http://www.nwhc.usgs.gov/publications/quarterly_reports/1995_qtr_4.jsp"
# original, only needed for regression
#url = "http://www.nwhc.usgs.gov/publications/quarterly_reports/2009_qtr_4.jsp"
# 2009 qtr3 has estimates with ***
#url = 'http://www.nwhc.usgs.gov/publications/quarterly_reports/2010_qtr_3.jsp'
# 2010qt3 has a \t after some fields.  Fix that
# tests 1417(e), 450    (e), 1417** and non-breakable spaces
url = 'http://www.nwhc.usgs.gov/publications/quarterly_reports/1999_qtr_1.jsp'
# has a '???' in count field

# here go ahead and grab all the tables once and hold it in the scraper

if popTable == 1:
    year = tableList[0]
#    tableList = tableList[0:]
    for table in tableList[1:]:
        for row in table:
            if len(row) == 7 and row[0] <> 'ReportedState ':
            
            # might need other logic once we get to later quarters
                row[4] = row[4].replace("\xc2\xa0", " ")
                row[4] = row[4].strip().replace(',','')
                if row[4] == '' or row[4] == '???':
                    count = 0
                    note = "Data not available.  Please check other fields or the website."
                elif row[4] == '***':
                    count = 0
                    note = 'est. not available'
                elif row[4][-2:] == '**':
                    count = row[4][:-2]
                    note = 'Virulent Newcastle Disease Virus'
                else:
                    countSplit = row[4].split("(")
                    # remove estimates out of count
                    if len(countSplit) == 2:
                            note = countSplit[1].strip('(')
                            note = note.strip(')')
                    else:
                        note = ''
                    count = countSplit[0].strip().replace(',','')
    
                row[4] = count
                row.append(note)
    #            print row[4], row
                # save these records in the database
                data1 = {"Year":year,"State":row[0],"Location":row[1],"Dates":row[2],"Species":row[3]
                ,"Mortality":int(row[4]),"Diagnosis":row[5],"Reported_By":row[6],"Notes":row[7]}
                scraperwiki.sqlite.save(unique_keys=["State", "Location","Dates","Species"], data=data1)
                # do not know if i need to request a table be created or what
    #            if int(row[4]) > 200:
    #                print 'Greater than 200!'

if printTable == 1:
    print scraperwiki.sqlite.select("* from ScrapeUSGS.swdata WHERE Mortality > 1000")




# do not forget the update tables on some of the pages.

# code snippets and other scrapers might find interesting
# print "The first 2000 characters of the page is:", html[:2000]
# a bar chart
# http://scraperwiki.com/views/bar_chart_of_exceedences/edit/