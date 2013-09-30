import scraperwiki
import requests
import urllib2
from scraperwiki import scrape
from scraperwiki.sqlite import save
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import re


# this scrapes the details of a single NYC lobbyist organization

target_org_url = 'http://www.nyc.gov/lobbyistsearch/search?lobbyist=1199+SEIU+United+Healthcare+Workers+East'
detail_url_base = 'http://www.nyc.gov/lobbyistsearch/print.jsp?lid='

lobbyists = urllib2.urlopen(target_org_url)
soupedPage = BeautifulSoup(lobbyists)
#start with the first page of info; this is easy

totalPages = 0
lobbyistIDs = []

#one set of links that will come up in this contains the "Page 1 of x" text. We'll use this to build a loop for subsequent pages
for allPages in soupedPage.findAll("td", "table_text", colspan=True):
    countText = allPages.contents[0]
    breakArray = countText.rsplit("&nbsp;")
    pageCount = breakArray[0].rsplit()
    totalPages = int(pageCount[3])


for pages in range(totalPages):
    target_url = target_org_url+'&op=&pg_l='+str(pages+1)
    pageData = urllib2.urlopen(target_url)
    soupedData = BeautifulSoup(pageData)

    for allCells in soupedData.findAll("td", "table_text"):
        for allLinks in allCells.findAll("a", onmouseover=True):
            myOverImage = allLinks['onmouseover']
            myHREF = allLinks['href']
            if re.search('Image223122', myOverImage):
                myArray = myHREF.rsplit('=')
                myID = myArray[1].split("'")
                lobbyistIDs.append(myID[0])
                print(myID[0])

#now that we've collected all the org ids, iterate over *that* list, loading, parsing & storing the detail info for each lobbyist record

#ok, start with a sample page
#test_ids = [122088]

for aRecord in lobbyistIDs:
    record_url = detail_url_base+str(aRecord)
    detailData = urllib2.urlopen(record_url)
    soupedDetail = BeautifulSoup(detailData)
    record_holder = []
    addtlLobbyists = []

    for aParam in soupedDetail.findAll("span", "search_instructional"):
        record_holder.append(aParam.renderContents())

    for moreLobbyists in soupedDetail.findAll("td", "search_instructional"):
        addtlLobbyists.append(moreLobbyists.renderContents())

    theTarget = str(record_holder[6]).rsplit("</strong>")
    theSubject = str(record_holder[7]).rsplit("</strong>")
    theLobbyists = addtlLobbyists[0].replace("<br />", " |")
    lobbyistAddress = record_holder[4].replace("<br />", " |")
    clientAddress = record_holder[1].replace("<br />", " |")
    print record_holder
    record_data = { "client_name": record_holder[0],
                    "client_address": clientAddress,
                    "begin_date": record_holder[2],
                    "end_date": record_holder[3],
                    "lobbyists": theLobbyists,
                    "lobbyist_address": lobbyistAddress,
                    "lobbyist_officer": record_holder[5],
                    "target": theTarget[1],
                    "subject":theSubject[1]
    }
    save([],record_data)

import scraperwiki
import requests
import urllib2
from scraperwiki import scrape
from scraperwiki.sqlite import save
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import re


# this scrapes the details of a single NYC lobbyist organization

target_org_url = 'http://www.nyc.gov/lobbyistsearch/search?lobbyist=1199+SEIU+United+Healthcare+Workers+East'
detail_url_base = 'http://www.nyc.gov/lobbyistsearch/print.jsp?lid='

lobbyists = urllib2.urlopen(target_org_url)
soupedPage = BeautifulSoup(lobbyists)
#start with the first page of info; this is easy

totalPages = 0
lobbyistIDs = []

#one set of links that will come up in this contains the "Page 1 of x" text. We'll use this to build a loop for subsequent pages
for allPages in soupedPage.findAll("td", "table_text", colspan=True):
    countText = allPages.contents[0]
    breakArray = countText.rsplit("&nbsp;")
    pageCount = breakArray[0].rsplit()
    totalPages = int(pageCount[3])


for pages in range(totalPages):
    target_url = target_org_url+'&op=&pg_l='+str(pages+1)
    pageData = urllib2.urlopen(target_url)
    soupedData = BeautifulSoup(pageData)

    for allCells in soupedData.findAll("td", "table_text"):
        for allLinks in allCells.findAll("a", onmouseover=True):
            myOverImage = allLinks['onmouseover']
            myHREF = allLinks['href']
            if re.search('Image223122', myOverImage):
                myArray = myHREF.rsplit('=')
                myID = myArray[1].split("'")
                lobbyistIDs.append(myID[0])
                print(myID[0])

#now that we've collected all the org ids, iterate over *that* list, loading, parsing & storing the detail info for each lobbyist record

#ok, start with a sample page
#test_ids = [122088]

for aRecord in lobbyistIDs:
    record_url = detail_url_base+str(aRecord)
    detailData = urllib2.urlopen(record_url)
    soupedDetail = BeautifulSoup(detailData)
    record_holder = []
    addtlLobbyists = []

    for aParam in soupedDetail.findAll("span", "search_instructional"):
        record_holder.append(aParam.renderContents())

    for moreLobbyists in soupedDetail.findAll("td", "search_instructional"):
        addtlLobbyists.append(moreLobbyists.renderContents())

    theTarget = str(record_holder[6]).rsplit("</strong>")
    theSubject = str(record_holder[7]).rsplit("</strong>")
    theLobbyists = addtlLobbyists[0].replace("<br />", " |")
    lobbyistAddress = record_holder[4].replace("<br />", " |")
    clientAddress = record_holder[1].replace("<br />", " |")
    print record_holder
    record_data = { "client_name": record_holder[0],
                    "client_address": clientAddress,
                    "begin_date": record_holder[2],
                    "end_date": record_holder[3],
                    "lobbyists": theLobbyists,
                    "lobbyist_address": lobbyistAddress,
                    "lobbyist_officer": record_holder[5],
                    "target": theTarget[1],
                    "subject":theSubject[1]
    }
    save([],record_data)

