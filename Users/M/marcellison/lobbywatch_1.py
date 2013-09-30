import scraperwiki
import urllib2
import datetime
import calendar
import tweepy
import bitlyapi
import cgi
import os
import mechanize
import re
import math
import requests
import cookielib
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
('Cookie', 'WEBTRENDS_ID=24.85.235.62.1366084508173719; __utma=228279554.904766632.1366084790.1371783956.1372001511.32;__utmz=228279554.1372001511.32.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=228279554;JSESSIONID=0000-ZHqE1qkaotckl8jFr3RADa:15gm0ddj0')]

COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

TEST_COUNCILLOR_LIST = ["Adam+Vaughan","Kristyn+Wong-Tam"]

def getNumberOfPages(soup):
    pageNumbers = soup.findAll("div", { "id" : "pagination1" })
    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(pageNumbers).index( "&nbsp;[" ) + len( "&nbsp;[" )
        end = str(pageNumbers).index( "&nbsp;records]</div>]", start )
        numberOfPages = float(str(pageNumbers)[start:end]) / 10
        return int(math.ceil(numberOfPages))
    except ValueError:
        print "ERROR: GETTING # OF RECORDS"
        return 0


def scrapeDetailPage(soup, MAIN_POLITICIAN):
    
    for a in soup.findAll('a'):
        try:
            if str(a.get('name')) == 'top':
                print "*** NEW PAGE ***"
            elif 'doSubmit' in a['href']:
                url = 'http://app.toronto.ca/lobbyistsearch/subjectMatterDetails.do?undertakingFormId=' + a["href"][21:-2] + '&pageNum=none'
                response = br.open(url)

                html = response.read()
                subPageSoup = BeautifulSoup(html)
                tables = subPageSoup.findAll("table")
        
                lobbyistName = getLobbyistName(tables[5])  

                # CLIENT NAME CAN BE IN NUMEROUS PLACES! 
                if ">Client</td>" in str(tables[10]):
                    details = getLobbyistGROUPClientDetails(tables[11])
                else:
                    # need try/except as format diff depending on data on page!           
                    try:
                        details = getLobbyistClientDetails(tables[6])
                    except IndexError:                    
                        details = getLobbyistClientDetails(tables[7])
                
                index = details.find('|')
                clientName = details[0:index]
                clientType = details[index+1:len(details)]

                # need try/except as format diff depending on data on page!          
                try:
                    subjectMatter = getSubjectMatter(tables[8])
                except IndexError:                   
                    subjectMatter = getSubjectMatter(tables[9])
                try:
                    issue = getSubjectMatterIssue(tables[8])
                except IndexError:                   
                    issue = getSubjectMatterIssue(tables[9])           

                getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyistName, clientName, clientType, subjectMatter, issue)
    
        except KeyError:
            holder = ""
            print "MAJOR ERROR - DATA NOT SAVED"
        

def getLobbyistName(table):

    rows = table.findChildren(['tr'])
    cells = rows[7].findChildren(['td'])
    name = cells[2]

    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        return str(name)[start:end]
    except ValueError:
        #print "ERROR: GETTING LOBBYIST CLIENT"
        return ""

def getLobbyistClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])
    name = cells[2]
    bizType = cells[6]

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end]
        try:
            start = str(bizType).index( "<br />" ) + len( "<br />" )
            end = str(bizType).index( "</td>", start )
            details = details + "|" + str(bizType)[start:end]
        except ValueError:
            #print "ERROR: GETTING LOBBYIST TYPE"
            details = details + "|N/A"
            return details

    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getLobbyistGROUPClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[0].findChildren(['td'])
    name = cells[2]
    bizType = "N/A"

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end] + "|" + str(bizType)
    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getSubjectMatter(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])  
    matter = cells[2]

    try:
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]

    except ValueError:
        #print "ERROR: GETTING SUBJECT MATTER"
        cells = rows[0].findChildren(['td']) 
        matter = cells[2]
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]
        return details

    return details


