# collecting Case #, Decision #, Employer, Petitioner, Date Issued, Method, Number of Eligible Voters, unit description, outcome

###############################################################################
# Individual Page - Public Employee Relations Commission - WA (Python Version)
#
# This script scrapes data from Certification Decisions of the state of
# Washington for an individual page.  Eventually, the guts of this script
# will be migrated into Public Employee Relations Commission - WA
#
###############################################################################
## DEBUG .............. If you uncommment the next line, it could help you debug possible issues that appear
## YOU_SHOULD_KNOW .... You'll be able to use this later
## NOTE ............... general comments


## NOTE: required before any other code (comments not included)
import scraperwiki
import lxml.html


## YOU_SHOULD_KNOW: this is where you put your target url(s) 
BASE_URL   = 'http://www.perc.wa.gov/Databases/Certifications/10947.htm'
MAX_CERT   = 0  ## set to 0 for unlimited
FIRST_CERT = 0  ## first CERT to pull


## NOTE: scrape_table function gets passed an individual page to scrape
def scrape_cert_data(page_url):
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
                            for cell in td.cssselect('a'):
                                ## print "SEE YY %s" % cell.text_content()
                                print "SEE link %s" % cell.get('href')
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


# ---------------------------------------------------------------------------
# START HERE
# (1) Grab all the CERT links from BASE_URL
# (2) Start on FIRST_CERT and increment to FIRST_CERT + MAX_CERTS
# ---------------------------------------------------------------------------
all_certs = scrape_cert_data(BASE_URL)

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