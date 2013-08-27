#import the libraries we'll need

import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#<table summary="Corporate level publications: What our priorities are and how we are doing: Knife Crime Summaries" class="foidocuments">

#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #create an empty variable 'record', which is a dictionary
    record = {}
    uniqueid = 0
    #Grab any bits of 'root' that have the tag <table> containing summary=" and 'Knife' somewhere in that, then the contents of <tr>. Put the results in variable called 'rows'
    rows = root.xpath(".//table[contains(@summary, 'Knife')]//tr")
    #That will be a list, so we start a for loop to go through each item, calling it 'row'
    for row in rows:
        #show us the text content of that object
        print row.text_content()
        #now grab the contents of all <td><a tags within that 'row' object, and put it in the variable 'report'
        report = row.cssselect("td a")
        #if that exists...
        if report:
            #get us the value of the first (index 0) 'href=' attribute
            pdfurl = report[0].attrib.get('href')
            #store the value of the first 'href=' and 'title=' attributes with the labels 'URL' and 'Date' in the variable 'record'
            record["Date"] = report[0].attrib.get('title')
            record["URL"] = report[0].attrib.get('href')
#            if the 'pdfurl' variable was indeed created...
            if pdfurl:
#Start running a PDF scraper on that, firstly 'opening' the PDF URL with the urllib2 library's urlopen function, and 'reading' the PDF into a variable called 'pdfdata'...
                pdfdata = urllib2.urlopen(baseurl+pdfurl).read()
#...Then using pdftoxml to convert that into a variable called 'xmldata'
                xmldata = scraperwiki.pdftoxml(pdfdata)
#...Then using .fromstring to convert that into a variable called 'pdfxml'
                pdfxml = lxml.etree.fromstring(xmldata)
                print xmldata
#Use .xpath again to find <text ... top="191"> tags, and <b> tags within those
                boldtags1 = pdfxml.xpath('.//text[contains(@top, "492")]//b')
#Then store the first [0] result's text in 'Date2'
                record ["Date2"] = boldtags1[0].text
                boldtags = pdfxml.xpath('.//text[contains(@top, "386")]//b')
#This is the code that the line above is looking for
#<text top="386" left="464" width="75" height="21" font="0"><b>04/09/2012</b></text>
#Then store the second [1] result's text in 'Review Date'
                record ["Review Date"] = boldtags[1].text
                print record
#Now we grab all the <text ...> tags
                texttags = pdfxml.xpath('.//text')
                for text in texttags:
                    left = text.attrib.get('left')
                    #convert the attribute from a string into an integer:
                    leftinteger = int(left)
#IF leftinteger is between 96 and 99
#Literally? If 96 is smaller than leftinteger, and leftinteger is smaller than 99:
#see other options at http://stackoverflow.com/questions/618093/how-to-find-whether-a-number-belongs-to-a-particular-range-in-python

                    if 96 < leftinteger < 99:
                        #Record the text of 'text' (sorry)
                        record ["BOCUname"] = text.text
                        print record
                    if 324 < leftinteger < 327:
                        record ["Offences"] = text.text
                        print record
                    if 405 < leftinteger < 408:
                        record ["Sanction_detentions"] = text.text
                        print record
                    if 481 < leftinteger < 484:
                        record ["Sanction_detention_rate"] = text.text
                        print record
                    if 587 < leftinteger < 590:
                        record ["Offences FYTD_2011_12"] = text.text
                        print record
                    if 661 < leftinteger < 664:
                        record ["Offences FYTD_2012_13"] = text.text
                        print record
                    if 713 < leftinteger < 716:
                        record ["Offences percentage change"] = text.text
                        print record
                    if 812 < leftinteger < 815:
                        record ["Sanction detections FYTD 2011_12"] = text.text
                    if 887 < leftinteger < 890:
                        record ["Sanction Detections FYTD_2012_13"] = text.text
                    if 943 < leftinteger < 946:
                        record ["Sanction Detection rate FYTD 2011_12"] = text.text
                    if 1021 < leftinteger < 1024:
                        record ["Sanction Detections rate FYTD 2012_13"] = text.text
                        uniqueid = uniqueid+1
                        record ["uniqueid"] = uniqueid
                        print record
                        scraperwiki.sqlite.save(["uniqueid","Date"], record)                    
                    else:
                        print "NO DATA!"

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)

#This will be used for relative links in later pages
baseurl = "http://www.met.police.uk/foi/"
#When added to the baseurl, this is our starting page 
startingurl = "c_priorities_and_how_we_are_doing.htm"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)


#COPY ACROSS CODE FROM PREVIOUS SCRAPER PT3#import the libraries we'll need