def getSubjectMatterIssue(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[3].findChildren(['td']) 
    issue = cells[2]

    try:
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]

    except ValueError:
        #print "ERROR: GETTING ISSUE"
        cells = rows[2].findChildren(['td'])
        issue = cells[2]
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]
        return details

    return details

def getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyist, client, clientBusiness, subjectMatter, issue):

    lobbyist = lobbyist.lstrip().rstrip()
    client = client.lstrip().rstrip()
    client = client.replace('&amp;', 'and')
    client = client.replace("&#039;", "\'")
    clientBusiness = clientBusiness.lstrip().rstrip()    
    subjectMatter = subjectMatter.lstrip().rstrip()
    issue = issue.lstrip().rstrip()


    commDate = ""
    commType = ""
    MAIN_POLITICIAN = MAIN_POLITICIAN.replace('+', ' ')
    rows = tables[len(tables)-5].findChildren(['tr'])

    test = "false"

#    for row in rows:

 #       cells = row.findChildren('td')
 #       try:
 #           name = cells[4]
 #           if MAIN_POLITICIAN in str(name):
#                test = "true"

 #               try:
#                    start = str(cells[8]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[8]).index( "</font>", start )
#                    commDate = str(cells[8])[start:end]
#                    commDate = commDate.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING DATE"
#                    commDate = ""
                
#                try:
#                    start = str(cells[12]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[12]).index( "</font>", start )
#                    commType = str(cells[12])[start:end]
#                    commType = commType.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING TYPE"
#                    commType = ""

                #NEED TO DO INSERT AT THIS POINT - ONE ROW PER MEETING
                #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
                #scraperwiki.sqlite.commit()

                #print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate

#        except IndexError:  
#            something = ""

    # if for some reason we did not find table with comm details, still insert one row for councillor-lobbyist pairing
#    if test == "false":
        #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
        #scraperwiki.sqlite.commit()
#        print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate


    scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue) VALUES (?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue))
    scraperwiki.sqlite.commit()
    print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue

def run():
        
    for councillor in TEST_COUNCILLOR_LIST:

        MAIN_URL_PREFIX = 'http://app.toronto.ca/lobbyistsearch/search.do?searchBy=target&searchTerm1='
        MAIN_URL_POSTFIX = '&searchTerm2=&searchTerm3=Member+of+Council&publicOfficeType=Member+of+Council&&targetName='
        MAIN_URL_POSTFIX2 = 'programWardOrAgency=&pageNum='
        MAIN_PAGE_NUMBER = '0'

        url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + MAIN_PAGE_NUMBER

        # (1) CALL ONCE TO GET HOW MANY PAGES
        response = br.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        numberOfPages = getNumberOfPages(soup)

        # (2) NOW LOOP THROUGH ALL PAGES
        for i in range(1,numberOfPages+1):
            url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + str(i)
            #print "accessing = "+url
            response = br.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            scrapeDetailPage(soup, councillor)

def createTables():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text, `commDate` text, `commType` text)")

def createTables2():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text)")

def dropTables():

    scraperwiki.sqlite.execute("drop table if exists lobbying")

def clear():
    dropTables()
    #createTables()
    createTables2()
    scraperwiki.sqlite.commit()

#clear()    
#run()        

#scraperwiki.sqlite.execute("delete from lobbying where councillor in ('Karen Stintz','Michael Thompson')")
#scraperwiki.sqlite.commit()
#result = scraperwiki.sqlite.execute("select count(*) from lobbying where councillor = 'Karen Stintz'")
#print str(result)


result = scraperwiki.sqlite.execute("select * from lobbying where lobbyist like '%Adam J. Brown%'")
print str(result)




import scraperwiki
import urllib2
import datetime
import calendar
import tweepy
import bitlyapi
import cgi
import os
import mechanize
import re
import math
import requests
import cookielib
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
('Cookie', 'WEBTRENDS_ID=24.85.235.62.1366084508173719; __utma=228279554.904766632.1366084790.1371783956.1372001511.32;__utmz=228279554.1372001511.32.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=228279554;JSESSIONID=0000-ZHqE1qkaotckl8jFr3RADa:15gm0ddj0')]

COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

TEST_COUNCILLOR_LIST = ["Adam+Vaughan","Kristyn+Wong-Tam"]

def getNumberOfPages(soup):
    pageNumbers = soup.findAll("div", { "id" : "pagination1" })
    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(pageNumbers).index( "&nbsp;[" ) + len( "&nbsp;[" )
        end = str(pageNumbers).index( "&nbsp;records]</div>]", start )
        numberOfPages = float(str(pageNumbers)[start:end]) / 10
        return int(math.ceil(numberOfPages))
    except ValueError:
        print "ERROR: GETTING # OF RECORDS"
        return 0


def scrapeDetailPage(soup, MAIN_POLITICIAN):
    
    for a in soup.findAll('a'):
        try:
            if str(a.get('name')) == 'top':
                print "*** NEW PAGE ***"
            elif 'doSubmit' in a['href']:
                url = 'http://app.toronto.ca/lobbyistsearch/subjectMatterDetails.do?undertakingFormId=' + a["href"][21:-2] + '&pageNum=none'
                response = br.open(url)

                html = response.read()
                subPageSoup = BeautifulSoup(html)
                tables = subPageSoup.findAll("table")
        
                lobbyistName = getLobbyistName(tables[5])  

                # CLIENT NAME CAN BE IN NUMEROUS PLACES! 
                if ">Client</td>" in str(tables[10]):
                    details = getLobbyistGROUPClientDetails(tables[11])
                else:
                    # need try/except as format diff depending on data on page!           
                    try:
                        details = getLobbyistClientDetails(tables[6])
                    except IndexError:                    
                        details = getLobbyistClientDetails(tables[7])
                
                index = details.find('|')
                clientName = details[0:index]
                clientType = details[index+1:len(details)]

                # need try/except as format diff depending on data on page!          
                try:
                    subjectMatter = getSubjectMatter(tables[8])
                except IndexError:                   
                    subjectMatter = getSubjectMatter(tables[9])
                try:
                    issue = getSubjectMatterIssue(tables[8])
                except IndexError:                   
                    issue = getSubjectMatterIssue(tables[9])           

                getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyistName, clientName, clientType, subjectMatter, issue)
    
        except KeyError:
            holder = ""
            print "MAJOR ERROR - DATA NOT SAVED"
        

def getLobbyistName(table):

    rows = table.findChildren(['tr'])
    cells = rows[7].findChildren(['td'])
    name = cells[2]

    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        return str(name)[start:end]
    except ValueError:
        #print "ERROR: GETTING LOBBYIST CLIENT"
        return ""

def getLobbyistClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])
    name = cells[2]
    bizType = cells[6]

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end]
        try:
            start = str(bizType).index( "<br />" ) + len( "<br />" )
            end = str(bizType).index( "</td>", start )
            details = details + "|" + str(bizType)[start:end]
        except ValueError:
            #print "ERROR: GETTING LOBBYIST TYPE"
            details = details + "|N/A"
            return details

    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getLobbyistGROUPClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[0].findChildren(['td'])
    name = cells[2]
    bizType = "N/A"

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end] + "|" + str(bizType)
    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getSubjectMatter(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])  
    matter = cells[2]

    try:
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]

    except ValueError:
        #print "ERROR: GETTING SUBJECT MATTER"
        cells = rows[0].findChildren(['td']) 
        matter = cells[2]
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]
        return details

    return details


def getSubjectMatterIssue(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[3].findChildren(['td']) 
    issue = cells[2]

    try:
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]

    except ValueError:
        #print "ERROR: GETTING ISSUE"
        cells = rows[2].findChildren(['td'])
        issue = cells[2]
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]
        return details

    return details

def getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyist, client, clientBusiness, subjectMatter, issue):

    lobbyist = lobbyist.lstrip().rstrip()
    client = client.lstrip().rstrip()
    client = client.replace('&amp;', 'and')
    client = client.replace("&#039;", "\'")
    clientBusiness = clientBusiness.lstrip().rstrip()    
    subjectMatter = subjectMatter.lstrip().rstrip()
    issue = issue.lstrip().rstrip()


    commDate = ""
    commType = ""
    MAIN_POLITICIAN = MAIN_POLITICIAN.replace('+', ' ')
    rows = tables[len(tables)-5].findChildren(['tr'])

    test = "false"

#    for row in rows:

 #       cells = row.findChildren('td')
 #       try:
 #           name = cells[4]
 #           if MAIN_POLITICIAN in str(name):
#                test = "true"

 #               try:
#                    start = str(cells[8]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[8]).index( "</font>", start )
#                    commDate = str(cells[8])[start:end]
#                    commDate = commDate.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING DATE"
#                    commDate = ""
                
#                try:
#                    start = str(cells[12]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[12]).index( "</font>", start )
#                    commType = str(cells[12])[start:end]
#                    commType = commType.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING TYPE"
#                    commType = ""

                #NEED TO DO INSERT AT THIS POINT - ONE ROW PER MEETING
                #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
                #scraperwiki.sqlite.commit()

                #print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate

#        except IndexError:  
#            something = ""

    # if for some reason we did not find table with comm details, still insert one row for councillor-lobbyist pairing
#    if test == "false":
        #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
        #scraperwiki.sqlite.commit()
#        print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate


    scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue) VALUES (?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue))
    scraperwiki.sqlite.commit()
    print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue

def run():
        
    for councillor in TEST_COUNCILLOR_LIST:

        MAIN_URL_PREFIX = 'http://app.toronto.ca/lobbyistsearch/search.do?searchBy=target&searchTerm1='
        MAIN_URL_POSTFIX = '&searchTerm2=&searchTerm3=Member+of+Council&publicOfficeType=Member+of+Council&&targetName='
        MAIN_URL_POSTFIX2 = 'programWardOrAgency=&pageNum='
        MAIN_PAGE_NUMBER = '0'

        url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + MAIN_PAGE_NUMBER

        # (1) CALL ONCE TO GET HOW MANY PAGES
        response = br.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        numberOfPages = getNumberOfPages(soup)

        # (2) NOW LOOP THROUGH ALL PAGES
        for i in range(1,numberOfPages+1):
            url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + str(i)
            #print "accessing = "+url
            response = br.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            scrapeDetailPage(soup, councillor)

def createTables():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text, `commDate` text, `commType` text)")

def createTables2():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text)")

def dropTables():

    scraperwiki.sqlite.execute("drop table if exists lobbying")

def clear():
    dropTables()
    #createTables()
    createTables2()
    scraperwiki.sqlite.commit()

#clear()    
#run()        

#scraperwiki.sqlite.execute("delete from lobbying where councillor in ('Karen Stintz','Michael Thompson')")
#scraperwiki.sqlite.commit()
#result = scraperwiki.sqlite.execute("select count(*) from lobbying where councillor = 'Karen Stintz'")
#print str(result)


result = scraperwiki.sqlite.execute("select * from lobbying where lobbyist like '%Adam J. Brown%'")
print str(result)




import scraperwiki
import urllib2
import datetime
import calendar
import tweepy
import bitlyapi
import cgi
import os
import mechanize
import re
import math
import requests
import cookielib
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
('Cookie', 'WEBTRENDS_ID=24.85.235.62.1366084508173719; __utma=228279554.904766632.1366084790.1371783956.1372001511.32;__utmz=228279554.1372001511.32.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=228279554;JSESSIONID=0000-ZHqE1qkaotckl8jFr3RADa:15gm0ddj0')]

COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

TEST_COUNCILLOR_LIST = ["Adam+Vaughan","Kristyn+Wong-Tam"]

def getNumberOfPages(soup):
    pageNumbers = soup.findAll("div", { "id" : "pagination1" })
    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(pageNumbers).index( "&nbsp;[" ) + len( "&nbsp;[" )
        end = str(pageNumbers).index( "&nbsp;records]</div>]", start )
        numberOfPages = float(str(pageNumbers)[start:end]) / 10
        return int(math.ceil(numberOfPages))
    except ValueError:
        print "ERROR: GETTING # OF RECORDS"
        return 0


