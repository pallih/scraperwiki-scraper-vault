################################## Relax. Start Over ##########################################




###############################################################################
# Attempting to scrape Craigslist         
# lol.... I'm lost....                   
# OK, I'm going to start with just the cpg in my city this time....
# I only need the first 100 or so records since I'm updating the database regularly.
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from time import sleep

# variables.
# soupCityList - The soup for the city list
# soupPostList - The soup for the list of postings in a city
# soupPosting - The soup for the specific posting
# listCities - list of city records
# listPostings - list of posting records


# Set things up
data = []
i = 0

# ceate database
scraperwiki.sqlite.execute("""
DROP TABLE IF EXISTS `posting_data`
""")
scraperwiki.sqlite.execute("""
CREATE TABLE `posting_data`
(
    `listing_id`       int,
    `listing_title`    text,
    `listing_url`      text,
    `listing _email`    text,
    `listing_description` text,
    'listing_type'       text,
    'listing_city'       text,
    'listing_date'       text
    
)
""")

cityhref = "http://losangeles.craigslist.org/cpg/"
crawlurl = cityhref

# While there are pages to crawl...
while crawlurl != "":

    # Retrieve the page
    soup = BeautifulSoup( scraperwiki.scrape( crawlurl ) )

    # Loop through all paragraph tags
    for p in soup('p' , {"align":None} ):

        # For sanity
        i = i + 1
        print "Retrieving listing #" + str(i)
        # I like sanity!
                        
        # Collect the listing's info
        listing = {}
    
        listing = {
            'listing_id':       "",
            'listing_title':    "",
            'listing_url':      "",
            'listing_email':    "",
            'listing_description': "",
            'listing_type':     "cpg",
            'listing_loc':      "losangeles",
            'listing_date':        ""
        }

        if p.a:
            # get title
            listing['listing_title'] = p.a.text
            
            if p.a['href']:
                # get url
                listing['listing_url'] = p.a['href']

                # get id
                if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                    listing['listing_id'] = int(re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0])

                    # Retrieve the listing detail page
                    try:
                        soup_listing = BeautifulSoup( scraperwiki.scrape( listing['listing_url'] ) )
                    except:
                        if i % 10 == 0:
                            sleep(10)
                            soup_listing = BeautifulSoup( scraperwiki.scrape( listing['listing_url'] ) )
                    soup_listing.prettify()
                    for body in soup_listing('body'):
                        
                        # get date
                        if re.search( re.compile('Date: [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]?[0-9]{1}:[0-9]{2}[AP]M [A-Z]{3}') , body.text ):
                            date = re.search( re.compile('Date: [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]?[0-9]{1}:[0-9]{2}[AP]M [A-Z]{3}') , body.text ).group(0)
                            listing['listing_date'] = date[6:]
                        
                        
                        # get email
                        if re.search( re.compile(r'(mailto:).*(subject)'), body.prettify()):
                            email = re.search( re.compile(r'(mailto:).*(subject)'), body.prettify()).group(0)
                            listing['listing_email'] = email[7:43]
                        
                            # get description
                            # TODO fix bug where the final partition isn't working
                            listing['listing_description'] = body.text.partition('[Errors when replying to ads?]')[2].partition('START CLTAGS')[0].partition('<!-- imgList = new Array')[0]
                            # seems like it's working fine to me....
                        
        # Finally, throw the listing into data[]
                            data.append(listing)
    
                            if i % 100 == 0:
                                print "saving data..."
                                scraperwiki.sqlite.save(["listing_id"],data,"posting_data")
                                data = []
            
        # Deal with CL's occasional timeouts
        if i % 10 == 0:
            print "sleeping for 10 seconds..."
            sleep(10)

            
################################## Relax. Start Over ##########################################




###############################################################################
# Attempting to scrape Craigslist         
# lol.... I'm lost....                   
# OK, I'm going to start with just the cpg in my city this time....
# I only need the first 100 or so records since I'm updating the database regularly.
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from time import sleep

# variables.
# soupCityList - The soup for the city list
# soupPostList - The soup for the list of postings in a city
# soupPosting - The soup for the specific posting
# listCities - list of city records
# listPostings - list of posting records


# Set things up
data = []
i = 0

# ceate database
scraperwiki.sqlite.execute("""
DROP TABLE IF EXISTS `posting_data`
""")
scraperwiki.sqlite.execute("""
CREATE TABLE `posting_data`
(
    `listing_id`       int,
    `listing_title`    text,
    `listing_url`      text,
    `listing _email`    text,
    `listing_description` text,
    'listing_type'       text,
    'listing_city'       text,
    'listing_date'       text
    
)
""")

cityhref = "http://losangeles.craigslist.org/cpg/"
crawlurl = cityhref

# While there are pages to crawl...
while crawlurl != "":

    # Retrieve the page
    soup = BeautifulSoup( scraperwiki.scrape( crawlurl ) )

    # Loop through all paragraph tags
    for p in soup('p' , {"align":None} ):

        # For sanity
        i = i + 1
        print "Retrieving listing #" + str(i)
        # I like sanity!
                        
        # Collect the listing's info
        listing = {}
    
        listing = {
            'listing_id':       "",
            'listing_title':    "",
            'listing_url':      "",
            'listing_email':    "",
            'listing_description': "",
            'listing_type':     "cpg",
            'listing_loc':      "losangeles",
            'listing_date':        ""
        }

        if p.a:
            # get title
            listing['listing_title'] = p.a.text
            
            if p.a['href']:
                # get url
                listing['listing_url'] = p.a['href']

                # get id
                if re.search( r"/([\d]+)\.html" , p.a['href'] ):
                    listing['listing_id'] = int(re.subn( r"\.html","", re.subn( r"/" ,"", re.search( r"/([\d]+)\.html" , p.a['href'] ).group(0) )[0] )[0])

                    # Retrieve the listing detail page
                    try:
                        soup_listing = BeautifulSoup( scraperwiki.scrape( listing['listing_url'] ) )
                    except:
                        if i % 10 == 0:
                            sleep(10)
                            soup_listing = BeautifulSoup( scraperwiki.scrape( listing['listing_url'] ) )
                    soup_listing.prettify()
                    for body in soup_listing('body'):
                        
                        # get date
                        if re.search( re.compile('Date: [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]?[0-9]{1}:[0-9]{2}[AP]M [A-Z]{3}') , body.text ):
                            date = re.search( re.compile('Date: [0-9]{4}-[0-9]{2}-[0-9]{2}, [0-9]?[0-9]{1}:[0-9]{2}[AP]M [A-Z]{3}') , body.text ).group(0)
                            listing['listing_date'] = date[6:]
                        
                        
                        # get email
                        if re.search( re.compile(r'(mailto:).*(subject)'), body.prettify()):
                            email = re.search( re.compile(r'(mailto:).*(subject)'), body.prettify()).group(0)
                            listing['listing_email'] = email[7:43]
                        
                            # get description
                            # TODO fix bug where the final partition isn't working
                            listing['listing_description'] = body.text.partition('[Errors when replying to ads?]')[2].partition('START CLTAGS')[0].partition('<!-- imgList = new Array')[0]
                            # seems like it's working fine to me....
                        
        # Finally, throw the listing into data[]
                            data.append(listing)
    
                            if i % 100 == 0:
                                print "saving data..."
                                scraperwiki.sqlite.save(["listing_id"],data,"posting_data")
                                data = []
            
        # Deal with CL's occasional timeouts
        if i % 10 == 0:
            print "sleeping for 10 seconds..."
            sleep(10)

            
