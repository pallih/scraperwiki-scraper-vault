import scraperwiki, lxml.html, itertools, datetime

host = "http://europa.eu/whoiswho/public/index.cfm?fuseaction=idea.hierarchy"

"""
IF <h2>Depending entity</h2> THEN further levels below

"""
def parsePage(pageRoot):
    submissions = pageRoot.find_class("color")
    """
    In the "result-top" class we have what we need: the URL to the
    submission page (not the app page!) and the name of the app.

    <div class="result-top">
        <a href="..." title="...">
    [...]
    </div>

    """
    for app in submissions :
        appInfo = ((app.find_class("color")[1]).cssselect("h3"))
        print appInfo
        #appTitle = appInfo[0].get("title")
        #appInfo = ((app.find_class("result-top")[0]).cssselect("a"))
        #appUrl = appInfo[0].get("href")
        #appTitle = appInfo[0].get("title")
        print "Found app: " + appTitle
        #Now we need the app info in the app page.
        #subPage = lxml.html.fromstring(scraperwiki.scrape(host + appUrl))
        #appInfo = subPage.find_class("text")[0].text_content()
        #Save in DB
        #record = {
                 #'Name' : appTitle ,
                 #'Url' : appUrl,
                 #'Descr' : appInfo
                 #}
        #scraperwiki.sqlite.save(unique_keys=['Name', 'Url'], data=record)

"""
http://europa.eu/whoiswho/public/index.cfm?fuseaction=idea.hierarchy&nodeID=371070&personID=153028&lang=en
"""
nodeID = 371070
personID = 153028
pageUrl = "&nodeID=371070&personID=153028&lang=en"
print "Connecting to: " + host+pageUrl

page = lxml.html.fromstring(scraperwiki.scrape(host+pageUrl))
#Parse first page.
pageNumber = 1
parsePage(page)
#Go to other pages.
next = (page.find_class("pagination"))[0].find_class("next_page")
while(next[0].get("href") is not None) :#While there are other next pages.
    #Connect to page.
    pageUrl = next[0].get("href")
    page = lxml.html.fromstring(scraperwiki.scrape(host + pageUrl))
    print "Connecting to: " + host+pageUrl
    #Parse it.
    pageNumber += 1
    parsePage(page)
    #Next page.
    next = (page.find_class("pagination"))[0].find_class("next_page")
print "Pages: " + str(pageNumber)
import scraperwiki, lxml.html, itertools, datetime

host = "http://europa.eu/whoiswho/public/index.cfm?fuseaction=idea.hierarchy"

"""
IF <h2>Depending entity</h2> THEN further levels below

"""
def parsePage(pageRoot):
    submissions = pageRoot.find_class("color")
    """
    In the "result-top" class we have what we need: the URL to the
    submission page (not the app page!) and the name of the app.

    <div class="result-top">
        <a href="..." title="...">
    [...]
    </div>

    """
    for app in submissions :
        appInfo = ((app.find_class("color")[1]).cssselect("h3"))
        print appInfo
        #appTitle = appInfo[0].get("title")
        #appInfo = ((app.find_class("result-top")[0]).cssselect("a"))
        #appUrl = appInfo[0].get("href")
        #appTitle = appInfo[0].get("title")
        print "Found app: " + appTitle
        #Now we need the app info in the app page.
        #subPage = lxml.html.fromstring(scraperwiki.scrape(host + appUrl))
        #appInfo = subPage.find_class("text")[0].text_content()
        #Save in DB
        #record = {
                 #'Name' : appTitle ,
                 #'Url' : appUrl,
                 #'Descr' : appInfo
                 #}
        #scraperwiki.sqlite.save(unique_keys=['Name', 'Url'], data=record)

"""
http://europa.eu/whoiswho/public/index.cfm?fuseaction=idea.hierarchy&nodeID=371070&personID=153028&lang=en
"""
nodeID = 371070
personID = 153028
pageUrl = "&nodeID=371070&personID=153028&lang=en"
print "Connecting to: " + host+pageUrl

page = lxml.html.fromstring(scraperwiki.scrape(host+pageUrl))
#Parse first page.
pageNumber = 1
parsePage(page)
#Go to other pages.
next = (page.find_class("pagination"))[0].find_class("next_page")
while(next[0].get("href") is not None) :#While there are other next pages.
    #Connect to page.
    pageUrl = next[0].get("href")
    page = lxml.html.fromstring(scraperwiki.scrape(host + pageUrl))
    print "Connecting to: " + host+pageUrl
    #Parse it.
    pageNumber += 1
    parsePage(page)
    #Next page.
    next = (page.find_class("pagination"))[0].find_class("next_page")
print "Pages: " + str(pageNumber)
