#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapeschool(url):
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
        #create an empty variable 'record', which is a dictionary
    record = {}
        #create a uniqueid that we'll add to with each record later
    uniqueid = 0
    record["school"] = root.cssselect("h1")[0].text_content()
    record["parentviewurl"] = root.xpath(".//div[@id='content']//a")[0].attrib.get('href')
#Expressed more simply, this could take up three lines like so:
#    parentviewurls = root.xpath(".//div[@id='content']//a")
#    parentviewurl = parentviewurls[0].attrib.get('href')
#    record["parentviewurl"] = parentviewurl
    record["URN"] = root.xpath(".//div[@id='content']//p//strong")[0].text_content()
    record["Address"] = lxml.etree.tostring(root.xpath(".//div[@id='content']//p")[1])
    report1url = root.xpath(".//table[@summary='Previous reports']//td//a")[0].attrib.get('href')
    record["report1url"] = report1url
#    record["inspectiondate"] = root.xpath(".//table[@summary='Previous reports']//td")[1].text_content
    uniqueid =+ 1
    record["uniqueid"] = uniqueid
    print record
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(baseurl+report1url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
    leadership = re.search(r'b>The quality of .* <b',pdfread)
    if leadership:
#        print linenumber
        print leadership.group()
#find all <b> tagged lines - headings?
    lines = pdfroot.findall('.//text')
    linenumber = 0
    for line in lines:
        linenumber = linenumber+1
        if line.text:
            FSM = re.match(r'.* free school meals .*',line.text)
            if FSM:
                print linenumber
                print FSM.group()
#                if pdfroot.xpath('.//text')[linenumber-2].text:
                print pdfroot.xpath('.//text')[linenumber-2].text
                print pdfroot.xpath('.//text')[linenumber-1].text
                print pdfroot.xpath('.//text')[linenumber].text
#                if pdfroot.findall('.//text')[linenumber].text:
                record["FSM3"] = pdfroot.findall('.//text')[linenumber].text
                print record

#UP TO HERE. NEED TO:
#IDENTIFY THE LINE WE WANT - PERHAPS .XPATH AND (CONTAINS)
#GRAB X CHARACTERS AFTER THAT - OR:
#IDENTIFY THE INDEX POSITION OF THAT <TEXT><B> HEADING AND THE NEXT ONE AND GRAB ALL LINES BETWEEN

    scraperwiki.sqlite.save(["uniqueid"],record)
    




#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #Grab the links in HTML like this:
    #<h2><a href="/inspection-reports/find-inspection-report/provider/ELS/113867">Ashdown Technology College
    links = root.xpath(".//h2//a")
    #That will be a list, so we start a for loop to go through each item, calling it 'links'
    for link in links:
        #now put the 'href=' attribute of each link in the variable 'reportpage'
        reportpage = link.attrib.get('href')
        #show us the link
        print reportpage
        #add it to baseurl and pass it to a function 'scrapeschool' defined above
        scrapeschool(baseurl+reportpage)



#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)
    #once that has scraped the table, it returns here, and looks for the next link
    #which is in this HTML:
    #<a href="/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999?page=1" class="active">Next ›</a>
    next_link = root.cssselect("ul.pagination a.active")[-2].attrib.get('href')
    print next_link
    next_link_absolute = baseurl+next_link
    if next_link:
        scrape_and_look_for_next_link(next_link_absolute)

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"
#When added to the baseurl, this is our starting page 
startingurl = "/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999#search4"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapeschool(url):
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
        #create an empty variable 'record', which is a dictionary
    record = {}
        #create a uniqueid that we'll add to with each record later
    uniqueid = 0
    record["school"] = root.cssselect("h1")[0].text_content()
    record["parentviewurl"] = root.xpath(".//div[@id='content']//a")[0].attrib.get('href')
#Expressed more simply, this could take up three lines like so:
#    parentviewurls = root.xpath(".//div[@id='content']//a")
#    parentviewurl = parentviewurls[0].attrib.get('href')
#    record["parentviewurl"] = parentviewurl
    record["URN"] = root.xpath(".//div[@id='content']//p//strong")[0].text_content()
    record["Address"] = lxml.etree.tostring(root.xpath(".//div[@id='content']//p")[1])
    report1url = root.xpath(".//table[@summary='Previous reports']//td//a")[0].attrib.get('href')
    record["report1url"] = report1url
#    record["inspectiondate"] = root.xpath(".//table[@summary='Previous reports']//td")[1].text_content
    uniqueid =+ 1
    record["uniqueid"] = uniqueid
    print record
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(baseurl+report1url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
    leadership = re.search(r'b>The quality of .* <b',pdfread)
    if leadership:
#        print linenumber
        print leadership.group()
#find all <b> tagged lines - headings?
    lines = pdfroot.findall('.//text')
    linenumber = 0
    for line in lines:
        linenumber = linenumber+1
        if line.text:
            FSM = re.match(r'.* free school meals .*',line.text)
            if FSM:
                print linenumber
                print FSM.group()
#                if pdfroot.xpath('.//text')[linenumber-2].text:
                print pdfroot.xpath('.//text')[linenumber-2].text
                print pdfroot.xpath('.//text')[linenumber-1].text
                print pdfroot.xpath('.//text')[linenumber].text
#                if pdfroot.findall('.//text')[linenumber].text:
                record["FSM3"] = pdfroot.findall('.//text')[linenumber].text
                print record

#UP TO HERE. NEED TO:
#IDENTIFY THE LINE WE WANT - PERHAPS .XPATH AND (CONTAINS)
#GRAB X CHARACTERS AFTER THAT - OR:
#IDENTIFY THE INDEX POSITION OF THAT <TEXT><B> HEADING AND THE NEXT ONE AND GRAB ALL LINES BETWEEN

    scraperwiki.sqlite.save(["uniqueid"],record)
    




#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #Grab the links in HTML like this:
    #<h2><a href="/inspection-reports/find-inspection-report/provider/ELS/113867">Ashdown Technology College
    links = root.xpath(".//h2//a")
    #That will be a list, so we start a for loop to go through each item, calling it 'links'
    for link in links:
        #now put the 'href=' attribute of each link in the variable 'reportpage'
        reportpage = link.attrib.get('href')
        #show us the link
        print reportpage
        #add it to baseurl and pass it to a function 'scrapeschool' defined above
        scrapeschool(baseurl+reportpage)



#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)
    #once that has scraped the table, it returns here, and looks for the next link
    #which is in this HTML:
    #<a href="/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999?page=1" class="active">Next ›</a>
    next_link = root.cssselect("ul.pagination a.active")[-2].attrib.get('href')
    print next_link
    next_link_absolute = baseurl+next_link
    if next_link:
        scrape_and_look_for_next_link(next_link_absolute)

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"
#When added to the baseurl, this is our starting page 
startingurl = "/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999#search4"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapeschool(url):
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
        #create an empty variable 'record', which is a dictionary
    record = {}
        #create a uniqueid that we'll add to with each record later
    uniqueid = 0
    record["school"] = root.cssselect("h1")[0].text_content()
    record["parentviewurl"] = root.xpath(".//div[@id='content']//a")[0].attrib.get('href')
#Expressed more simply, this could take up three lines like so:
#    parentviewurls = root.xpath(".//div[@id='content']//a")
#    parentviewurl = parentviewurls[0].attrib.get('href')
#    record["parentviewurl"] = parentviewurl
    record["URN"] = root.xpath(".//div[@id='content']//p//strong")[0].text_content()
    record["Address"] = lxml.etree.tostring(root.xpath(".//div[@id='content']//p")[1])
    report1url = root.xpath(".//table[@summary='Previous reports']//td//a")[0].attrib.get('href')
    record["report1url"] = report1url
#    record["inspectiondate"] = root.xpath(".//table[@summary='Previous reports']//td")[1].text_content
    uniqueid =+ 1
    record["uniqueid"] = uniqueid
    print record
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(baseurl+report1url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
    leadership = re.search(r'b>The quality of .* <b',pdfread)
    if leadership:
#        print linenumber
        print leadership.group()
#find all <b> tagged lines - headings?
    lines = pdfroot.findall('.//text')
    linenumber = 0
    for line in lines:
        linenumber = linenumber+1
        if line.text:
            FSM = re.match(r'.* free school meals .*',line.text)
            if FSM:
                print linenumber
                print FSM.group()
#                if pdfroot.xpath('.//text')[linenumber-2].text:
                print pdfroot.xpath('.//text')[linenumber-2].text
                print pdfroot.xpath('.//text')[linenumber-1].text
                print pdfroot.xpath('.//text')[linenumber].text
#                if pdfroot.findall('.//text')[linenumber].text:
                record["FSM3"] = pdfroot.findall('.//text')[linenumber].text
                print record

#UP TO HERE. NEED TO:
#IDENTIFY THE LINE WE WANT - PERHAPS .XPATH AND (CONTAINS)
#GRAB X CHARACTERS AFTER THAT - OR:
#IDENTIFY THE INDEX POSITION OF THAT <TEXT><B> HEADING AND THE NEXT ONE AND GRAB ALL LINES BETWEEN

    scraperwiki.sqlite.save(["uniqueid"],record)
    




#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #Grab the links in HTML like this:
    #<h2><a href="/inspection-reports/find-inspection-report/provider/ELS/113867">Ashdown Technology College
    links = root.xpath(".//h2//a")
    #That will be a list, so we start a for loop to go through each item, calling it 'links'
    for link in links:
        #now put the 'href=' attribute of each link in the variable 'reportpage'
        reportpage = link.attrib.get('href')
        #show us the link
        print reportpage
        #add it to baseurl and pass it to a function 'scrapeschool' defined above
        scrapeschool(baseurl+reportpage)



#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)
    #once that has scraped the table, it returns here, and looks for the next link
    #which is in this HTML:
    #<a href="/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999?page=1" class="active">Next ›</a>
    next_link = root.cssselect("ul.pagination a.active")[-2].attrib.get('href')
    print next_link
    next_link_absolute = baseurl+next_link
    if next_link:
        scrape_and_look_for_next_link(next_link_absolute)

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"
#When added to the baseurl, this is our starting page 
startingurl = "/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999#search4"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapeschool(url):
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
        #create an empty variable 'record', which is a dictionary
    record = {}
        #create a uniqueid that we'll add to with each record later
    uniqueid = 0
    record["school"] = root.cssselect("h1")[0].text_content()
    record["parentviewurl"] = root.xpath(".//div[@id='content']//a")[0].attrib.get('href')
#Expressed more simply, this could take up three lines like so:
#    parentviewurls = root.xpath(".//div[@id='content']//a")
#    parentviewurl = parentviewurls[0].attrib.get('href')
#    record["parentviewurl"] = parentviewurl
    record["URN"] = root.xpath(".//div[@id='content']//p//strong")[0].text_content()
    record["Address"] = lxml.etree.tostring(root.xpath(".//div[@id='content']//p")[1])
    report1url = root.xpath(".//table[@summary='Previous reports']//td//a")[0].attrib.get('href')
    record["report1url"] = report1url
#    record["inspectiondate"] = root.xpath(".//table[@summary='Previous reports']//td")[1].text_content
    uniqueid =+ 1
    record["uniqueid"] = uniqueid
    print record
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(baseurl+report1url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
    leadership = re.search(r'b>The quality of .* <b',pdfread)
    if leadership:
#        print linenumber
        print leadership.group()
#find all <b> tagged lines - headings?
    lines = pdfroot.findall('.//text')
    linenumber = 0
    for line in lines:
        linenumber = linenumber+1
        if line.text:
            FSM = re.match(r'.* free school meals .*',line.text)
            if FSM:
                print linenumber
                print FSM.group()
#                if pdfroot.xpath('.//text')[linenumber-2].text:
                print pdfroot.xpath('.//text')[linenumber-2].text
                print pdfroot.xpath('.//text')[linenumber-1].text
                print pdfroot.xpath('.//text')[linenumber].text
#                if pdfroot.findall('.//text')[linenumber].text:
                record["FSM3"] = pdfroot.findall('.//text')[linenumber].text
                print record

#UP TO HERE. NEED TO:
#IDENTIFY THE LINE WE WANT - PERHAPS .XPATH AND (CONTAINS)
#GRAB X CHARACTERS AFTER THAT - OR:
#IDENTIFY THE INDEX POSITION OF THAT <TEXT><B> HEADING AND THE NEXT ONE AND GRAB ALL LINES BETWEEN

    scraperwiki.sqlite.save(["uniqueid"],record)
    




#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #Grab the links in HTML like this:
    #<h2><a href="/inspection-reports/find-inspection-report/provider/ELS/113867">Ashdown Technology College
    links = root.xpath(".//h2//a")
    #That will be a list, so we start a for loop to go through each item, calling it 'links'
    for link in links:
        #now put the 'href=' attribute of each link in the variable 'reportpage'
        reportpage = link.attrib.get('href')
        #show us the link
        print reportpage
        #add it to baseurl and pass it to a function 'scrapeschool' defined above
        scrapeschool(baseurl+reportpage)



#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)
    #once that has scraped the table, it returns here, and looks for the next link
    #which is in this HTML:
    #<a href="/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999?page=1" class="active">Next ›</a>
    next_link = root.cssselect("ul.pagination a.active")[-2].attrib.get('href')
    print next_link
    next_link_absolute = baseurl+next_link
    if next_link:
        scrape_and_look_for_next_link(next_link_absolute)

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"
#When added to the baseurl, this is our starting page 
startingurl = "/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999#search4"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapeschool(url):
    print url
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
        #create an empty variable 'record', which is a dictionary
    record = {}
        #create a uniqueid that we'll add to with each record later
    uniqueid = 0
    record["school"] = root.cssselect("h1")[0].text_content()
    record["parentviewurl"] = root.xpath(".//div[@id='content']//a")[0].attrib.get('href')
#Expressed more simply, this could take up three lines like so:
#    parentviewurls = root.xpath(".//div[@id='content']//a")
#    parentviewurl = parentviewurls[0].attrib.get('href')
#    record["parentviewurl"] = parentviewurl
    record["URN"] = root.xpath(".//div[@id='content']//p//strong")[0].text_content()
    record["Address"] = lxml.etree.tostring(root.xpath(".//div[@id='content']//p")[1])
    report1url = root.xpath(".//table[@summary='Previous reports']//td//a")[0].attrib.get('href')
    record["report1url"] = report1url
#    record["inspectiondate"] = root.xpath(".//table[@summary='Previous reports']//td")[1].text_content
    uniqueid =+ 1
    record["uniqueid"] = uniqueid
    print record
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(baseurl+report1url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
    leadership = re.search(r'b>The quality of .* <b',pdfread)
    if leadership:
#        print linenumber
        print leadership.group()
#find all <b> tagged lines - headings?
    lines = pdfroot.findall('.//text')
    linenumber = 0
    for line in lines:
        linenumber = linenumber+1
        if line.text:
            FSM = re.match(r'.* free school meals .*',line.text)
            if FSM:
                print linenumber
                print FSM.group()
#                if pdfroot.xpath('.//text')[linenumber-2].text:
                print pdfroot.xpath('.//text')[linenumber-2].text
                print pdfroot.xpath('.//text')[linenumber-1].text
                print pdfroot.xpath('.//text')[linenumber].text
#                if pdfroot.findall('.//text')[linenumber].text:
                record["FSM3"] = pdfroot.findall('.//text')[linenumber].text
                print record

#UP TO HERE. NEED TO:
#IDENTIFY THE LINE WE WANT - PERHAPS .XPATH AND (CONTAINS)
#GRAB X CHARACTERS AFTER THAT - OR:
#IDENTIFY THE INDEX POSITION OF THAT <TEXT><B> HEADING AND THE NEXT ONE AND GRAB ALL LINES BETWEEN

    scraperwiki.sqlite.save(["uniqueid"],record)
    




#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #Grab the links in HTML like this:
    #<h2><a href="/inspection-reports/find-inspection-report/provider/ELS/113867">Ashdown Technology College
    links = root.xpath(".//h2//a")
    #That will be a list, so we start a for loop to go through each item, calling it 'links'
    for link in links:
        #now put the 'href=' attribute of each link in the variable 'reportpage'
        reportpage = link.attrib.get('href')
        #show us the link
        print reportpage
        #add it to baseurl and pass it to a function 'scrapeschool' defined above
        scrapeschool(baseurl+reportpage)



#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)
    #once that has scraped the table, it returns here, and looks for the next link
    #which is in this HTML:
    #<a href="/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999?page=1" class="active">Next ›</a>
    next_link = root.cssselect("ul.pagination a.active")[-2].attrib.get('href')
    print next_link
    next_link_absolute = baseurl+next_link
    if next_link:
        scrape_and_look_for_next_link(next_link_absolute)

#This will be used for relative links in later pages
baseurl = "http://www.ofsted.gov.uk"
#When added to the baseurl, this is our starting page 
startingurl = "/inspection-reports/find-inspection-report/results/type/23/range/1301612400/1346453999#search4"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
