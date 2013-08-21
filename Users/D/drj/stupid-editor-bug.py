# David Jones, Climate Code Foundation, 2011-09-07
# Scrapes the run history of canada-temperature-data.

import json
import urllib

import scraperwiki

target = 'canada-temperature-data'
# Hi.  Put your cursor at the beginning of this line.  Then press "down arrow" a few times, and see
# if you can get to the bottom of the file.

def getruns(scraper):
    """Get all the runs for the scraper."""
    # See https://scraperwiki.com/docs/api#getinfo

    d = json.load(urllib.urlopen(
        "https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=%(scraper)s&history_start_date=1999-01-01&quietfields=datasummary%&Ccode" % locals()))
    return d['runevents']

# Well, I can't get past the line with the ridiculously long string, but maybe that's just me
# using Chrome on OS X.  Does it work for you?

# As pointed out, definitely doesn't work correctly in webkit on OSX - does however do the right thing 
# in FF 3.6, which is annoying. Also appears to still be working in FF 6.0.2.

