#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapepdf(url):
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
#find all <text> tags and put in list variable 'lines'
    lines = pdfroot.findall('.//text')
    #create variable 'linenumber', initialised at 0
    linenumber = 0
    record = {}
    #loop through each item in 'lines' list
    for line in lines:
        #add one to 'linenumber' so we can track which line we're dealing with
        linenumber = linenumber+1
        #if 'line' has some text:
        if line.text is not None:
#create a new variable 'mention' that is filled with the result of
#using the 're' library's .match function
            mention = re.search(r'.*black.*',line.text)
            if mention:
                print line.text
#the RANGE function generates a list from the first parameter to the second, 
#e.g. range(5,8) would make [5, 6, 7] - it doesn't include the 'end' of the range
#in this case we're using the line number minus 2, and the linenumber as our start and end points
                print range(linenumber-2,linenumber+1)
                linebefore = "EMPTY LINE"
                lineafter = "EMPTY LINE"
                incontextlist = []
                if pdfroot.xpath('.//text')[linenumber-2].text:
                    linebefore = pdfroot.xpath('.//text')[linenumber-2].text
                    incontextlist.append(linebefore)
                incontextlist.append(pdfroot.xpath('.//text')[linenumber-1].text)
                if pdfroot.xpath('.//text')[linenumber].text is not None:
                    lineafter = pdfroot.xpath('.//text')[linenumber].text
                    incontextlist.append(lineafter)
                print "mention.group()", mention.group()
                print "CAN YOU SEE ME?", ''.join(incontextlist)
                record["mention in context"] = ''.join(incontextlist)
                record["linenumber"] = linenumber
#this stores the 'url' variable which is passed right at the start of this function: def scrapepdf(url):
                record["url"] = url
                print record
                scraperwiki.sqlite.save(["linenumber", "url"],record)

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #links to each PDF are in HTML like this:
    #<p><a onclick="window.open(this.href, '_blank'); return false;" title="Link to the October 2012 Stop and Search update - link opens in new window" href="/PDF/PSD_031012_04_Stop_and_Search.pdf" onkeypress="if (event.keyCode==13) {window.open(this.href, '_blank'); return false;}">Stop/Search and Stop/Account Update - October 2012</a> &gt;</p>
#This just shows us the href= attribute of each item ('link') in that list
    pdflinks = root.cssselect("p a")
    for link in pdflinks:
        print link.attrib.get('href')
        next_link_absolute = baseurl+link.attrib.get('href')
#this line has 'is not None' added as future versions won't accept 'if link'
        if link is not None:
            scrapepdf(next_link_absolute)

#This could be used for relative links in later pages
baseurl = "http://www.dpa.police.uk"
#When added to the baseurl, this is our starting page: http://www.dpa.police.uk/default.aspx?page=473
startingurl = "/default.aspx?page=473"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapepdf(url):
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
#find all <text> tags and put in list variable 'lines'
    lines = pdfroot.findall('.//text')
    #create variable 'linenumber', initialised at 0
    linenumber = 0
    record = {}
    #loop through each item in 'lines' list
    for line in lines:
        #add one to 'linenumber' so we can track which line we're dealing with
        linenumber = linenumber+1
        #if 'line' has some text:
        if line.text is not None:
#create a new variable 'mention' that is filled with the result of
#using the 're' library's .match function
            mention = re.search(r'.*black.*',line.text)
            if mention:
                print line.text
#the RANGE function generates a list from the first parameter to the second, 
#e.g. range(5,8) would make [5, 6, 7] - it doesn't include the 'end' of the range
#in this case we're using the line number minus 2, and the linenumber as our start and end points
                print range(linenumber-2,linenumber+1)
                linebefore = "EMPTY LINE"
                lineafter = "EMPTY LINE"
                incontextlist = []
                if pdfroot.xpath('.//text')[linenumber-2].text:
                    linebefore = pdfroot.xpath('.//text')[linenumber-2].text
                    incontextlist.append(linebefore)
                incontextlist.append(pdfroot.xpath('.//text')[linenumber-1].text)
                if pdfroot.xpath('.//text')[linenumber].text is not None:
                    lineafter = pdfroot.xpath('.//text')[linenumber].text
                    incontextlist.append(lineafter)
                print "mention.group()", mention.group()
                print "CAN YOU SEE ME?", ''.join(incontextlist)
                record["mention in context"] = ''.join(incontextlist)
                record["linenumber"] = linenumber
