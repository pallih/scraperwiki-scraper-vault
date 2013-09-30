import scraperwiki
import urllib2
import datetime
import calendar
import cgi
import os
import mechanize
import re
import math
import requests
import cookielib
import datetime

from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()

# sometimes the server is sensitive to this information
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
#('Cookie', 'WEBTRENDS_ID=192.206.151.130.1371819178837082; __utma=228279554.616733573.1371840655.1376512182.1376579671.60; __utmz=228279554.1376579671.60.53.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=228279554; JSESSIONID=0000hjzNRrlpqmctOxyw30eQu19:162rr0mfu')]

STATUS = ""

WARD_LIST =["W01","W02","W03","W04","W05","W06","W07","N08","N09","N10","W11","W12","W13","S14","N15","N16","W17","S18","S19","S20","S21","S22","N23","N24","N25","N26","S27","S28","S29","S30","S31","S32","N33","N34","E35","E36","E37","E38","E39","E40","E41","E42","E43","E44"]

TEST_WARD_LIST = ["W01"]

def getNumberOfPages(soup):
    paras = soup.findAll("p")
    try:
        start = str(paras[1]).index( "of&nbsp;" ) + len( "of&nbsp;" )
        end = str(paras[1]).index( "</p>", start )
        numberOfPages = float(str(paras[1])[start:end]) / 5
        return int(math.ceil(numberOfPages))
    except ValueError:
        print "ERROR: GETTING # OF PAGES"
        return 0

def getAndSaveInvestigationDetails(table, MAIN_WARD):
    theDate = ""  
    issue = ""
    status= ""
    address= ""
    description = ""
    rows = table.findChildren(['tr'])
    cells = rows[4].findChildren(['td'])
    name = cells[1]

    try:
        start = str(name).index( ">" ) + len( ">" )
        end = str(name).index( "</td>", start )
        theDate = str(name)[start:end]
    except ValueError:
        print "ERROR: GETTING INVESTIGATION DATE"
        theDate = "N/A"

    cells = rows[9].findChildren(['td'])
    name = cells[1]

    #try:
    #    start = str(name).index( ">" ) + len( ">" )
    #    end = str(name).index( "</td>", start )
    #    issue = str(name)[start:end]
    #except ValueError:
    #    print "ERROR: GETTING INVESTIGATION ISSUE"
    #    issue = "N/A"

    #cells = rows[10].findChildren(['td'])
    #name = cells[1]

    #try:
    #    start = str(name).index( ">" ) + len( ">" )
    #    end = str(name).index( "</td>", start )
    #    status = str(name)[start:end]
    #except ValueError:
    #    print "ERROR: GETTING INVESTIGATION STATUS"
    #    status = "N/A"

    #cells = rows[11].findChildren(['td'])
    #name = cells[1]

    #try:
    #    start = str(name).index( ">" ) + len( ">" )
    #    end = str(name).index( "</td>", start )
    #    address = str(name)[start:end]
    #except ValueError:
    #    print "ERROR: GETTING INVESTIGATION ADDRESS"
    #    address = "N/A"

    #cells = rows[13].findChildren(['td'])
    #name = cells[1]

    #try:
    #    start = str(name).index( ">" ) + len( ">" )
    #    end = str(name).index( "</td>", start )
    #    description = str(name)[start:end]
    #except ValueError:
    #    print "ERROR: GETTING INVESTIGATION DESCRIPTION"
    #    description = "N/A"

    #scraperwiki.sqlite.execute("INSERT INTO investigations (ward,theDate,issue,status,description,address,city,province) VALUES (?,?,?,?,?,?,?,?)", (MAIN_WARD,theDate.lstrip().rstrip(),issue.lstrip().rstrip(),status.lstrip().rstrip(),description.lstrip().rstrip(),address.lstrip().rstrip(), "TORONTO", "ON"))
    #scraperwiki.sqlite.commit()
    print "INSERTING = "+ MAIN_WARD + " | " + address + " | " + theDate + " | " + issue + " | " + status + " | " + description


def scrapeDetailPage(soup, MAIN_WARD):
 
    for a in soup.findAll('a'):
        try:
            if str(a.get('name')) == 'top':
                print "*** NEW PAGE ***"
            elif 'details.do?folderRsn' in a['href']:
                url = 'http://app.toronto.ca/InvestigationActivity/details.do?folderRsn=' + a["href"][21:len(a["href"])]
                print "COMPLAINT DATA TO BE FOUND HERE: " + url
                try:
                    response = br.open(url)
                    html = response.read()
                    subPageSoup = BeautifulSoup(html)
                    tables = subPageSoup.findAll("table")
                    #getAndSaveInvestigationDetails(tables[6], MAIN_WARD) 
                except:
                    print "!!! ERROR ACCESSING SUBPAGE = " + url           

        except KeyError:
            holder = ""
            print "MAJOR ERROR - DATA NOT SAVED"

def run():
        
    for ward in TEST_WARD_LIST:

        MAIN_URL = 'http://app.toronto.ca/InvestigationActivity/search.do?house=&street=&streetType=&streetDirection=&region=&mapNumber=' + ward + '&inDateFromM=1&inDateFromD=1&inDateFromY=2013&inDateToM=' + str(datetime.datetime.today().month) + '&inDateToD=' + str(datetime.datetime.today().day) + '&inDateToY=2013&work=&status=' + STATUS + '&submit.x=20&submit.y=14'

        url = MAIN_URL

        print "PAGE TO SCRAPE: " + MAIN_URL

        # (1) CALL ONCE TO GET HOW MANY PAGES
        response = br.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        numberOfPages = getNumberOfPages(soup)
        print "NUMBER OF PAGES TO SCRAPE" + str(numberOfPages) 

        # (2) NOW LOOP THROUGH ALL PAGES
        #for i in range(1,numberOfPages+1):
        #    if i == 1:
        #        url = MAIN_URL
        #    else:
        #        url = 'http://app.toronto.ca/InvestigationActivity/navigate.do?method=next'
        #        br.addheaders = [('Referer', 'http://app.toronto.ca/InvestigationActivity/search.do'),('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
#('Cookie', 'WEBTRENDS_ID=192.206.151.130.1371819178837082; __utma=228279554.616733573.1371840655.1376597664.1376657600.62; __utmz=228279554.1376657600.62.55.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmb=228279554.3.10.1376657600; __utmc=228279554; JSESSIONID=0000hjzNRrlpqmctOxyw30eQu19:162rr0mfu')]

        #    try:       
        #        response = br.open(url)
        #        html = response.read()
        #        soup = BeautifulSoup(html)
        #        scrapeDetailPage(soup, ward)
        #    except:
        #        print "!!! ERROR ACCESSING LIST PAGE = " + url  

def createTables():
    scraperwiki.sqlite.execute("create table investigations (`ward` string, `theDate` text, `issue` text, `status` text, `description` text, `address` text, `city` text, `province` text)")

def dropTables():
    scraperwiki.sqlite.execute("drop table if exists investigations ")

def clear():
    dropTables()
    createTables()
    scraperwiki.sqlite.commit()

def runQueries():
    result = scraperwiki.sqlite.execute("select address, count(address) myTotal from investigations group by address order by myTotal desc limit 5")
    #result = scraperwiki.sqlite.execute("select description from investigations where ward='W06'and issue like '%Property Standards%'")
    print str(result)

#clear()
run()

