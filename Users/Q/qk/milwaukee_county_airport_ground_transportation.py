import scraperwiki
         
html = scraperwiki.scrape("http://www.mitchellairport.com/mobile")

import lxml.html           
root = lxml.html.fromstring(html)

#find ground transport
for content in root.cssselect("div[id='content-transportation']"):

    #get headings
    allTransTypes = content.cssselect("h1")
    num = 0

    #loop over types
    for transType in allTransTypes:
        print "TYPE: " + transType.text

        #loop over options
        transOptions = content.cssselect("ul")[num]
        for option in transOptions.cssselect("li"):

            linkNum = 0
            #loop over links
            for link in option.cssselect("a"):
                if isinstance(link.text, basestring):
                    print "ANCHOR: " + str(linkNum) + ": " + link.text
                linkNum += 1
        num += 1
import scraperwiki
         
html = scraperwiki.scrape("http://www.mitchellairport.com/mobile")

import lxml.html           
root = lxml.html.fromstring(html)

#find ground transport
for content in root.cssselect("div[id='content-transportation']"):

    #get headings
    allTransTypes = content.cssselect("h1")
    num = 0

    #loop over types
    for transType in allTransTypes:
        print "TYPE: " + transType.text

        #loop over options
        transOptions = content.cssselect("ul")[num]
        for option in transOptions.cssselect("li"):

            linkNum = 0
            #loop over links
            for link in option.cssselect("a"):
                if isinstance(link.text, basestring):
                    print "ANCHOR: " + str(linkNum) + ": " + link.text
                linkNum += 1
        num += 1
