#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html
import random

#TO DO: Grab services provided
#TO DO: Grab parts of `report text

def scrapeschool(url, LA, latestreport):
    print "url", url
    #scrape the 'url' variable into 'html'
    html = scraperwiki.scrape(url)
    print "html", html
    #convert that from a string into an lxml object, 'root'
    root = lxml.html.fromstring(html)
        #create an empty variable 'record', which is a dictionary
    record = {}
    #store the three variables passed into this function when it runs:
    #this first one allows us to see where the scraper got to if it falls over, then change the starting URL to that and run again
    record['resultspage'] = url
    record['LA'] = str(LA)
    record['latestreport'] = latestreport
    #look in 'root' for <table summary="Previous reports"><td><a>, and store results as 'reporttypes':
    reporttypes = root.xpath(".//table[@summary='Previous reports']//td//a")
    #loop through that list of results:
    for reporttype in reporttypes:
        print "reporttype", reporttype.text_content()
        #put the text content into 'matching'
        matching = reporttype.text_content()
        #use regex (re) to search for the phrase 'Social care inspection report'
        #and store any matches in 'match'
        match = re.search(r'Social care inspection report.*',matching)
#IF that match variable is created (i.e. there is a match), then start recording data
        if match:
            print "INSPECTION REPORT", match.group()
            #the school name is in the first (0) <h1> tag
            record["school"] = root.cssselect("h1")[0].text_content()
            #the URN is the first text in <div id='content'><p><strong>
            record["URN"] = root.xpath(".//div[@id='content']//p//strong")[0].text_content()
            #closed schools have an image in <h1><img> with <alt='closed'>, but other have no image, so we have to test first:
            if root.cssselect("h1 img"):
            #and if it exists, we store the <alt> attribute of the first one
                record['closed'] = root.cssselect("h1 img")[0].attrib.get('alt')
            else:
            #otherwise we record 'no icon'
                record['closed'] = "NO ICON"
            #the most recent report link will be in the first <table summary='Previous reports'><td><a> tags
            report1url = root.xpath(".//table[@summary='Previous reports']//td//a")[0].attrib.get('href')
            record["report1url"] = report1url
            print "record", record
            scraperwiki.sqlite.save(["report1url"],record)

#This section would go before the line above to work
'''#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
            pdfdata = urllib2.urlopen(baseurl+report1url).read()
#use pdftoxml to convert that into an xml document
            pdfread = scraperwiki.pdftoxml(pdfdata)
            print "pdfread:", pdfread
#use lxml.etree to convert that into an lxml object - we're not using this yet.
            pdfroot = lxml.etree.fromstring(pdfread)
#likewise, this looks for services provided, but we need to work out how to grab more than one, and to not fall over when there aren't any listed at all
            services = re.match("services for the following:<\/p><ul><li>.*<\/ul", html)
            print "SERVICES", services'''



#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #Grab the lits items in one list in the HTML like this:
    #<ul class="resultsList"><li>
    lis = root.xpath(".//ul[@class='resultsList']//li")
    #loop through each and grab more details before running another function:
    for li in lis:
        print li
        #this grabs the first <h2><a> in the item, and then grabs the "href=' attribute
        link = li.xpath(".//h2//a")[0].attrib.get('href')
        #this grabs the text content in the third <p> tag - the local authority
        LA = li.xpath(".//p")[2].text_content()
        #this grabs the text content in the fourth <p> tag - the report date
        latestreport = li.xpath(".//p")[3].text_content()
        print "LINK & LA", link, LA, latestreport
        #this adds 'link' to baseurl and uses it to run a function 'scrapeschool' defined above
        #it also 'passes' the other two variables we've created, because we'll need to store these in the next function
        scrapeschool(baseurl+link, LA, latestreport)



#This creates a function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root' - now look at those lines to see what happens, before returning here
    scrapetable(root)
    #once that has scraped the table, it returns here, and looks for the next link
    #which is in this HTML:
    #<a href="/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999?page=1" class="active">Next ›</a>
    next_link = root.cssselect("ul.pagination a.active")[-2].attrib.get('href')
    print next_link
    next_link_absolute = baseurl+next_link
    if next_link:
        scrape_and_look_for_next_link(next_link_absolute)

#START HERE

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"
#When added to the baseurl, this is our starting page 
#startingurl = "/inspection-reports/find-inspection-report/results/type/2/any/any?sort=1"
#startingurl = "/inspection-reports/find-inspection-report/results/all/all/turney/any#search1"
#Changing the startingurl below starts the scraper 10 pages before the last, i.e. the last 100 results: 
startingurl = '/inspection-reports/find-inspection-report/results/type/2/any/any?page=237&sort=1'

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