import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#<table summary="Corporate level publications: What our priorities are and how we are doing: Knife Crime Summaries" class="foidocuments">

#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #create an empty variable 'record', which is a dictionary
    record = {}
    uniqueid = 0
    #Grab any bits of 'root' that have the tag <table> containing summary=" and 'Knife' somewhere in that, then the contents of <tr>. Put the results in variable called 'rows'
    rows = root.xpath(".//table[contains(@summary, 'Knife')]//tr")
    #That will be a list, so we start a for loop to go through each item, calling it 'row'
    for row in rows:
        #show us the text content of that object
        print row.text_content()
        #now grab the contents of all <td><a tags within that 'row' object, and put it in the variable 'report'
        report = row.cssselect("td a")
        #if that exists...
        if report:
            #get us the value of the first (index 0) 'href=' attribute
            pdfurl = report[0].attrib.get('href')
            #store the value of the first 'href=' and 'title=' attributes with the labels 'URL' and 'Date' in the variable 'record'
            record["Date"] = report[0].attrib.get('title')
            record["URL"] = report[0].attrib.get('href')
#            if the 'pdfurl' variable was indeed created...
            if pdfurl:
#Start running a PDF scraper on that, firstly 'opening' the PDF URL with the urllib2 library's urlopen function, and 'reading' the PDF into a variable called 'pdfdata'...
                pdfdata = urllib2.urlopen(baseurl+pdfurl).read()
#...Then using pdftoxml to convert that into a variable called 'xmldata'
                xmldata = scraperwiki.pdftoxml(pdfdata)
#...Then using .fromstring to convert that into a variable called 'pdfxml'
                pdfxml = lxml.etree.fromstring(xmldata)
                print xmldata
#Use .xpath again to find <text ... top="191"> tags, and <b> tags within those
                boldtags1 = pdfxml.xpath('.//text[contains(@top, "492")]//b')
#Then store the first [0] result's text in 'Date2'
                record ["Date2"] = boldtags1[0].text
                boldtags = pdfxml.xpath('.//text[contains(@top, "386")]//b')
#This is the code that the line above is looking for
#<text top="386" left="464" width="75" height="21" font="0"><b>04/09/2012</b></text>
#Then store the second [1] result's text in 'Review Date'
                record ["Review Date"] = boldtags[1].text
                print record
#Now we grab all the <text ...> tags
                texttags = pdfxml.xpath('.//text')
                for text in texttags:
                    left = text.attrib.get('left')
                    #convert the attribute from a string into an integer:
                    leftinteger = int(left)
#IF leftinteger is between 96 and 99
#Literally? If 96 is smaller than leftinteger, and leftinteger is smaller than 99:
#see other options at http://stackoverflow.com/questions/618093/how-to-find-whether-a-number-belongs-to-a-particular-range-in-python

                    if 96 < leftinteger < 99:
                        #Record the text of 'text' (sorry)
                        record ["BOCUname"] = text.text
                        print record
                    if 324 < leftinteger < 327:
                        record ["Offences"] = text.text
                        print record
                    if 405 < leftinteger < 408:
                        record ["Sanction_detentions"] = text.text
                        print record
                    if 481 < leftinteger < 484:
                        record ["Sanction_detention_rate"] = text.text
                        print record
                    if 587 < leftinteger < 590:
                        record ["Offences FYTD_2011_12"] = text.text
                        print record
                    if 661 < leftinteger < 664:
                        record ["Offences FYTD_2012_13"] = text.text
                        print record
                    if 713 < leftinteger < 716:
                        record ["Offences percentage change"] = text.text
                        print record
                    if 812 < leftinteger < 815:
                        record ["Sanction detections FYTD 2011_12"] = text.text
                    if 887 < leftinteger < 890:
                        record ["Sanction Detections FYTD_2012_13"] = text.text
                    if 943 < leftinteger < 946:
                        record ["Sanction Detection rate FYTD 2011_12"] = text.text
                    if 1021 < leftinteger < 1024:
                        record ["Sanction Detections rate FYTD 2012_13"] = text.text
                        uniqueid = uniqueid+1
                        record ["uniqueid"] = uniqueid
                        print record
                        scraperwiki.sqlite.save(["uniqueid","Date"], record)                    
                    else:
                        print "NO DATA!"

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)

#This will be used for relative links in later pages
baseurl = "http://www.met.police.uk/foi/"
#When added to the baseurl, this is our starting page 
startingurl = "c_priorities_and_how_we_are_doing.htm"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)


#COPY ACROSS CODE FROM PREVIOUS SCRAPER PT3#import the libraries we'll need

import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#<table summary="Corporate level publications: What our priorities are and how we are doing: Knife Crime Summaries" class="foidocuments">

