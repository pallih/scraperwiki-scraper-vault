###############################################################################
# Public Employee Relations Commission (Python Version)
#
# This script scrapes data from Certification Decisions of the state of
# Washington.
#
###############################################################################
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments


## NOTE: required before any other code (comments not included)
import scraperwiki
import lxml.html


## YOU_SHOULD_KNOW: this is where you put your target url(s) 
BASE_URL   = 'http://www.perc.wa.gov/hearings-decisions.asp'
MAX_CERT   = 0  ## set to 0 for unlimited
FIRST_CERT = 0  ## first CERT to pull


## NOTE: scrape_table function gets passed an individual page to scrape
def scrape_all_cert_links(page_url):
    print "I SEE %s" % (page_url)

    ## NOTE: first, scrape the page
    page = scraperwiki.scrape(page_url)

    ## NOTE: next, parse the scraped page
    root = lxml.html.fromstring(page)

    ## NOTE: instead of figuring out which table we care about,
    ## we know we want the 2nd table and look for that.
    table_cnt = 0;
    for table in root.cssselect('table'):
        if table_cnt == 1:
            print "hello table two"
            tr_cnt = 0
            for tr in table:
                if tr_cnt == 1:
                    print "SEE ZZ %s" % tr
                    td_cnt = 0
                    for td in tr:
                        if td_cnt == 1:
                            print "SEE XX %s" % td
                            cell_cnt = 1
                            for cell in td.cssselect('a'):
                                ## print "SEE YY %s" % cell.text_content()
                                print "%4d) link %s" % (cell_cnt, cell.get('href'))
                                cell_cnt += 1
                        else:
                            pass
                        td_cnt += 1
                else:
                    pass
                tr_cnt += 1

        else:
            pass

        table_cnt += 1


    data = {
          'MyKey'    : "a",
          'Business' : "b",
    }
    scraperwiki.sqlite.save(unique_keys=['MyKey'], data=data)


## NOTE: scrape_all_certs function grabs all CERT links on passed link
##       and returns the links in an array
def xxscrape_all_certs(page_url):

    ## NOTE: first, scrape the page
    page = scraperwiki.scrape(page_url)

    ## NOTE: next, parse the scraped page
    root = lxml.html.fromstring(page)

    ## NOTE: loop through each listing block delimited by 'div="listing content"'
    for x in root.cssselect('table'):
        print "SEE %s" % x
        # global DATA_KEY  ## NOTE: access the global var DATA_KEY to later increment

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
        # data = {
        #   'MyKey'    : DATA_KEY,
        #  'Business' : check_data(x.cssselect('.business-name')),
        #  'Address'  : check_data(x.cssselect('span.street-address')),
        #  'City'     : check_data(x.cssselect('span.locality')),
        #  'State'    : check_data(x.cssselect('span.region')),
        #  'Zipcode'  : check_data(x.cssselect('span.postal-code')),
        #  'Phone'    : check_data(x.cssselect('span.business-phone')),
        # }
        ## OLDWAY ## scraperwiki.sqlite.save(unique_keys=['Business'], data=data)
        # scraperwiki.sqlite.save(unique_keys=['MyKey'], data=data)
        # DATA_KEY += 1
        ## DEBUG: print "I SEE %d" % (DATA_KEY)
        
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
        next_link = None  ## default for next link to avoid error
        for links in root.cssselect('li.next a'):
            next_link = "%s%s" % (BASE_URL, links.get('href'))

    ## DEBUG: print "B: SEE %s, %s" % (MAX_PAGES, CURRENT_PAGE)
    return next_link


# ---------------------------------------------------------------------------
# START HERE
# (1) Grab all the CERT links from BASE_URL
# (2) Start on FIRST_CERT and increment to FIRST_CERT + MAX_CERTS
# ---------------------------------------------------------------------------
all_certs = scrape_all_cert_links(BASE_URL)

if all_certs is None:
    max_cert  = 0
    all_certs = []
elif MAX_CERT == 0:
    max_cert  = len(all_certs)
else:
    max_cert  = MAX_CERT

for link in all_certs:
    parse_cert_link(link)
    ## break if cnt > max_cert

print "all done!"