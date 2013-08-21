import scraperwiki

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that


import scraperwiki
import requests
import lxml.html

def scrape_people():
## going through each page
    for i in range(1,15):
## remember: when you see a % in a string followed by % it means "insert in"
## i only exists as long as we're inside the loop
        print "scraping page %s" % i
## the dom has a lot of elements, but we only want to have the "text" element, thats why ".text"
        r = requests.get('http://www.hyperisland.com/people?filter=true&page=%s&role=student' % i).text
## parsing it with library lxml.html (to get this html from before) into a dom to be able to select it
        dom = lxml.html.fromstring(r)
## "for every element in" this list (which is all the headings) "do something" (printing all names) - all names wrapped in h6's
        for name in dom.cssselect('h6'):
            print name.text
## creating a row to put into the database, simple columns with their name
            d = { 'name': name.text }
## use the scraperwiki library from the top and then save the rows there
            scraperwiki.sqlite.save(['name'], d)

scrape_people()

## IMPORTANT: Python uses no {} like Java/Javascript but rather Einschiebungen (with Tabs) really important that Python knows which is in which!!!!

## Alternatives to %

## 1. print 'scraping page ' + i ## not working, raising an error

## 2. print 'scraping page ' + str(i) ## works

## 3. print 'scraping page %s' % i ## works and elegant