def scrapeDetailPage(soup, MAIN_POLITICIAN):
    
    for a in soup.findAll('a'):
        try:
            if str(a.get('name')) == 'top':
                print "*** NEW PAGE ***"
            elif 'doSubmit' in a['href']:
                url = 'http://app.toronto.ca/lobbyistsearch/subjectMatterDetails.do?undertakingFormId=' + a["href"][21:-2] + '&pageNum=none'
                response = br.open(url)

                html = response.read()
                subPageSoup = BeautifulSoup(html)
                tables = subPageSoup.findAll("table")
        
                lobbyistName = getLobbyistName(tables[5])  

                # CLIENT NAME CAN BE IN NUMEROUS PLACES! 
                if ">Client</td>" in str(tables[10]):
                    details = getLobbyistGROUPClientDetails(tables[11])
                else:
                    # need try/except as format diff depending on data on page!           
                    try:
                        details = getLobbyistClientDetails(tables[6])
                    except IndexError:                    
                        details = getLobbyistClientDetails(tables[7])
                
                index = details.find('|')
                clientName = details[0:index]
                clientType = details[index+1:len(details)]

                # need try/except as format diff depending on data on page!          
                try:
                    subjectMatter = getSubjectMatter(tables[8])
                except IndexError:                   
                    subjectMatter = getSubjectMatter(tables[9])
                try:
                    issue = getSubjectMatterIssue(tables[8])
                except IndexError:                   
                    issue = getSubjectMatterIssue(tables[9])           

                getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyistName, clientName, clientType, subjectMatter, issue)
    
        except KeyError:
            holder = ""
            print "MAJOR ERROR - DATA NOT SAVED"
        

def getLobbyistName(table):

    rows = table.findChildren(['tr'])
    cells = rows[7].findChildren(['td'])
    name = cells[2]

    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        return str(name)[start:end]
    except ValueError:
        #print "ERROR: GETTING LOBBYIST CLIENT"
        return ""

def getLobbyistClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])
    name = cells[2]
    bizType = cells[6]

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end]
        try:
            start = str(bizType).index( "<br />" ) + len( "<br />" )
            end = str(bizType).index( "</td>", start )
            details = details + "|" + str(bizType)[start:end]
        except ValueError:
            #print "ERROR: GETTING LOBBYIST TYPE"
            details = details + "|N/A"
            return details

    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getLobbyistGROUPClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[0].findChildren(['td'])
    name = cells[2]
    bizType = "N/A"

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end] + "|" + str(bizType)
    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getSubjectMatter(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])  
    matter = cells[2]

    try:
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]

    except ValueError:
        #print "ERROR: GETTING SUBJECT MATTER"
        cells = rows[0].findChildren(['td']) 
        matter = cells[2]
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]
        return details

    return details


def getSubjectMatterIssue(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[3].findChildren(['td']) 
    issue = cells[2]

    try:
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]

    except ValueError:
        #print "ERROR: GETTING ISSUE"
        cells = rows[2].findChildren(['td'])
        issue = cells[2]
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]
        return details

    return details

def getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyist, client, clientBusiness, subjectMatter, issue):

    lobbyist = lobbyist.lstrip().rstrip()
    client = client.lstrip().rstrip()
    client = client.replace('&amp;', 'and')
    client = client.replace("&#039;", "\'")
    clientBusiness = clientBusiness.lstrip().rstrip()    
    subjectMatter = subjectMatter.lstrip().rstrip()
    issue = issue.lstrip().rstrip()


    commDate = ""
    commType = ""
    MAIN_POLITICIAN = MAIN_POLITICIAN.replace('+', ' ')
    rows = tables[len(tables)-5].findChildren(['tr'])

    test = "false"

#    for row in rows:

 #       cells = row.findChildren('td')
 #       try:
 #           name = cells[4]
 #           if MAIN_POLITICIAN in str(name):
#                test = "true"

 #               try:
