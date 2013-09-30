##########################################################################
# this is a practice scraper- there may be easier ways to get this info  #
# and neater ways to do it!                                              #
##########################################################################

import scraperwiki
import lxml.html
import dateutil.parser
from datetime import datetime

# with hindsight, might have been better to write urls to SQL then record when scraped- better for restarting after errors

# Borrowed this from another scraper
def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 



def build_url_list(startpage,maxpage):

#Builds a list of urls of scrapers based from each summary page.
#May be a better way to go from page 1 through all pages but this way is handy for testing

    #loop through each page in turn finding links to scraper detail pages. Put in one big list
    urllist = []
    for pageno in range(startpage,maxpage):
        pageurl= "https://scraperwiki.com/browse/scrapers/?page="+str(pageno)

        root = fetch_html(pageurl)
#        html = scraperwiki.scrape(pageurl)
#        root = lxml.html.fromstring(html)
        print pageurl

        #get the page link (not the _edit one)
        for a in root.cssselect("li.code_object_line"):
            hrefs = a.cssselect("a")
            #print hrefs

            if len(hrefs) >0:
                urllist.append(hrefs[1].get('href'))
    print urllist
    return urllist

#print build_url_list(3)

#on each scraper page, loop through fields
#PARAM IS START PAGE and MAX PAGE REQUIRED + 1
#seems to have halted without error, fill in missing pages
for scraper in build_url_list(353,532):

    scraperurl = "https://scraperwiki.com" + scraper
    #print scraperurl

    #ditionary to store info for each scraper
    scraperinfo = {'Scraper URL' : "",
                    'User Name'  : "",
                    'Scraper Name' : "",
                    'Forked Scraper Name' : "",
                    'Forked Scraper User' : "",
                    'Desc Present Flag' : "",
                    'No of Contributors' : 0,
                    'Language Used' : "",
                    'Source' : "",
                    'Schedule' : "",
                    'Protection Status' : "",
                    'Scraper Create Date' : ""}

    root2 = fetch_html(scraperurl)

#    html2 = scraperwiki.scrape(scraperurl)
#    root2 = lxml.html.fromstring(html2)


    #find long user name and scraper name

    userlame = ""
    scraperlname = ""

    for el in root2.cssselect("div#header h2"):

        ela = el.cssselect("a")    #user long name
        elem = el.cssselect("em")    #scraper long name

        userlame = ela[0].text_content()
        scraperlname = elem[0].text_content()

        scraperinfo['Scraper URL'] = scraperurl

        #print "usrnm", userlame 
        #print "scrprnm", scraperlname

    
    #If scraper was forked, find name and user of forked scraper

    forked_user = ""
    forked_scraper = ""
    
    for el in root2.cssselect("div.forked_from li"):

        ela = el.cssselect("a")

        forked_user = ela[0].text_content()
        forked_scraper = ela[1].text_content()

        #print "f-user", forked_user 
        #print "f-scraper", forked_scraper 


    #Check if scraper have a description- could pick up description too but only record presence for now

    descflag =""

    for el in root2.cssselect("div#divAboutScraper p"):

        desc = el.text_content()
        desc2 = desc.strip()

        if "This scraper has no description" in desc2:
            descflag = "N"
        else:
            descflag = "Y"

        #print "descflag", descflag


    #get a list of all contributors- does this only contain unique values?
    #for now only record number of contributors to db

    contributors = []
    contr_count = 0

    for el in root2.cssselect("div#contributors ul"):

        elsp = el.cssselect("span")

        for contr in range(len(elsp)):
            contributors.append(elsp[contr].text_content())

    contr_count = len(contributors)
    #print "No. of contributors:", contr_count
    #print "contributors:",contributors


    #find header info: language, source, schedule, status
    langused = ""
    source = ""
    sched = ""
    status = ""
    
    for el in root2.cssselect("div#header p"):

        elsp = el.cssselect("span")

        langused = elsp[0].text_content()
        source = elsp[1].text_content()
        sched = elsp[2].text_content()
        status = elsp[3].text_content()

        #print "lang", langused 
        #print "source", source 
        #print "sched", sched 
        #print "status", status 

        #0- language 1-source 2-schedule 3-public/prot - is this always true, will all be present?


    #this picks up editor name and date, but for now only interested in first edit date

    history = []
    create_date = "01-01-1900"

    for el in root2.cssselect("span.history_editor_info"):

        ela = el.cssselect("a")    #editor's username
        elsp = el.cssselect("span.history_date")    #edit date

        history.append(dateutil.parser.parse(elsp[0].text_content()))

    createdate = min(history)

    #print createdate.date()

    scraperinfo['User Name'] = userlame
    scraperinfo['Scraper Name'] = scraperlname
    scraperinfo['Forked Scraper Name'] = forked_scraper
    scraperinfo['Forked Scraper User'] = forked_user
    scraperinfo['Desc Present Flag'] = descflag
    scraperinfo['No of Contributors'] = contr_count
    scraperinfo['Language Used'] = langused
    scraperinfo['Source'] = source
    scraperinfo['Schedule'] = sched
    scraperinfo['Protection Status'] = status
    scraperinfo['Scraper Create Date'] = createdate.date()
    scraperinfo['Record Create Date'] = datetime.now()

    try:
        scraperwiki.sqlite.save(unique_keys=['Scraper Name'], data=scraperinfo)
    except:
        print "Failed on: %s - %s --> " % (scraperurl, scraperinfo['Scraper Create Date'])




##########################################################################
# this is a practice scraper- there may be easier ways to get this info  #
# and neater ways to do it!                                              #
##########################################################################

