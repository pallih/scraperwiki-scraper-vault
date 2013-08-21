###############################################################################
# Scape planning applications to Bristol City council
###############################################################################

import re
import urlparse
import urllib
import traceback
from urllib2 import URLError
from datetime import datetime, date, timedelta

from BeautifulSoup import BeautifulSoup as Soup
import mechanize

try:
    import scraperwiki
except ImportError:
    from scraper_utils import *

SEARCH_FORM=u"hhttp://e2eweb.bristol-city.gov.uk/PublicAccess/tdc/DcApplication/application_searchform.aspx"
br = mechanize.Browser()


class PlanningApp(dict):
    unique_keys = [u'Application Reference']

    @property
    def latlng(self):
        from scraperwiki import geo
        return geo.gb_postcode_to_latlng(
            geo.extract_gb_postcode(self[u'Address of Proposal']))

    @property
    def date(self):
        return self[u'Date Application Received']

# the links on the next button on a search form contain spaces
def scrub_link(url):
    "remove spaces and re-encode url"
    pr = urlparse.urlparse(url)
    pqs = urlparse.parse_qs(pr.query)
    npr = list(pr)
    npr[4] = urllib.urlencode(pqs, doseq=True) # that's the query string
    return urlparse.urlunparse(npr)

def site_link(rel_url, site_url=SEARCH_FORM):
    "Full url (based the same place as SEARCH_FORM) for rel_url"
    return urlparse.urljoin(site_url, rel_url).replace(" ", "%20")

def val(tag):
    "value of a (form control) tag"
    if tag.name == u'textarea':
        return tag.string
    return tag["value"]

def err_msg(soup):
    msg = soup.find('div', id="nonJavaScriptErrorMessage")
    if msg:
        return u" ".join(msg.findAll(text=True))
    return ""

def strpdate(string, format="%d/%m/%Y"):
    return datetime.strptime(string, format).date()

def strfdate(d, format="%d/%m/%Y"):
    return d.strfdate(format)


def labeled_values(tag):
    "Find all form controls with labels (using label-for), and return a dict mapping label -> value"
    labels = [lbl for lbl in tag.findAll('label')]
    tag_val = lambda field: val(tag.find(id=field))
    return dict((lbl.string, tag_val(lbl["for"])) for lbl in labels)


def scrape_detail(soup):
    "dict of values scraped from a detail page"
    rec = {}
    for tbl in soup.findAll('table', id=re.compile(r"TC\d")):
        rec.update(labeled_values(tbl))
    return rec

def scrape_search(soup):
    "Soup of every details page in search result"
    # if there are no results PublicAccess consideres this an error
    if u"search returned no results" in err_msg(soup):
        return

    # there's summary data in the table, but nothing we can't get from
    # the detail records, so we just scrape them
    tbl = soup.find('table', attrs={"class": "cResultsForm" })
    for anchor in tbl.findAll('a', href=re.compile(r".*application_detailview.*")):
        yield site_link(anchor['href'])

    # do the next page of results
    try:
        nxt = soup.find('a', id="A_nextpage")
        if nxt:
            print "NEXT NEXT NEXT " + site_link(nxt["href"])
            for link in scrape_search(Soup(br.open(site_link(nxt['href'])))):
                yield site_link(link)
    except URLError:
        pass


def applications(from_date, to_date):
    "Submit search form and return search result soup"
    br.open(SEARCH_FORM)
    br.select_form(name="searchform")
    # search date received start
    br["srchDateReceivedStart"] = from_date.strftime("%d/%m/%Y")
    br["srchDateReceivedEnd"] = to_date.strftime("%d/%m/%Y")
    resp = br.submit(id="btnSubmitSearchForm")
    return Soup(resp.get_data())



def walk(from_date, to_date):
    def scour(url):
        return url, Soup(scraperwiki.scrape(url))

    for url, soup in (scour(url) for url in scrape_search(applications(from_date, to_date))):
        print "walk", url
        try:
            rec = scrape_detail(soup)
            rec["url"] = url
            yield rec
        except Exception:
            print "Failed to parse %s" % url
            traceback.print_exc()

default_cleanups = (
    (r'No Details', lambda x: None),
    (r'\d{1,2}/\d{1,2}/\d{2,4}', lambda d: strpdate(d, u'%d/%m/%Y')),
    (r'Yes|No', lambda s: s == "Yes"))

def clean(rec, rclass=PlanningApp, cleanups=default_cleanups):
    "Clean up a record ready to save to scraperwiki"
    def c_label(l):
        return l[:-1] if l[-1] == ":" else l
    def c_val(v):
        for rex, parse in cleanups:
            if re.match(rex, v):
                return parse(v)
        return v
    return rclass((c_label(k), c_val(v)) for k,v in rec.items())

def sw_save(rec):
    try:
        from scraperwiki.datastore import save
        save(rec.unique_keys, rec, rec.date, rec.latlng)
    except ImportError:
        print "save", rec


# 10/8/2010 - 15/8/2010 will return results
def main(from_d=None, to_d=None):
    from_date = strpdate(from_d, "%d/%m/%Y") if from_d else date.today() - timedelta(days=1)
    to_date = strpdate(to_d, "%d/%m/%Y") if to_d else date.today()

    print "Main: scraping %s to %s" % (from_date.strftime("%d/%m/%Y"), to_date.strftime("%d/%m/%Y"))
    for rec in (clean(r) for r in walk(from_date, to_date)):
        sw_save(rec)

def historic():
    try:
        from scraperwiki import metadata
        hmark = metadata.get('hist_marker', default=(date.today() - timedelta(days=1)).strftime("%d/%m/%Y"))
        hmark = strpdate(hmark)
        if hmark < date(2005, 1, 1):
            print "History marker is %s (earlier than 2005), stopping." % hmark.strptime("%d/%m/%Y")

        fdate = hmark - timedelta(days=5)
        # XXX should retreive record and update only fields that arn't
        # present, or it will overwrite more recent data
        print "Historic: scraping %s to %s" % (fdate.strftime("%d/%m/%Y"), hmark.strftime("%d/%m/%Y"))
        for rec in (clean(r) for r in walk(fdate, hmark)):
            sw_save(rec)
        metadata.save('hist_marker', fdate.strftime('%d/%m/%Y'))
    except ImportError:
        print "no historic"

# normal 'if __name__ ==' doesn't seem to work on sw
try:
    import scraperwiki
    main()
    historic()
except ImportError:
    try:
        __IPYTHON__
    except NameError:
        # running from console
        #main()
        main("10/8/2010", "15/8/2010")