#                    start = str(cells[8]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[8]).index( "</font>", start )
#                    commDate = str(cells[8])[start:end]
#                    commDate = commDate.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING DATE"
#                    commDate = ""
                
#                try:
#                    start = str(cells[12]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[12]).index( "</font>", start )
#                    commType = str(cells[12])[start:end]
#                    commType = commType.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING TYPE"
#                    commType = ""

                #NEED TO DO INSERT AT THIS POINT - ONE ROW PER MEETING
                #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
                #scraperwiki.sqlite.commit()

                #print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate

#        except IndexError:  
#            something = ""

    # if for some reason we did not find table with comm details, still insert one row for councillor-lobbyist pairing
#    if test == "false":
        #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
        #scraperwiki.sqlite.commit()
#        print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate


    scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue) VALUES (?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue))
    scraperwiki.sqlite.commit()
    print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue

def run():
        
    for councillor in TEST_COUNCILLOR_LIST:

        MAIN_URL_PREFIX = 'http://app.toronto.ca/lobbyistsearch/search.do?searchBy=target&searchTerm1='
        MAIN_URL_POSTFIX = '&searchTerm2=&searchTerm3=Member+of+Council&publicOfficeType=Member+of+Council&&targetName='
        MAIN_URL_POSTFIX2 = 'programWardOrAgency=&pageNum='
        MAIN_PAGE_NUMBER = '0'

        url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + MAIN_PAGE_NUMBER

        # (1) CALL ONCE TO GET HOW MANY PAGES
        response = br.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        numberOfPages = getNumberOfPages(soup)

        # (2) NOW LOOP THROUGH ALL PAGES
        for i in range(1,numberOfPages+1):
            url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + str(i)
            #print "accessing = "+url
            response = br.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            scrapeDetailPage(soup, councillor)

def createTables():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text, `commDate` text, `commType` text)")

def createTables2():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text)")

def dropTables():

    scraperwiki.sqlite.execute("drop table if exists lobbying")

def clear():
    dropTables()
    #createTables()
    createTables2()
    scraperwiki.sqlite.commit()

#clear()    
#run()        

#scraperwiki.sqlite.execute("delete from lobbying where councillor in ('Karen Stintz','Michael Thompson')")
#scraperwiki.sqlite.commit()
#result = scraperwiki.sqlite.execute("select count(*) from lobbying where councillor = 'Karen Stintz'")
#print str(result)


result = scraperwiki.sqlite.execute("select * from lobbying where lobbyist like '%Adam J. Brown%'")
print str(result)




import scraperwiki
import urllib2
import datetime
import calendar
import tweepy
import bitlyapi
import cgi
import os
import mechanize
import re
import math
import requests
import cookielib
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
('Cookie', 'WEBTRENDS_ID=24.85.235.62.1366084508173719; __utma=228279554.904766632.1366084790.1371783956.1372001511.32;__utmz=228279554.1372001511.32.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=228279554;JSESSIONID=0000BJsgHkmLtrOWiDpwEZqxkVb:15gm0e16a')]

COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

TEST_COUNCILLOR_LIST = ["Adam+Vaughan","Kristyn+Wong-Tam"]

def getNumberOfPages(soup):
    pageNumbers = soup.findAll("div", { "id" : "pagination1" })
    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(pageNumbers).index( "&nbsp;[" ) + len( "&nbsp;[" )
        end = str(pageNumbers).index( "&nbsp;records]</div>]", start )
        numberOfPages = float(str(pageNumbers)[start:end]) / 10
        return int(math.ceil(numberOfPages))
    except ValueError:
        print "ERROR: GETTING # OF RECORDS"
        return 0


