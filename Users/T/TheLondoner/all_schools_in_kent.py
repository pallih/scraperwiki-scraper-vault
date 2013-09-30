##################################################
# All Schools in Kent
##################################################

import scraperwiki
import sys
from BeautifulSoup import BeautifulSoup

rootUrl = "http://schoolswebdirectory.co.uk/"

#process an individual school record and save it
def scrapeSchool(link, leaName):
    try:
        key = ""
        value = ""
        record = {}
        record[u"LEA"] = leaName
        schoolHtml = scraperwiki.scrape(link)
        schoolSoup = BeautifulSoup(schoolHtml)
        firstRow = schoolSoup.find("tr", {"valign": "middle"})

        try:
            if firstRow.find("font", {"size": "1"}):
                key = firstRow.find("font", {"size": "1"}).text.replace(":","")
            if firstRow.find("font", {"size": "2"}):
                 value = firstRow.find("font", {"size": "2"}).text
            if key != "":
                record[key] = value.replace("&rsquo;","'").replace('/','_')
        except Exception,e:
            print "Exception thrown in: scrapeSchool: processing firstRow", e

        tableRows = firstRow.findNextSiblings('tr') 
        for tableRow in tableRows:
            key = ""
            value = ""
            try:
                if tableRow.find("font", {"size": "1"}):
                    key = tableRow.find("font", {"size": "1"}).text.replace(":","")
                if key == "or to send in a picture...please email us":
                    key = ""
                elif key == "LEA" or key == "Type":
                    if tableRow.find("td", {"class": "infotext3"}):
                        value = tableRow.find("td", {"class": "infotext3"}).text
                elif key == "Info Last Updated":
                    if tableRow.find("span", {"class": "listtext1"}):
                        value = tableRow.find("span", {"class": "listtext1"}).text
                elif tableRow.find("font", {"size": "2"}):
                    value = tableRow.find("font", {"size": "2"}).text
                if key != "":
                    value = value.replace("&rsquo;","'")
                    record[key.replace('/','_')] = value.replace("&nbsp;&nbsp;&nbsp;",",")
            except Exception,e:
                print "Exception thrown in: scrapeSchool: for loop", e
        scraperwiki.datastore.save([u"School"], record)
    except Exception, e:
        print "Exception thrown in: scrapeSchool: link: "+link+", LEA: "+leaName +  str(e)

    
def pageUrl(startingUrl,leaName):
    try:
        leaText = leaName+" LEA"
        html = scraperwiki.scrape(startingUrl)
        soup = BeautifulSoup(html)
        leaSpan = soup.find('p', align="left")
        if leaSpan:
            skipInfo = 0
            aLinks = leaSpan.findAll("a")
            for aLink in aLinks:
                if skipInfo == 1:
                    skipInfo = 0
                else:
                    if aLink.text == leaText:
                        skipInfo = 1
                    else:
                        if aLink.text == "info":
                            link = rootUrl+aLink['href']
                            scrapeSchool(link,leaName)
    except Exception,e:
        print "Exception thrown in: pageUrl", e


#for a given lea get the list of schools and scrape them
def leaSweep(leaName):
    try:
        baseUrl = rootUrl+"leasearch.php?lea="+leaName+"&submit=Submit+Query"
        pageUrl(baseUrl,leaName)
    except Exception,e:
        print "Exception thrown in: leaSweep: leaName = "+leaName



#search the schools web directory for all of Kent's LEA's
leas = ['Bexley','Bromley','Kent','Medway+Towns']
for lea in leas:
    leaSweep(lea)

# Code to re-run Exceptions detected in scrapeSchool
#scrapeSchool("http://schoolswebdirectory.co.uk/schoolinfo2.php?ref=14392", "Medway+Towns")

##################################################
# All Schools in Kent
##################################################

import scraperwiki
import sys
from BeautifulSoup import BeautifulSoup

rootUrl = "http://schoolswebdirectory.co.uk/"

#process an individual school record and save it
def scrapeSchool(link, leaName):
    try:
        key = ""
        value = ""
        record = {}
        record[u"LEA"] = leaName
        schoolHtml = scraperwiki.scrape(link)
        schoolSoup = BeautifulSoup(schoolHtml)
        firstRow = schoolSoup.find("tr", {"valign": "middle"})

        try:
            if firstRow.find("font", {"size": "1"}):
                key = firstRow.find("font", {"size": "1"}).text.replace(":","")
            if firstRow.find("font", {"size": "2"}):
                 value = firstRow.find("font", {"size": "2"}).text
            if key != "":
                record[key] = value.replace("&rsquo;","'").replace('/','_')
        except Exception,e:
            print "Exception thrown in: scrapeSchool: processing firstRow", e

        tableRows = firstRow.findNextSiblings('tr') 
        for tableRow in tableRows:
            key = ""
            value = ""
            try:
                if tableRow.find("font", {"size": "1"}):
                    key = tableRow.find("font", {"size": "1"}).text.replace(":","")
                if key == "or to send in a picture...please email us":
                    key = ""
                elif key == "LEA" or key == "Type":
                    if tableRow.find("td", {"class": "infotext3"}):
                        value = tableRow.find("td", {"class": "infotext3"}).text
                elif key == "Info Last Updated":
                    if tableRow.find("span", {"class": "listtext1"}):
                        value = tableRow.find("span", {"class": "listtext1"}).text
                elif tableRow.find("font", {"size": "2"}):
                    value = tableRow.find("font", {"size": "2"}).text
                if key != "":
                    value = value.replace("&rsquo;","'")
                    record[key.replace('/','_')] = value.replace("&nbsp;&nbsp;&nbsp;",",")
            except Exception,e:
                print "Exception thrown in: scrapeSchool: for loop", e
        scraperwiki.datastore.save([u"School"], record)
    except Exception, e:
        print "Exception thrown in: scrapeSchool: link: "+link+", LEA: "+leaName +  str(e)

    
def pageUrl(startingUrl,leaName):
    try:
        leaText = leaName+" LEA"
        html = scraperwiki.scrape(startingUrl)
        soup = BeautifulSoup(html)
        leaSpan = soup.find('p', align="left")
        if leaSpan:
            skipInfo = 0
            aLinks = leaSpan.findAll("a")
            for aLink in aLinks:
                if skipInfo == 1:
                    skipInfo = 0
                else:
                    if aLink.text == leaText:
                        skipInfo = 1
                    else:
                        if aLink.text == "info":
                            link = rootUrl+aLink['href']
                            scrapeSchool(link,leaName)
    except Exception,e:
        print "Exception thrown in: pageUrl", e


#for a given lea get the list of schools and scrape them
def leaSweep(leaName):
    try:
        baseUrl = rootUrl+"leasearch.php?lea="+leaName+"&submit=Submit+Query"
        pageUrl(baseUrl,leaName)
    except Exception,e:
        print "Exception thrown in: leaSweep: leaName = "+leaName



#search the schools web directory for all of Kent's LEA's
leas = ['Bexley','Bromley','Kent','Medway+Towns']
for lea in leas:
    leaSweep(lea)

# Code to re-run Exceptions detected in scrapeSchool
#scrapeSchool("http://schoolswebdirectory.co.uk/schoolinfo2.php?ref=14392", "Medway+Towns")

