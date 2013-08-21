###############################################################################
# Available commercial real estate in Santa Cruz, CA                           
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from time import sleep

data = []

i = 0

# Crawling commercial rentals in Santa Cruz
rooturl = "http://stlouis.craigslist.org/reo"

# Set initial crawl URL to root URL
crawlurl = rooturl

# While there are pages to crawl...
while crawlurl != "":

    # Retrieve the page
    soup = BeautifulSoup( scraperwiki.scrape( crawlurl ) )

    # Loop through all paragraph tags
    for p in soup('p' , {"align":None} ):

        # For sanity
        i = i + 1
        print "Retrieving listing #" + str(i)

        # Collect the listing's info
        listing = {}

        listing = {
            'listing_id':       "",
            'listing_title':    "",
            'listing_url':      "",
            'listing_price':    "",
            'listing_location': "",
            'listing_footage':  "",
            'listing_date':     "",
            'listing_description': ""
        }

        if p.font:
            # get location
            listing['listing_location'] =  re.subn(r"\(" , "" , re.subn(r"\)" , "" , p.font.text)[0] )[0]

        if p.a:
            # get title
            listing['listing_title'] = p.a.text

            # get price
            if re.search( re.compile('\$[0-9]+') , p.a.text ):
                price = re.search( re.compile('\$[0-9]+') , p.a.text ).group(0)
                # strip off the $ dollar sign
                listing['listing_price'] = price[1:]

            # get square footage
            if re.search( re.compile('/ [0-9]+'), p.a.text ):
                footage = re.search( re.compile('/ [0-9]+') , p.a.text).group(0)
                listing['listing_footage'] = footage[2:]
            
            if p.a['href']:
                # get url
                listing['listing_url'] = p.a['href']

                # get id
                if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                    listing['listing_id'] = int(re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0])

                # Retrieve the listing detail page
                soup_listing = BeautifulSoup( scraperwiki.scrape( listing['listing_url'] ) )

                for body in soup_listing('body'):
                    # get date
                    if re.search( re.compile('Date: [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]?[0-9]{1}:[0-9]{2}[AP]M [A-Z]{3}') , body.text ):
                        date = re.search( re.compile('Date: [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]?[0-9]{1}:[0-9]{2}[AP]M [A-Z]{3}') , body.text ).group(0)
                        listing['listing_date'] = date[6:]
                        
                    # get description
                    # TODO fix bug where the final partition isn't working
                    listing['listing_description'] = body.text.partition('[Errors when replying to ads?]')[2].partition('START CLTAGS')[0].partition('<!-- imgList = new Array')[0]

                    # TODO get address

        # Finally, throw the listing into data[]
        data.append(listing)
    
        # Deal with CL's occasional timeouts
        if i % 10 == 0:
            print "sleeping for 10 seconds..."
           # sleep(10)

    # Retrieve the URL for the next page
    nexturl = soup.find(text=re.compile("next 100 postings"))

    # Set next crawl URL
    if nexturl is not None:
        crawlurl = rooturl + nexturl.parent['href']
    else:
        crawlurl = ""

print data

# Write data to database
scraperwiki.sqlite.execute("""
DROP TABLE IF EXISTS `cl_sc_commercial_space`
""")

scraperwiki.sqlite.execute("""
CREATE TABLE `cl_sc_commercial_space`
(
    `listing_id`       int,
    `listing_title`    text,
    `listing_url`      text,
    `listing_price`    text,
    `listing_location` text,
    `listing_footage`  text,
    `listing_date`     text
)
""")

scraperwiki.sqlite.save(["listing_id"],data,"cl_sc_commercial_space")