def scrapeDetailPage(soup, MAIN_POLITICIAN):
    
    for a in soup.findAll('a'):
        try:
            if str(a.get('name')) == 'top':
                print "*** NEW PAGE ***"
            elif 'doSubmit' in a['href']:
                url = 'http://app.toronto.ca/lobbyistsearch/subjectMatterDetails.do?undertakingFormId=' + a["href"][21:-2] + '&pageNum=none'
                response = br.open(url)

                html = response.read()
                subPageSoup = BeautifulSoup(html)
                tables = subPageSoup.findAll("table")
        
                lobbyistName = getLobbyistName(tables[5])  

                # CLIENT NAME CAN BE IN NUMEROUS PLACES! 
                if ">Client</td>" in str(tables[10]):
                    details = getLobbyistGROUPClientDetails(tables[11])
                else:
                    # need try/except as format diff depending on data on page!           
                    try:
                        details = getLobbyistClientDetails(tables[6])
                    except IndexError:                    
                        details = getLobbyistClientDetails(tables[7])
                
                index = details.find('|')
                clientName = details[0:index]
                clientType = details[index+1:len(details)]

                # need try/except as format diff depending on data on page!          
                try:
                    subjectMatter = getSubjectMatter(tables[8])
                except IndexError:                   
                    subjectMatter = getSubjectMatter(tables[9])
                try:
                    issue = getSubjectMatterIssue(tables[8])
                except IndexError:                   
                    issue = getSubjectMatterIssue(tables[9])           

                getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyistName, clientName, clientType, subjectMatter, issue)
    
        except KeyError:
            holder = ""
            print "MAJOR ERROR - DATA NOT SAVED"
        

def getLobbyistName(table):

    rows = table.findChildren(['tr'])
    cells = rows[7].findChildren(['td'])
    name = cells[2]

    try:
        # data is in this format:  <br />Mr Graham Henderson</td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        return str(name)[start:end]
    except ValueError:
        #print "ERROR: GETTING LOBBYIST CLIENT"
        return ""

def getLobbyistClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])
    name = cells[2]
    bizType = cells[6]

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end]
        try:
            start = str(bizType).index( "<br />" ) + len( "<br />" )
            end = str(bizType).index( "</td>", start )
            details = details + "|" + str(bizType)[start:end]
        except ValueError:
            #print "ERROR: GETTING LOBBYIST TYPE"
            details = details + "|N/A"
            return details

    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getLobbyistGROUPClientDetails(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[0].findChildren(['td'])
    name = cells[2]
    bizType = "N/A"

    try:
        # data is in this format:  <br />Northcliffe Group Inc. </td>
        start = str(name).index( "<br />" ) + len( "<br />" )
        end = str(name).index( "</td>", start )
        details = str(name)[start:end] + "|" + str(bizType)
    except ValueError:
        #print "ERROR: GETTING LOBBYIST DETAILS"
        return details

    return details

def getSubjectMatter(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[1].findChildren(['td'])  
    matter = cells[2]

    try:
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]

    except ValueError:
        #print "ERROR: GETTING SUBJECT MATTER"
        cells = rows[0].findChildren(['td']) 
        matter = cells[2]
        start = str(matter).index( "<br />" ) + len( "<br />" )
        end = str(matter).index( "</td>", start )
        details = str(matter)[start:end]
        return details

    return details


def getSubjectMatterIssue(table):

    details = ""
    rows = table.findChildren(['tr'])
    cells = rows[3].findChildren(['td']) 
    issue = cells[2]

    try:
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]

    except ValueError:
        #print "ERROR: GETTING ISSUE"
        cells = rows[2].findChildren(['td'])
        issue = cells[2]
        start = str(issue).index( "<br />" ) + len( "<br />" )
        end = str(issue).index( "</td>", start )
        details = str(issue)[start:end]
        return details

    return details

def getMeetingDetailsAndSave(tables, MAIN_POLITICIAN, lobbyist, client, clientBusiness, subjectMatter, issue):

    lobbyist = lobbyist.lstrip().rstrip()
    client = client.lstrip().rstrip()
    client = client.replace('&amp;', 'and')
    client = client.replace("&#039;", "\'")
    clientBusiness = clientBusiness.lstrip().rstrip()    
    subjectMatter = subjectMatter.lstrip().rstrip()
    issue = issue.lstrip().rstrip()


    commDate = ""
    commType = ""
    MAIN_POLITICIAN = MAIN_POLITICIAN.replace('+', ' ')
    rows = tables[len(tables)-5].findChildren(['tr'])

    test = "false"

