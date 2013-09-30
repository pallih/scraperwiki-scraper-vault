##########################################################################
# Use wayback machine to scrape Express front-page headlines for 2012    #
# v1: simply takes first page from each day of 2012                      #
##########################################################################

import scraperwiki
import lxml.html
import dateutil.parser
from datetime import datetime


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

#GET A LIST OF ALL AVAILABLE ARCHIVED PAGES FROM: http://web.archive.org/web/*/http://www.express.co.uk

def build_url_list():

#Builds a list of urls of archive pages based from summary page.

    #loop through page links to archived daily pages. Put in one big list
    urllist = []
#NEED TO ADD LIST TO DICT ON EACH LOOP KEYED ON URL
#CAN DO MIN ON URL (per day) as URLS can be numerically sorted

    pageurl= "http://wayback.archive.org/web/2004*/http://www.autofacts.ca"

    root = fetch_html(pageurl)
    print pageurl

    #Need to loop one day at a time
    for a in root.cssselect("div.date.tooltip"):

        crawltime = a.cssselect("a")
       
        #first element is first crawl if day
        if len(crawltime) >0:
            urllist.append(crawltime[0].get('href'))

            #print "0", crawltime[0].get('href')
            #print "0",crawltime[0].text_content()

    return urllist


for archpage in build_url_list():

    pagerurl = "http://web.archive.org" + archpage
    #print pageurl

    #ditionary to store info for each scraper
    pageinfo = {'Archive Page URL' : "",
            'Headline Article URL' :"",
                    'Date Published'  : "",
                    'Main Headline Text' : ""}

    root2 = fetch_html(pagerurl)


    for el in root2.cssselect("div#articleLarge"):

        el = el.cssselect("a")

        headurl = el[0].get('href')
        headtxt= el[0].text_content()

        pubdate = headurl[5:13:]
        #pageinfo ['Archive Page URL'] = headurl 

        pubdate2 = datetime.strptime(pubdate, '%Y%m%d')

        print headurl, headtxt, pubdate2 


    pageinfo ['Archive Page URL'] = pagerurl
    pageinfo ['Headline Article URL'] = headurl
    pageinfo ['Date Published'] = pubdate2.date()        
    pageinfo ['Main Headline Text'] = headtxt

    #using date published as key is a quick fix to resolve dupes
    #only a few hundred recs so shouldn't be any issues

    try:
        scraperwiki.sqlite.save(unique_keys=['Date Published'], data=pageinfo)
    except:
        print "Failed on: %s - %s --> " % (pageurl, pageinfo['Date Published'])
##########################################################################
# Use wayback machine to scrape Express front-page headlines for 2012    #
# v1: simply takes first page from each day of 2012                      #
##########################################################################

import scraperwiki
import lxml.html
import dateutil.parser
from datetime import datetime


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

#GET A LIST OF ALL AVAILABLE ARCHIVED PAGES FROM: http://web.archive.org/web/*/http://www.express.co.uk

def build_url_list():

#Builds a list of urls of archive pages based from summary page.

    #loop through page links to archived daily pages. Put in one big list
    urllist = []
#NEED TO ADD LIST TO DICT ON EACH LOOP KEYED ON URL
#CAN DO MIN ON URL (per day) as URLS can be numerically sorted

    pageurl= "http://wayback.archive.org/web/2004*/http://www.autofacts.ca"

    root = fetch_html(pageurl)
    print pageurl

    #Need to loop one day at a time
    for a in root.cssselect("div.date.tooltip"):

        crawltime = a.cssselect("a")
       
        #first element is first crawl if day
        if len(crawltime) >0:
            urllist.append(crawltime[0].get('href'))

            #print "0", crawltime[0].get('href')
            #print "0",crawltime[0].text_content()

    return urllist


for archpage in build_url_list():

    pagerurl = "http://web.archive.org" + archpage
    #print pageurl

    #ditionary to store info for each scraper
    pageinfo = {'Archive Page URL' : "",
            'Headline Article URL' :"",
                    'Date Published'  : "",
                    'Main Headline Text' : ""}

    root2 = fetch_html(pagerurl)


    for el in root2.cssselect("div#articleLarge"):

        el = el.cssselect("a")

        headurl = el[0].get('href')
        headtxt= el[0].text_content()

        pubdate = headurl[5:13:]
        #pageinfo ['Archive Page URL'] = headurl 

        pubdate2 = datetime.strptime(pubdate, '%Y%m%d')

        print headurl, headtxt, pubdate2 


    pageinfo ['Archive Page URL'] = pagerurl
    pageinfo ['Headline Article URL'] = headurl
    pageinfo ['Date Published'] = pubdate2.date()        
    pageinfo ['Main Headline Text'] = headtxt

    #using date published as key is a quick fix to resolve dupes
    #only a few hundred recs so shouldn't be any issues

    try:
        scraperwiki.sqlite.save(unique_keys=['Date Published'], data=pageinfo)
    except:
        print "Failed on: %s - %s --> " % (pageurl, pageinfo['Date Published'])
