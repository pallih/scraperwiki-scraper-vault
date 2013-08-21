import scraperwiki
from bs4 import BeautifulSoup

import string
import urlparse

url = "http://www.nyc.gov/html/cau/html/cb/cb.shtml"

html = scraperwiki.scrape(url)
soup = BeautifulSoup(html)

## In this case I know (because I looked at the page source), that we're looking for one 
## td with the id attribute "main_content" and then we want to find the paragraphs within 
## that block of HTML.

# first, find the "main_content" cell
lump = soup.find("td", id="main_content");

# then find all the paragraphs within that block of HTML
paragraphs = lump.find_all("p")

## how many paragraphs did it find? 
print "This page has", len(paragraphs), "paragraphs."

## what is in those paragraphs?
for para in paragraphs:
    print para.get_text()

## The second paragraph, or paragraphs[1] in our list syntax has the actual community boards. 
## We can find the "anchors" in that paragraph and pull out their "href" attributes
## to see the full list of pages we want to scrape.
for anchor in paragraphs[1].find_all("a"):
    print anchor['href']
    print urlparse.urljoin(url,anchor['href'])
    
## Create an empty list (or array).
boro_urls = []

## Instead of printing the URLs to the screen, append them to our list.
for anchor in paragraphs[1].find_all("a"):
    boro_urls.append(urlparse.urljoin(url,anchor['href']))

## Now comes the fun part. For every boro in our boro_urls list, we're going to do some scraping. 
for boro in boro_urls:
    html = scraperwiki.scrape(boro)
    soup = BeautifulSoup(html)
    print soup.title.get_text()
    print boro
    ## we just want one kind of table, the cb_table class
    cb_tables = soup.find_all("table", {"class":"cb_table"})
    print "There are", len(cb_tables), "in this borough."
    ## now this all starts to look a whole lot like https://scraperwiki.com/scrapers/foreclosures --
    ## we know how to put the rows from a table into a data store!
    for table in cb_tables:
        rows = table.find_all('tr')
        cb_name = rows[0].get_text()
        neighborhoods = rows[1].find_all("td")[2].get_text()
        cb_info = rows[2].find_all("td")[1].get_text()
        precincts = rows[3].find_all("td")[1].get_text()
        precinct_phones = rows[4].find_all("td")[1].get_text()
        print cb_name
        print neighborhoods
        print cb_info
        print precincts
        print precinct_phones

