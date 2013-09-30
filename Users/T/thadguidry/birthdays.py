# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import lxml.html, lxml.etree
import re
import datetime
from time import sleep

# INITIALIZE
global d
d = datetime.date(2001,1,1)
url = "http://www.famouswhy.com/Born_Today/1/1/1/1.html"


    # place your cssselection case here and extract the values
def parse_page(url):


    root = lxml.html.parse(url).getroot()
    pages = root.cssselect('a.pagerLinkStyle') # Get an array of all the individual page number urls
#    print "LAST PAGE: " + pages[-2].attrib["href"]

    for link in pages: # Loop through all pages in the array

        link_str = link.attrib["href"] # Get the current page link we are now scraping.
#        print "LINK STR:" + link_str
        last_page = pages[-2].attrib["href"] # Get the 2nd to last page url to scrape (instead of getting very last, which is just the NEXT)
#        print "LAST PAGE: " + last_page
        
#        print "PROCESSING PAGE: " + link.attrib["href"]

        page = lxml.html.parse(link.attrib["href"]).getroot()

        for rows in page.cssselect('table.bk_date_user'):
            record = {}
            record['Name'] = rows.cssselect('a.class_font.link_month')[0].text.strip()
            record['Birthday'] = rows.cssselect('td.data_burn_of_user')[0].text.strip()
            record['NotableType'] = rows.cssselect('td.data_burn_of_user br')[0].tail.strip()
            record['URL'] = rows.cssselect('a.class_font.link_month')[0].attrib["href"].strip()
        
            scraperwiki.sqlite.save(['URL'], record)

        sleep(3) # Sleep 3 seconds so that the server being scraped is not hit very hard

        if link_str == last_page: # Compare if last_page has been reached, if so update url
            next_day_url()


# Update URL to be scraped by 1 day, function checks for January 1, 2002 and STOPS when reached
def next_day_url():

    global d
    d = d + datetime.timedelta(days=1)
    day = d.strftime("%d") #if needed add .lstrip("0")
    month = d.strftime("%m") # if needed add .lstrip("0")

    url = "http://www.famouswhy.com/Born_Today/" + month + "/" + day + "/1/1.html"

    #STOP when January 1, 2002 is reached, because we now have all 365 days of Birthdays.
    if d == datetime.date(2002,1,1):
        print "done"

    else:
#        print "NEXT BIRTHDAY: " + url
        parse_page(url)


# START MAIN

parse_page(url)


                        

# Starting script to get you going fast.  
# Delete code as appropriate

import scraperwiki
import lxml.html, lxml.etree
import re
import datetime
from time import sleep

# INITIALIZE
global d
d = datetime.date(2001,1,1)
url = "http://www.famouswhy.com/Born_Today/1/1/1/1.html"


    # place your cssselection case here and extract the values
def parse_page(url):


    root = lxml.html.parse(url).getroot()
    pages = root.cssselect('a.pagerLinkStyle') # Get an array of all the individual page number urls
#    print "LAST PAGE: " + pages[-2].attrib["href"]

    for link in pages: # Loop through all pages in the array

        link_str = link.attrib["href"] # Get the current page link we are now scraping.
#        print "LINK STR:" + link_str
        last_page = pages[-2].attrib["href"] # Get the 2nd to last page url to scrape (instead of getting very last, which is just the NEXT)
#        print "LAST PAGE: " + last_page
        
#        print "PROCESSING PAGE: " + link.attrib["href"]

        page = lxml.html.parse(link.attrib["href"]).getroot()

        for rows in page.cssselect('table.bk_date_user'):
            record = {}
            record['Name'] = rows.cssselect('a.class_font.link_month')[0].text.strip()
            record['Birthday'] = rows.cssselect('td.data_burn_of_user')[0].text.strip()
            record['NotableType'] = rows.cssselect('td.data_burn_of_user br')[0].tail.strip()
            record['URL'] = rows.cssselect('a.class_font.link_month')[0].attrib["href"].strip()
        
            scraperwiki.sqlite.save(['URL'], record)

        sleep(3) # Sleep 3 seconds so that the server being scraped is not hit very hard

        if link_str == last_page: # Compare if last_page has been reached, if so update url
            next_day_url()


# Update URL to be scraped by 1 day, function checks for January 1, 2002 and STOPS when reached
def next_day_url():

    global d
    d = d + datetime.timedelta(days=1)
    day = d.strftime("%d") #if needed add .lstrip("0")
    month = d.strftime("%m") # if needed add .lstrip("0")

    url = "http://www.famouswhy.com/Born_Today/" + month + "/" + day + "/1/1.html"

    #STOP when January 1, 2002 is reached, because we now have all 365 days of Birthdays.
    if d == datetime.date(2002,1,1):
        print "done"

    else:
#        print "NEXT BIRTHDAY: " + url
        parse_page(url)


# START MAIN

parse_page(url)


                        