#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #create an empty variable 'record', which is a dictionary
    record = {}
    uniqueid = 0
    #Grab any bits of 'root' that have the tag <table> containing summary=" and 'Knife' somewhere in that, then the contents of <tr>. Put the results in variable called 'rows'
    rows = root.xpath(".//table[contains(@summary, 'Knife')]//tr")
    #That will be a list, so we start a for loop to go through each item, calling it 'row'
    for row in rows:
        #show us the text content of that object
        print row.text_content()
        #now grab the contents of all <td><a tags within that 'row' object, and put it in the variable 'report'
        report = row.cssselect("td a")
        #if that exists...
        if report:
            #get us the value of the first (index 0) 'href=' attribute
            pdfurl = report[0].attrib.get('href')
            #store the value of the first 'href=' and 'title=' attributes with the labels 'URL' and 'Date' in the variable 'record'
            record["Date"] = report[0].attrib.get('title')
            record["URL"] = report[0].attrib.get('href')
#            if the 'pdfurl' variable was indeed created...
            if pdfurl:
#Start running a PDF scraper on that, firstly 'opening' the PDF URL with the urllib2 library's urlopen function, and 'reading' the PDF into a variable called 'pdfdata'...
                pdfdata = urllib2.urlopen(baseurl+pdfurl).read()
#...Then using pdftoxml to convert that into a variable called 'xmldata'
                xmldata = scraperwiki.pdftoxml(pdfdata)
#...Then using .fromstring to convert that into a variable called 'pdfxml'
                pdfxml = lxml.etree.fromstring(xmldata)
                print xmldata
#Use .xpath again to find <text ... top="191"> tags, and <b> tags within those
                boldtags1 = pdfxml.xpath('.//text[contains(@top, "492")]//b')
#Then store the first [0] result's text in 'Date2'
                record ["Date2"] = boldtags1[0].text
                boldtags = pdfxml.xpath('.//text[contains(@top, "386")]//b')
#This is the code that the line above is looking for
#<text top="386" left="464" width="75" height="21" font="0"><b>04/09/2012</b></text>
#Then store the second [1] result's text in 'Review Date'
                record ["Review Date"] = boldtags[1].text
                print record
#Now we grab all the <text ...> tags
                texttags = pdfxml.xpath('.//text')
                for text in texttags:
                    left = text.attrib.get('left')
                    #convert the attribute from a string into an integer:
                    leftinteger = int(left)
#IF leftinteger is between 96 and 99
#Literally? If 96 is smaller than leftinteger, and leftinteger is smaller than 99:
#see other options at http://stackoverflow.com/questions/618093/how-to-find-whether-a-number-belongs-to-a-particular-range-in-python

                    if 96 < leftinteger < 99:
                        #Record the text of 'text' (sorry)
                        record ["BOCUname"] = text.text
                        print record
                    if 324 < leftinteger < 327:
                        record ["Offences"] = text.text
                        print record
                    if 405 < leftinteger < 408:
                        record ["Sanction_detentions"] = text.text
                        print record
                    if 481 < leftinteger < 484:
                        record ["Sanction_detention_rate"] = text.text
                        print record
                    if 587 < leftinteger < 590:
                        record ["Offences FYTD_2011_12"] = text.text
                        print record
                    if 661 < leftinteger < 664:
                        record ["Offences FYTD_2012_13"] = text.text
                        print record
                    if 713 < leftinteger < 716:
                        record ["Offences percentage change"] = text.text
                        print record
                    if 812 < leftinteger < 815:
                        record ["Sanction detections FYTD 2011_12"] = text.text
                    if 887 < leftinteger < 890:
                        record ["Sanction Detections FYTD_2012_13"] = text.text
                    if 943 < leftinteger < 946:
                        record ["Sanction Detection rate FYTD 2011_12"] = text.text
                    if 1021 < leftinteger < 1024:
                        record ["Sanction Detections rate FYTD 2012_13"] = text.text
                        uniqueid = uniqueid+1
                        record ["uniqueid"] = uniqueid
                        print record
                        scraperwiki.sqlite.save(["uniqueid","Date"], record)                    
                    else:
                        print "NO DATA!"

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)

#This will be used for relative links in later pages
baseurl = "http://www.met.police.uk/foi/"
#When added to the baseurl, this is our starting page 
startingurl = "c_priorities_and_how_we_are_doing.htm"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)


#COPY ACROSS CODE FROM PREVIOUS SCRAPER PT3#import the libraries we'll need

import scraperwiki
import urllib2
import lxml.etree
import lxml.html

#<table summary="Corporate level publications: What our priorities are and how we are doing: Knife Crime Summaries" class="foidocuments">