#    for row in rows:

 #       cells = row.findChildren('td')
 #       try:
 #           name = cells[4]
 #           if MAIN_POLITICIAN in str(name):
#                test = "true"

 #               try:
#                    start = str(cells[8]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[8]).index( "</font>", start )
#                    commDate = str(cells[8])[start:end]
#                    commDate = commDate.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING DATE"
#                    commDate = ""
                
#                try:
#                    start = str(cells[12]).index( '<font size="1">' ) + len( '<font size="1">' )
#                    end = str(cells[12]).index( "</font>", start )
#                    commType = str(cells[12])[start:end]
#                    commType = commType.lstrip().rstrip()
#                except IndexError:
#                    print "ERROR RETRIEVING MEETING TYPE"
#                    commType = ""

                #NEED TO DO INSERT AT THIS POINT - ONE ROW PER MEETING
                #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
                #scraperwiki.sqlite.commit()

                #print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate

#        except IndexError:  
#            something = ""

    # if for some reason we did not find table with comm details, still insert one row for councillor-lobbyist pairing
#    if test == "false":
        #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue,commDate,commType) VALUES (?,?,?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue,commDate, commType))
        #scraperwiki.sqlite.commit()
#        print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue+ " | " + commType + " | " + commDate


    #scraperwiki.sqlite.execute("INSERT INTO lobbying (councillor,lobbyist,client,clientBusiness,subjectMatter,issue) VALUES (?,?,?,?,?,?)", (MAIN_POLITICIAN,lobbyist,client, clientBusiness, subjectMatter, issue))
    #scraperwiki.sqlite.commit()
    print "INSERTING = "+ MAIN_POLITICIAN + " | " + lobbyist+ " | " + client+ " | " + clientBusiness+ " | " + subjectMatter+ " | " + issue

def run():
        
    for councillor in TEST_COUNCILLOR_LIST:

        MAIN_URL_PREFIX = 'http://app.toronto.ca/lobbyistsearch/search.do?searchBy=target&searchTerm1='
        MAIN_URL_POSTFIX = '&searchTerm2=&searchTerm3=Member+of+Council&publicOfficeType=Member+of+Council&&targetName='
        MAIN_URL_POSTFIX2 = 'programWardOrAgency=&pageNum='
        MAIN_PAGE_NUMBER = '0'

        url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + MAIN_PAGE_NUMBER

        # (1) CALL ONCE TO GET HOW MANY PAGES
        response = br.open(url)
        html = response.read()
        soup = BeautifulSoup(html)
        numberOfPages = getNumberOfPages(soup)

        # (2) NOW LOOP THROUGH ALL PAGES
        for i in range(1,numberOfPages+1):
            url = MAIN_URL_PREFIX + councillor + MAIN_URL_POSTFIX + councillor + MAIN_URL_POSTFIX2 + str(i)
            #print "accessing = "+url
            response = br.open(url)
            html = response.read()
            soup = BeautifulSoup(html)
            scrapeDetailPage(soup, councillor)

def createTables():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text, `commDate` text, `commType` text)")

def createTables2():
    scraperwiki.sqlite.execute("create table lobbying (`councillor` string, `lobbyist` text, `client` text, `clientBusiness` text, `subjectMatter` text, `issue` text)")

def dropTables():

    scraperwiki.sqlite.execute("drop table if exists lobbying")

def clear():
    dropTables()
    #createTables()
    createTables2()
    scraperwiki.sqlite.commit()

#clear()    
run()        

#scraperwiki.sqlite.execute("delete from lobbying where councillor in ('Karen Stintz','Michael Thompson')")
#scraperwiki.sqlite.commit()
#result = scraperwiki.sqlite.execute("select count(*) from lobbying where councillor = 'Karen Stintz'")
#print str(result)


#result = scraperwiki.sqlite.execute("select * from lobbying where lobbyist like '%Adam J. Brown%'")
#print str(result)




