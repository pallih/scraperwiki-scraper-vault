####
# WARN notices are mass layoff actions reported to the state of Kansas.
# Please note that *reported* mass layoffs are only a subset of mass
# layoffs--there's essentially no enforcement of this law. Use BLS mass layoffs
# if you want better accuracy. 
# For more info, see: http://www.doleta.gov/layoff/warn.cfm
# This will only work for result sets with less than 125 results -- they've got
# crazy pagination past 5 pages, but it shouldn't be too hard to adapt to make
# it work with more. You should have no problem grabbing a year of results
# at a time. The detail pages seem to break beautifulsoup. Instead of trying
# to repair, I just hacked past it with some regexes. The detail pages
# seem quite consistent.
# Hacked up by Jacob Fenton at investigativereportingworkshop.org
# as an excuse to test-drive scraperwiki.
####

import scraperwiki
import mechanize
import cookielib
import re
import time

class KansasWARNScraper():

    # regexes we'll use to parse pages
    spanre = re.compile("<span class=\"blTransparent\">.*?</span>")
    alltags = re.compile("\<.*?\>")

    def __init__(self):

        # Set up the browser. For more, info see:
        # http://stockrt.github.com/p/emulating-a-browser-in-python-with-mechanize/

        self.browser = mechanize.Browser()

        # Set up cookies--the site won't work without them
        self.cj = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cj)

        # Browser options
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        # Ignore their robots settings. This is public data, people
        self.browser.set_handle_robots(False)
        # Turn debugging on for gory details of http
        self.browser.set_debug_http(False)
        self.browser.set_debug_redirects(True)
        self.browser.set_debug_responses(True)

        # Set the user agent they'll see in their logs.
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # Remove a few html tags from chunk we grabbed
    def clean_tags(self, arg):
        return re.sub(self.alltags, "", arg)

    # The detail pages seem to break beautifulsoup, so hack through 'em by hand with regexes
    def _handle_detail_page(self, detail_page):
        found = self.spanre.findall(detail_page)
        company = self.clean_tags(found[1])
        address = self.clean_tags(found[3])
        city = self.clean_tags(found[5])
        state = self.clean_tags(found[7])
        zip_code = self.clean_tags(found[9])
        number_affected = self.clean_tags(found[11])
        notice_date = self.clean_tags(found[13])
        line = "|".join([company, address, city, state, zip_code, number_affected, notice_date])
        print "Retrieved data: %s" % (line)
        # Outside of scraperwiki, would save this to a file
        # Not sure this is the best way to use scraperwiki, but it works here.
        # We're not using a schema this way--all fields are text--but that's fine here
        # Also, not using Kansas' canonical id--but mashing all fields works.
        scraperwiki.sqlite.save(['company', 'address', 'city', 'state', 'ZIP', 'number_affected', 'notice_date'], {"company": company, "address": address, "city": city, "state": state, "ZIP": zip_code, "number_affected": number_affected, "notice_date": notice_date})

    def scrape(self, start_date, end_date):
        print "Scraping time range: %s - %s" % (start_date, end_date)
        # start with a referring page--it complains about cookies otherwise.
        referring_page = "https://www.kansasworks.com/ada/mn_warninfo_dsp.cfm?"
        r = self.browser.open(referring_page)
        # Follow the link to the search page
        for link in self.browser.links(url_regex="/ada/mn_warn_dsp"):
            r = self.browser.follow_link(link)

        # We want the first form on the page:
        self.browser.select_form(nr=0)

        # Obviously there are other searches possible, but I'm just doing this by year
        self.browser["startdate"] = start_date
        self.browser["enddate"] = end_date
        self.browser.submit()

        # Track which page we're on, how many results we've read,
        # and whether to keep reading.
        result_page = 1
        keep_reading = True
        result_count = 1

        while (keep_reading):
            ## because the details are all buried on the details page, click through to every page, and save it.
            for link in self.browser.links(url_regex="mn_warn_dsp\.cfm"):
                if ('id=' in link.url):
                    print " Following link: %s" % (link)

                    self.browser.follow_link(link)
                    this_page = self.browser.response().read()
                    self._handle_detail_page(this_page)
                    # Be nice to their servers
                    print "sleeping for 1 second"
                    time.sleep(1)
                    # Go back to the previous page
                    self.browser.back()

            # Stop reading unless there's another page of results.
            keep_reading = False

            # Their pagination system uses numbered pages--so we're looking for the next page of results
            # Stuff gets weird after 5 pages, but this isn't a problem when grabbing a single year or two of results.
            for link in self.browser.links(url_regex="securitysys"):
                if (link.text == str(result_page + 1)):
                    result_page += 1
                    keep_reading = True
                    r = self.browser.follow_link(link)
                    break

# Code executed in scaperwiki isn't called main, hence:
if __name__ == 'scraper':
    scraper = KansasWARNScraper()
    # Dates must be in MM/DD/YYYY format
    scraper.scrape("01/01/2008", "12/31/2009")

