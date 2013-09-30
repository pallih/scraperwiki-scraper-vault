import scraperwiki
import lxml.html
import csv
# re is for the substing selection
import re

def getSubStrings(text,startString,endString):
    text = text
    startString = startString
    endString = endString
    retVal = []
    starts = [match.start() for match in re.finditer(re.escape(startString), text)]
    ends = [match.start() for match in re.finditer(re.escape(endString), text)]

    for index in range(len(starts)):
        retVal.append(text[starts[index]+len(startString):ends[index]])
    return retVal

def searchByScientificName(taxon):
    taxon=taxon.replace(' ','%20')
    url = 'http://www.itis.gov/ITISWebService/services/ITISService/searchByScientificName?srchKey='+str(taxon)
    html = scraperwiki.scrape(url)
    retVal=getSubStrings(html,'<ax21:tsn>','</ax21:tsn>')
    return retVal


data = scraperwiki.scrape("https://dl.dropbox.com/u/6913631/match.txt")
reader = csv.reader(data.splitlines(), delimiter='\t')

for row in reader:
    print "Taxon: %s TSN: %s" % (row[0], row[1])
    x = searchByScientificName(row[0])
    print x


import scraperwiki
import lxml.html
import csv
# re is for the substing selection
import re

def getSubStrings(text,startString,endString):
    text = text
    startString = startString
    endString = endString
    retVal = []
    starts = [match.start() for match in re.finditer(re.escape(startString), text)]
    ends = [match.start() for match in re.finditer(re.escape(endString), text)]

    for index in range(len(starts)):
        retVal.append(text[starts[index]+len(startString):ends[index]])
    return retVal

def searchByScientificName(taxon):
    taxon=taxon.replace(' ','%20')
    url = 'http://www.itis.gov/ITISWebService/services/ITISService/searchByScientificName?srchKey='+str(taxon)
    html = scraperwiki.scrape(url)
    retVal=getSubStrings(html,'<ax21:tsn>','</ax21:tsn>')
    return retVal


data = scraperwiki.scrape("https://dl.dropbox.com/u/6913631/match.txt")
reader = csv.reader(data.splitlines(), delimiter='\t')

for row in reader:
    print "Taxon: %s TSN: %s" % (row[0], row[1])
    x = searchByScientificName(row[0])
    print x


