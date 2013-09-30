import urllib2
import scraperwiki

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

for year in range(2010, 2011):
    for quarter in range (1,5):
        url = urlBase + str(year) + "_qtr_" + str(quarter) + ".jsp"
        print url
        tableList = parse(url, "-")
        print tableListimport urllib2
import scraperwiki

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

for year in range(2010, 2011):
    for quarter in range (1,5):
        url = urlBase + str(year) + "_qtr_" + str(quarter) + ".jsp"
        print url
        tableList = parse(url, "-")
        print tableList