#NEED TO: Grab 'next' links and store results - URL doesn't change
#CYCLE through alphabet adding to base URL for searches

#import the libraries we'll need
import re
import scraperwiki
import urllib2
import lxml.etree
import lxml.html



#This creates a new function to scrape the initial page so we can grab report titles and the links
def scrape_and_look_for_next_link(url):
    #scrapes the page and puts it in 'html'
    html = scraperwiki.scrape(url)
    print html
    #turns html from a string into an lxml object called 'root'
    root = lxml.html.fromstring(html)
    pdflinks = root.cssselect("table.results_grid")
    for link in pdflinks:
        print link.text_content()
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
scrape_and_look_for_next_link("http://architects-register.org.uk/search/company/c")
