import urllib2
import scraperwiki
import sys

# use the following variables to set scraper behavior
# a 1 means do that
scrape = 1
popTable = 1
printTable = 0
display = 0
printTableList = 0

def RepresentsInt(s):
    #print s
    try: 
        int(s)
        return True
    except ValueError:
        return False

# parse and parseTable copied from http://ariffwambeck.co.uk/2010/11/20/html-table-parser-in-python/
# Simple HtmlTableParser module
# Author: Ariff Wambeck
# Year: 2010
#
# Ken Keller 4/29/2011
# modified code to only add unique rows pertinant to this scraper
#

import lxml.html

def parse(url, missingCell="NA"):
    """
    Parses all HTML tables found at the given url. Missing data or those 
    without text content will be replaced with the missingCell string.
    
    Returns a list of lists of strings, corresponding to rows within all 
    found tables.
    """
    doc = lxml.html.parse(url)
    #print doc
    tableList = doc.xpath("/html//table")
    dataList = []
    #print len(tableList), tableList
    for table in tableList:
        # ken modification
        temp = parseTable(table, missingCell)
        if len(temp) <> 0:
            #dataList.append(temp)
            dataList = dataList+filter(lambda x:x not in dataList,temp)
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
            #print len(colList), colList
        # ken modification
        if len(colList) == 7 and colList[0] <> 'ReportedState ':            
            rowList.append(colList)
    #print len(rowList), rowList
    return rowList

urlBase = "http://www.nwhc.usgs.gov/publications/quarterly_reports/"
# as of now no report for q4 2010
lastQuarter = [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4]
deathTable = []

if scrape == 1:
    for year in range(2001, 2002):
        for quarter in range (1, lastQuarter [year - 1995]):
            url = urlBase + str(year) + "_qtr_" + str(quarter) + ".jsp"
            print url
            tableList = parse(url, "-")
            for row in tableList:
                row = row + [str(year)]
                deathTable = deathTable + [row]
            #print len(deathTable), deathTable  

# Tests
#
#url = "http://www.nwhc.usgs.gov/publications/quarterly_reports/1995_qtr_4.jsp"
# original, only needed for regression
#url = "http://www.nwhc.usgs.gov/publications/quarterly_reports/2009_qtr_4.jsp"
# 2009 qtr3 has estimates with ***
#url = 'http://www.nwhc.usgs.gov/publications/quarterly_reports/2010_qtr_3.jsp'
# 2010qt3 has a \t after some fields.  Fix that
# tests 1417(e), 450    (e), 1417** and non-breakable spaces
#url = 'http://www.nwhc.usgs.gov/publications/quarterly_reports/1999_qtr_1.jsp'
# has a '???' in count field
#url = 'http://www.nwhc.usgs.gov/publications/quarterly_reports/2003_qtr_2.jsp'
# has a row with extra "headers="header1""
# http://www.nwhc.usgs.gov/publications/quarterly_reports/1997_qtr_1.jsp
# has species and mortality mixed up

# here go ahead and grab all the tables once and hold it in the scraper

if popTable == 1:
    print len(deathTable)
    data1 = []
    for row in deathTable:
        #print len(row), row
        if len(row) == 8 and (row[0][:13] <> 'ReportedState'):


            # might need other logic once we get to later quarters
            # q1 and q2 1997 switched species and row at least once
            print row[4]
            # commas detecting as a string
            if (RepresentsInt(row[4].replace(',','')) == False and (row[4].strip()[-3:] != "(e)")):
                print "found one!"
                print "Before ", row
                temp = row[3]
                row[3] = row[4]
                row[4] = temp
            print "After ", row

            row[4] = row[4].replace("\xc2\xa0", " ")
            row[4] = row[4].strip().replace(',','')

            # clean up header error
            #print "before ", row[0], " ", row[0][:9]
            if row[0][:9] ==  " headers=":
                for col in range(0,7):
                    #print row[col], "remaining string: ", row[col][18:]
                    row[col] = row[col][18:]
            #print "after ", row[0], " ", " ", row[0][:9], " ", row
            # clean up mortality colum
            if row[4] == '' or row[4] == '???':
                count = 0
                note = "Data not available.  Please check other fields or the website."
            elif row[4] == '***':
                count = 0
                note = 'est. not available'
            elif row[4][-2:] == '**':
                count = row[4][:-2]
                note = 'Virulent Newcastle Disease Virus'
            else: # should prob make est. and e the same note
                countSplit = row[4].split("(")
                # remove estimates out of count, ad put into note
                if len(countSplit) == 2:
                        note = countSplit[1].strip('(')
                        note = note.strip(')')
                else:
                    note = ''
                count = countSplit[0].strip().replace(',','')
            row[4] = count
            row.append(note)
            # save these records in the database
            try:
                data1 = {"Year":str(row[7]),"State":row[0],"Location":row[1],"Dates":row[2],"Species":row[3]
                ,"Mortality":int(row[4]),"Diagnosis":row[5],"Reported_By":row[6],"Notes":row[8]}
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print "Year ", str(row[7])," State ", row[0]," Location ", row[1]," Dates ", row[2]," Species ", row[3]
                print " Mortality ", int(row[4])," Diagnosis ", row[5]," Reported_By ", row[6]," Notes ",row[8]
            #print data1
            try:
                scraperwiki.sqlite.save(unique_keys=["State", "Location","Dates","Species","Year"], data=data1)
            except:
                print "Unexpected error:", sys.exc_info()[0]
                print data1

if printTableList == 1:
    year = tableList[0]
    for table in tableList:
        for row in table[0:]:
            print row

if printTable == 1:
    print scraperwiki.sqlite.select("* from ScrapeUSGS.swdata WHERE Mortality > 1000")




# do not forget the update tables on some of the pages.
# todo: add 2010 data

# code snippets and other scrapers might find interesting
# print "The first 2000 characters of the page is:", html[:2000]
# a bar chart
# http://scraperwiki.com/views/bar_chart_of_exceedences/edit/