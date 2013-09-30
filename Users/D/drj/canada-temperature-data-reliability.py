# David Jones, Climate Code Foundation, 2011-09-07
# Scrapes the run history of canada-temperature-data.

import collections
import itertools
import json
import urllib

import scraperwiki

target = 'canada-temperature-data'

def getruns(scraper):
    """Get all the runs for the scraper."""
    # See https://scraperwiki.com/docs/api#getinfo

    start = "2011-08-17" # When I fixed the scraper to work with new datastore.
    d, = json.load(urllib.urlopen(
        "https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=%(scraper)s&history_start_date=%(start)s&quietfields=datasummary%%7Ccode" % locals()))
    return d['runevents']

def get_exception(run):
    """The exception from the run, or '' if there is no exception."""

    return run.get("exception_message", '')

runs = [x for x in getruns(target) if not x['still_running']]
exceptcount = collections.defaultdict(int)
for exception,group in itertools.groupby(sorted(runs, key=get_exception), get_exception):
    exceptcount[exception] += len(list(group))

for k,v in sorted(exceptcount.iteritems()):
    print v, k# David Jones, Climate Code Foundation, 2011-09-07
# Scrapes the run history of canada-temperature-data.

import collections
import itertools
import json
import urllib

import scraperwiki

target = 'canada-temperature-data'

def getruns(scraper):
    """Get all the runs for the scraper."""
    # See https://scraperwiki.com/docs/api#getinfo

    start = "2011-08-17" # When I fixed the scraper to work with new datastore.
    d, = json.load(urllib.urlopen(
        "https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=%(scraper)s&history_start_date=%(start)s&quietfields=datasummary%%7Ccode" % locals()))
    return d['runevents']

def get_exception(run):
    """The exception from the run, or '' if there is no exception."""

    return run.get("exception_message", '')

runs = [x for x in getruns(target) if not x['still_running']]
exceptcount = collections.defaultdict(int)
for exception,group in itertools.groupby(sorted(runs, key=get_exception), get_exception):
    exceptcount[exception] += len(list(group))

for k,v in sorted(exceptcount.iteritems()):
    print v, k