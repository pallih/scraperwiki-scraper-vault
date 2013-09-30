import scraperwiki, sys
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("test_1_6")

links = scraperwiki.sqlite.select("URL from `test_1_6`.swdata")

for link in links:
    url = link["URL"]
    print url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    
    title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
    print title

    ps = soup.find_all("p", "clearfix")
    
    for p in ps:
        span_text = ""
        span = p.find("span")
        if span:
            span_text = span.get_text().strip()
            span.clear()
        if span_text != "":
            info = p.get_text().strip()
            #print span_text
            #print info

            if span_text == "Reference number:":
                ref = info
                print "Reference Number is: " + ref
            elif span_text == "Estimated length of contract:":
                length = info
                print "Contract Length is: " + length
            elif span_text == "Awarded value":
                value = info
                print "Awarded Value is: " + value
            elif span_text == "Location where the contract is to be carried out:":
                location = info
                print "Contract Location is: " + location
            elif span_text == "Name of the buying organisation:":
                buyer = info
                print "Buying Organisation is: " + buyer
            elif span_text == "Is it a framework agreement?":
                framework = info
                print "Is it a framework agreement? " + framework
            elif span_text == "Contracted length of the contract":
                contracted = info
                print "Contracted Length is: " + contracted
            elif span_text == "Awarded on:":
                awardedon = info
                print "Awarded on: " + awardedon
            elif span_text == "Nature of procurement":
                procurement = info
                print "Nature of Procurement is: " + procurement
                


import scraperwiki, sys
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("test_1_6")

links = scraperwiki.sqlite.select("URL from `test_1_6`.swdata")

for link in links:
    url = link["URL"]
    print url

    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    
    title = soup.find("h2", "legend-edit").get_text().replace("English", "").strip()
    print title

    ps = soup.find_all("p", "clearfix")
    
    for p in ps:
        span_text = ""
        span = p.find("span")
        if span:
            span_text = span.get_text().strip()
            span.clear()
        if span_text != "":
            info = p.get_text().strip()
            #print span_text
            #print info

            if span_text == "Reference number:":
                ref = info
                print "Reference Number is: " + ref
            elif span_text == "Estimated length of contract:":
                length = info
                print "Contract Length is: " + length
            elif span_text == "Awarded value":
                value = info
                print "Awarded Value is: " + value
            elif span_text == "Location where the contract is to be carried out:":
                location = info
                print "Contract Location is: " + location
            elif span_text == "Name of the buying organisation:":
                buyer = info
                print "Buying Organisation is: " + buyer
            elif span_text == "Is it a framework agreement?":
                framework = info
                print "Is it a framework agreement? " + framework
            elif span_text == "Contracted length of the contract":
                contracted = info
                print "Contracted Length is: " + contracted
            elif span_text == "Awarded on:":
                awardedon = info
                print "Awarded on: " + awardedon
            elif span_text == "Nature of procurement":
                procurement = info
                print "Nature of Procurement is: " + procurement
                


