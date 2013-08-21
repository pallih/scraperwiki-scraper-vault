###############################################################################
# MI Interpreters - the Python Version
#
# This script starts on the first page and then
# scrapes it and all subsequent pages by calling
# 'scrape_and_look_for_next_link' over and over
# again.
#
###############################################################################
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments


## NOTE: required before any other code (comments not included)
import scraperwiki
import lxml.html


## YOU_SHOULD_KNOW: this is where you put your target url(s) 
BASE_URL  = 'http://www.yellowpages.com'
FIRST_EXT = '/mi/interpreters?g=MI'
MAX_PAGES    = 0  ## set to 0 for unlimited
CURRENT_PAGE = 0  ## keeps track of current page


## NOTE: the intermediate function "check_data()" was required because
## not all the fields are filled for all businesses and I was getting
## errors when trying to add the data.
def check_data(data):
    if len(data) > 0:
        ## NOTE: pull out first element, get its text, remove end whitespace
        ## and then remove trailing ',' if it exists (like on addresses)
        return data[0].text_content().rstrip().rstrip(',')
    else:
        ## NOTE: otherwise, return 'n/a'
        return "n/a"


## NOTE: scrape_table function gets passed an individual page to scrape
def scrape_table(page_url):

    ## NOTE: first, scrape the page
    page = scraperwiki.scrape(page_url)

    ## NOTE: next, parse the scraped page
    root = lxml.html.fromstring(page)

    ## NOTE: loop through each listing block delimited by 'div="listing content"'
    for x in root.cssselect('.listing_content'):
        ## DEBUG: make sure we are seeing the correct data
        # print "SEE %s" % x
        # print "GOT %s" % x.text_content()
        # print "BIZ %s" % check_data(x.cssselect('.business-name'))
        # print "BIZ %s" % check_data(x.cssselect('.business-name'))
        # print "ADR %s" % check_data(x.cssselect('span.street-address'))
        # print "CIT %s" % check_data(x.cssselect('span.locality'))
        # print "STA %s" % check_data(x.cssselect('span.region'))
        # print "ZIP %s" % check_data(x.cssselect('span.postal-code'))
        # print "PHN %s" % check_data(x.cssselect('span.business-phone'))

        ## NOTE: the intermediate function "check_data()" was required because
        ## not all the fields are filled for all businesses and I was getting
        ## errors when trying to add the data.
        data = {
          'Business' : check_data(x.cssselect('.business-name')),
          'Address'  : check_data(x.cssselect('span.street-address')),
          'City'     : check_data(x.cssselect('span.locality')),
          'State'    : check_data(x.cssselect('span.region')),
          'Zipcode'  : check_data(x.cssselect('span.postal-code')),
          'Phone'    : check_data(x.cssselect('span.business-phone')),
        }
        scraperwiki.sqlite.save(unique_keys=['Business'], data=data)


    ## YOU_SHOULD_KNOW: if you would like to a global variable, be sure
    ## to define the variable locally with 'global' (like below).  If
    ## you only plan on reading the variable, there is no need to set
    ## the global definition (like with MAX_PAGES below)
    global CURRENT_PAGE
    ## DEBUG: print "A: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    CURRENT_PAGE += 1

    ## NOTE: check to see if there are more links to follow
    if MAX_PAGES == CURRENT_PAGE:
        next_link = None
    else:
        for links in root.cssselect('li.next a'):
            next_link = "%s%s" % (BASE_URL, links.get('href'))

    ## DEBUG: print "B: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    return next_link


## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    # print 'scraping: '+url
    next_url = scrape_table(url)

    if next_url:
        scrape_and_look_for_next_link(next_url)



# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = "%s%s" % (BASE_URL,FIRST_EXT)
## DEBUG: make sure I found the page
# print "I SEE URL: %s" % starting_url
scrape_and_look_for_next_link(starting_url)