import scraperwiki
import lxml.html
import dateutil.parser
from datetime import datetime

# with hindsight, might have been better to write urls to SQL then record when scraped- better for restarting after errors

# Borrowed this from another scraper
def fetch_html(url):
    try:
        html = scraperwiki.scrape(url)
        return lxml.html.fromstring(html)
    except:
        try:
            html = scraperwiki.scrape(url)
            return lxml.html.fromstring(html)
        except:
            pass
        print "Failed to fetch url: " + url
    return 



def build_url_list(startpage,maxpage):

#Builds a list of urls of scrapers based from each summary page.
#May be a better way to go from page 1 through all pages but this way is handy for testing

    #loop through each page in turn finding links to scraper detail pages. Put in one big list
    urllist = []
    for pageno in range(startpage,maxpage):
        pageurl= "https://scraperwiki.com/browse/scrapers/?page="+str(pageno)

        root = fetch_html(pageurl)
#        html = scraperwiki.scrape(pageurl)
#        root = lxml.html.fromstring(html)
        print pageurl

        #get the page link (not the _edit one)
        for a in root.cssselect("li.code_object_line"):
            hrefs = a.cssselect("a")
            #print hrefs

            if len(hrefs) >0:
                urllist.append(hrefs[1].get('href'))
    print urllist
    return urllist

#print build_url_list(3)

#on each scraper page, loop through fields
#PARAM IS START PAGE and MAX PAGE REQUIRED + 1
#seems to have halted without error, fill in missing pages
for scraper in build_url_list(353,532):

    scraperurl = "https://scraperwiki.com" + scraper
    #print scraperurl

    #ditionary to store info for each scraper
    scraperinfo = {'Scraper URL' : "",
                    'User Name'  : "",
                    'Scraper Name' : "",
                    'Forked Scraper Name' : "",
                    'Forked Scraper User' : "",
                    'Desc Present Flag' : "",
                    'No of Contributors' : 0,
                    'Language Used' : "",
                    'Source' : "",
                    'Schedule' : "",
                    'Protection Status' : "",
                    'Scraper Create Date' : ""}

    root2 = fetch_html(scraperurl)

#    html2 = scraperwiki.scrape(scraperurl)
#    root2 = lxml.html.fromstring(html2)


    #find long user name and scraper name

    userlame = ""
    scraperlname = ""

    for el in root2.cssselect("div#header h2"):

        ela = el.cssselect("a")    #user long name
        elem = el.cssselect("em")    #scraper long name

        userlame = ela[0].text_content()
        scraperlname = elem[0].text_content()

        scraperinfo['Scraper URL'] = scraperurl

        #print "usrnm", userlame 
        #print "scrprnm", scraperlname

    
    #If scraper was forked, find name and user of forked scraper

    forked_user = ""
    forked_scraper = ""
    
    for el in root2.cssselect("div.forked_from li"):

        ela = el.cssselect("a")

        forked_user = ela[0].text_content()
        forked_scraper = ela[1].text_content()

        #print "f-user", forked_user 
        #print "f-scraper", forked_scraper 


    #Check if scraper have a description- could pick up description too but only record presence for now

    descflag =""

    for el in root2.cssselect("div#divAboutScraper p"):

        desc = el.text_content()
        desc2 = desc.strip()

        if "This scraper has no description" in desc2:
            descflag = "N"
        else:
            descflag = "Y"

        #print "descflag", descflag


    #get a list of all contributors- does this only contain unique values?
    #for now only record number of contributors to db

    contributors = []
    contr_count = 0

    for el in root2.cssselect("div#contributors ul"):

        elsp = el.cssselect("span")

        for contr in range(len(elsp)):
            contributors.append(elsp[contr].text_content())

    contr_count = len(contributors)
    #print "No. of contributors:", contr_count
    #print "contributors:",contributors


    #find header info: language, source, schedule, status
    langused = ""
    source = ""
    sched = ""
    status = ""
    
    for el in root2.cssselect("div#header p"):

        elsp = el.cssselect("span")

        langused = elsp[0].text_content()
        source = elsp[1].text_content()
        sched = elsp[2].text_content()
        status = elsp[3].text_content()

        #print "lang", langused 
        #print "source", source 
        #print "sched", sched 
        #print "status", status 

        #0- language 1-source 2-schedule 3-public/prot - is this always true, will all be present?


    #this picks up editor name and date, but for now only interested in first edit date

    history = []
    create_date = "01-01-1900"

    for el in root2.cssselect("span.history_editor_info"):

        ela = el.cssselect("a")    #editor's username
        elsp = el.cssselect("span.history_date")    #edit date

        history.append(dateutil.parser.parse(elsp[0].text_content()))

    createdate = min(history)

    #print createdate.date()

    scraperinfo['User Name'] = userlame
    scraperinfo['Scraper Name'] = scraperlname
    scraperinfo['Forked Scraper Name'] = forked_scraper
    scraperinfo['Forked Scraper User'] = forked_user
    scraperinfo['Desc Present Flag'] = descflag
    scraperinfo['No of Contributors'] = contr_count
    scraperinfo['Language Used'] = langused
    scraperinfo['Source'] = source
    scraperinfo['Schedule'] = sched
    scraperinfo['Protection Status'] = status
    scraperinfo['Scraper Create Date'] = createdate.date()
    scraperinfo['Record Create Date'] = datetime.now()

    try:
        scraperwiki.sqlite.save(unique_keys=['Scraper Name'], data=scraperinfo)
    except:
        print "Failed on: %s - %s --> " % (scraperurl, scraperinfo['Scraper Create Date'])