#This creates a new function to find the part of the page we want, scrape bits, and follow links in it.
def scrapetable(root):
    #create an empty variable 'record', which is a dictionary
    record = {}
    uniqueid = 0
    #Grab any bits of 'root' that have the tag <table> containing summary=" and 'Knife' somewhere in that, then the contents of <tr>. Put the results in variable called 'rows'
    rows = root.xpath(".//table[contains(@summary, 'Knife')]//tr")
    #That will be a list, so we start a for loop to go through each item, calling it 'row'
    for row in rows:
        #show us the text content of that object
        print row.text_content()
        #now grab the contents of all <td><a tags within that 'row' object, and put it in the variable 'report'
        report = row.cssselect("td a")
        #if that exists...
        if report:
            #get us the value of the first (index 0) 'href=' attribute
            pdfurl = report[0].attrib.get('href')
            #store the value of the first 'href=' and 'title=' attributes with the labels 'URL' and 'Date' in the variable 'record'
            record["Date"] = report[0].attrib.get('title')
            record["URL"] = report[0].attrib.get('href')
#            if the 'pdfurl' variable was indeed created...
            if pdfurl:
#Start running a PDF scraper on that, firstly 'opening' the PDF URL with the urllib2 library's urlopen function, and 'reading' the PDF into a variable called 'pdfdata'...
                pdfdata = urllib2.urlopen(baseurl+pdfurl).read()
#...Then using pdftoxml to convert that into a variable called 'xmldata'
                xmldata = scraperwiki.pdftoxml(pdfdata)
#...Then using .fromstring to convert that into a variable called 'pdfxml'
                pdfxml = lxml.etree.fromstring(xmldata)
                print xmldata
#Use .xpath again to find <text ... top="191"> tags, and <b> tags within those
                boldtags1 = pdfxml.xpath('.//text[contains(@top, "492")]//b')
#Then store the first [0] result's text in 'Date2'
                record ["Date2"] = boldtags1[0].text
                boldtags = pdfxml.xpath('.//text[contains(@top, "386")]//b')
#This is the code that the line above is looking for
#<text top="386" left="464" width="75" height="21" font="0"><b>04/09/2012</b></text>
#Then store the second [1] result's text in 'Review Date'
                record ["Review Date"] = boldtags[1].text
                print record
#Now we grab all the <text ...> tags
                texttags = pdfxml.xpath('.//text')
                for text in texttags:
                    left = text.attrib.get('left')
                    #convert the attribute from a string into an integer:
                    leftinteger = int(left)
#IF leftinteger is between 96 and 99
#Literally? If 96 is smaller than leftinteger, and leftinteger is smaller than 99:
#see other options at http://stackoverflow.com/questions/618093/how-to-find-whether-a-number-belongs-to-a-particular-range-in-python

                    if 96 < leftinteger < 99:
                        #Record the text of 'text' (sorry)
                        record ["BOCUname"] = text.text
                        print record
                    if 324 < leftinteger < 327:
                        record ["Offences"] = text.text
                        print record
                    if 405 < leftinteger < 408:
                        record ["Sanction_detentions"] = text.text
                        print record
                    if 481 < leftinteger < 484:
                        record ["Sanction_detention_rate"] = text.text
                        print record
                    if 587 < leftinteger < 590:
                        record ["Offences FYTD_2011_12"] = text.text
                        print record
                    if 661 < leftinteger < 664:
                        record ["Offences FYTD_2012_13"] = text.text
                        print record
                    if 713 < leftinteger < 716:
                        record ["Offences percentage change"] = text.text
                        print record
                    if 812 < leftinteger < 815:
                        record ["Sanction detections FYTD 2011_12"] = text.text
                    if 887 < leftinteger < 890:
                        record ["Sanction Detections FYTD_2012_13"] = text.text
                    if 943 < leftinteger < 946:
                        record ["Sanction Detection rate FYTD 2011_12"] = text.text
                    if 1021 < leftinteger < 1024:
                        record ["Sanction Detections rate FYTD 2012_13"] = text.text
                        uniqueid = uniqueid+1
                        record ["uniqueid"] = uniqueid
                        print record
                        scraperwiki.sqlite.save(["uniqueid","Date"], record)                    
                    else:
                        print "NO DATA!"

#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    #runs another function - created earlier - on 'root'
    scrapetable(root)

#This will be used for relative links in later pages
baseurl = "http://www.met.police.uk/foi/"
#When added to the baseurl, this is our starting page 
startingurl = "c_priorities_and_how_we_are_doing.htm"

#Run the function created earlier above on that URL
scrape_and_look_for_next_link(baseurl+startingurl)


#COPY ACROSS CODE FROM PREVIOUS SCRAPER PT3