#this stores the 'url' variable which is passed right at the start of this function: def scrapepdf(url):
                record["url"] = url
                print record
                scraperwiki.sqlite.save(["linenumber", "url"],record)

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #links to each PDF are in HTML like this:
    #<p><a onclick="window.open(this.href, '_blank'); return false;" title="Link to the October 2012 Stop and Search update - link opens in new window" href="/PDF/PSD_031012_04_Stop_and_Search.pdf" onkeypress="if (event.keyCode==13) {window.open(this.href, '_blank'); return false;}">Stop/Search and Stop/Account Update - October 2012</a> &gt;</p>
#This just shows us the href= attribute of each item ('link') in that list
    pdflinks = root.cssselect("p a")
    for link in pdflinks:
        print link.attrib.get('href')
        next_link_absolute = baseurl+link.attrib.get('href')
#this line has 'is not None' added as future versions won't accept 'if link'
        if link is not None:
            scrapepdf(next_link_absolute)

#This could be used for relative links in later pages
baseurl = "http://www.dpa.police.uk"
#When added to the baseurl, this is our starting page: http://www.dpa.police.uk/default.aspx?page=473
startingurl = "/default.aspx?page=473"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html

def scrapepdf(url):
#use the urllib2 library's .urlopen function to open the full PDF URL, and the .read() function to read it into a new object, 'pdfdata'
    pdfdata = urllib2.urlopen(url).read()
#use pdftoxml to convert that into an xml document
    pdfread = scraperwiki.pdftoxml(pdfdata)
    print pdfread
#use lxml.etree to convert that into an lxml object
    pdfroot = lxml.etree.fromstring(pdfread)
#find all <text> tags and put in list variable 'lines'
    lines = pdfroot.findall('.//text')
    #create variable 'linenumber', initialised at 0
    linenumber = 0
    record = {}
    #loop through each item in 'lines' list
    for line in lines:
        #add one to 'linenumber' so we can track which line we're dealing with
        linenumber = linenumber+1
        #if 'line' has some text:
        if line.text is not None:
#create a new variable 'mention' that is filled with the result of
#using the 're' library's .match function
            mention = re.search(r'.*black.*',line.text)
            if mention:
                print line.text
#the RANGE function generates a list from the first parameter to the second, 
#e.g. range(5,8) would make [5, 6, 7] - it doesn't include the 'end' of the range
#in this case we're using the line number minus 2, and the linenumber as our start and end points
                print range(linenumber-2,linenumber+1)
                linebefore = "EMPTY LINE"
                lineafter = "EMPTY LINE"
                incontextlist = []
                if pdfroot.xpath('.//text')[linenumber-2].text:
                    linebefore = pdfroot.xpath('.//text')[linenumber-2].text
                    incontextlist.append(linebefore)
                incontextlist.append(pdfroot.xpath('.//text')[linenumber-1].text)
                if pdfroot.xpath('.//text')[linenumber].text is not None:
                    lineafter = pdfroot.xpath('.//text')[linenumber].text
                    incontextlist.append(lineafter)
                print "mention.group()", mention.group()
                print "CAN YOU SEE ME?", ''.join(incontextlist)
                record["mention in context"] = ''.join(incontextlist)
                record["linenumber"] = linenumber
#this stores the 'url' variable which is passed right at the start of this function: def scrapepdf(url):
                record["url"] = url
                print record
                scraperwiki.sqlite.save(["linenumber", "url"],record)

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #links to each PDF are in HTML like this:
    #<p><a onclick="window.open(this.href, '_blank'); return false;" title="Link to the October 2012 Stop and Search update - link opens in new window" href="/PDF/PSD_031012_04_Stop_and_Search.pdf" onkeypress="if (event.keyCode==13) {window.open(this.href, '_blank'); return false;}">Stop/Search and Stop/Account Update - October 2012</a> &gt;</p>
#This just shows us the href= attribute of each item ('link') in that list
    pdflinks = root.cssselect("p a")
    for link in pdflinks:
        print link.attrib.get('href')
        next_link_absolute = baseurl+link.attrib.get('href')
#this line has 'is not None' added as future versions won't accept 'if link'
        if link is not None:
            scrapepdf(next_link_absolute)

#This could be used for relative links in later pages
baseurl = "http://www.dpa.police.uk"
#When added to the baseurl, this is our starting page: http://www.dpa.police.uk/default.aspx?page=473
startingurl = "/default.aspx?page=473"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)
