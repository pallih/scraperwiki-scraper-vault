# Pull information from the CAA's G-INFO database of UK registered aircraft.
# http://www.caa.co.uk/application.aspx?catid=60&pagetype=65&appid=1
# Richard Cameron. May 2011

# Updated December 2012. The G-INFO website requires at least a two letter
# prefix. We have to search for G-AA?? rather than G-A??? now.

import re, datetime, urllib2, time

import scraperwiki
import lxml.html
from lxml import etree
def scrape(url):
    N=10
    for i in range(N+1):
        try:
            return scraperwiki.scrape(url, user_agent="Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")
        except Exception, e:
            print "Failed to fetch", url, e
            print "Retry", i
            if i==N:
                raise    

def current_prefix():
    # Spider aircraft based on the first letters of their registration.
    # On the first run we'll do G-AAA?, next run we'll do G-AAB?, and so on
    # Need to keep track of which prefix we're on between runs
    return scraperwiki.sqlite.get_var("current_prefix", "AAA")

def next_prefix(x):
    """ Map AAA -> AAB -> AAC -> ... -> AAZ -> ABA -> ... -> ZZZ -> AAA """
    if not re.match(r'[A-Z]{3}$', x):
        raise ValueError, "Bad prefix: %s" % x
    def aord(x):
        return ord(x) - ord('A')
    
    offset = 26*26*aord(x[0]) + 26*aord(x[1]) + aord(x[2])
    offset = (offset + 1) % (26**3)
    
    third = (offset % 26)
    offset = (offset - third) / 26
    second = offset % 26
    first = (offset - second) / 26

    def achr(x):
        return chr( ord('A') + x)

    return achr(first) + achr(second) + achr(third)




def fetch_registrations(url):
    """Spider the G-INFO side and yield a bunch of four_letter_registration
    registrations of (hopefully) all the aircraft registred"""


    while url:
        print "Fetching ", url
        html = scrape(url)
        root = lxml.html.fromstring(html)
        root.make_links_absolute("http://www.caa.co.uk/application.aspx")
        for link in root.cssselect('tr td a[id^="currentModule_currentModule_myRepeater__ct"]'):
            reg = link.text_content().strip()
            if not re.match(r'G-[A-Z]{4}', reg):
                raise ValueError, "Bad registration: %s" % reg
            yield reg[2:]

        # If this is the unique aircraft with this prefix, they might have redirected us
        # to the detail page already
        # We'd see something like this <span id="currentModule_currentModule_Registration" class="small">G-UACA</span>
        for span in root.cssselect('span[id^="currentModule_currentModule_Registration"]'):
            reg = span.text
            if not re.match(r'G-[A-Z]{4}', reg):
                raise ValueError, "Bad registration: %s" % reg
            yield reg[2:]
        

        # Is there a next page? Slightly funny "next" button behaviour.
        pages = root.cssselect('div[class="apppaging"] a[class^="textbutton"]')
        found_current = False
        url=None
        for page in pages:
            if found_current:
                url=page.attrib['href']
                break
            if page.attrib['class']=="textbuttoncurrent":
                found_current=True


def aircraft_html(registration):
    if not re.match(r"[A-Z]{4}", registration):
        raise ValueError, "Bad registration: %s" % registration

    return scrape("http://www.caa.co.uk/application.aspx?catid=60&pagetype=65&appid=1&mode=detailnosummary&fullregmark=%s" % registration)

def data_save(unique_keys, data):
    attempts = 0
    while True:
        attempts += 1
        try:
            scraperwiki.sqlite.save(unique_keys=unique_keys, data=data, verbose=0)
            return
        except scraperwiki.sqlite.SqliteError, e:
            print e
            if attempts>60:
                raise
            time.sleep(1)



def parse_aircraft_details(html):
    boring_fields = ['RecordLabel']
    ret = {'FetchTime' : datetime.datetime.now().isoformat()}
    root = lxml.html.fromstring(html)
    prefix = "currentModule_currentModule_"
    for span in root.cssselect('span[id^="%s"]' % prefix):
        key = re.sub("^%s" % prefix, "", span.attrib['id'])
        key = key.replace(" ", "")
        if key in boring_fields:
            continue
        value = "|".join(etree.XPath("text()")(span))
        value = value.replace(u"\xa0", " ") # Non-breaking spaces
        value = value.strip()
        ret[key] = value

    # Photos
    root.make_links_absolute("http://www.caa.co.uk/application.aspx")
    photos = root.cssselect('span[id="currentModule_currentModule_AircraftPhoto"] a')
    urls = [l.attrib['href'] for l in photos]
    for i,url in enumerate(urls):
        ret["Photo%d" % (i+1)] = url

    data_save(['Registration'], ret)


    return ret


def spider():

    # There are 26^3 = 17576 prefixes. Aim to read the whole CAA database every month.
    # I hope that's a reasonable compromise between sending them too many requests and
    # having the data out of date.
    for i in xrange(26**3 / 31):
        # Start spidering where we left off last run by lookup up the last used prefix in the database
        url = "http://www.caa.co.uk/application.aspx?catid=60&pagetype=65&appid=1&mode=summary&regmark=%s" % current_prefix()
    
        for reg in fetch_registrations(url):
            print "Fetching aircraft", reg
            parse_aircraft_details(aircraft_html(reg))

        # If we've got this far then we've gone through all the registrations
        # beginning with that prefix. Record that fact in the database.
        # If we haven't hit the CAA's website too hard already today we can
        # continue, otherwise pick up where we left off tomorrow.

        # The database locking model results in us getting a random
        # "database is locked" exception here. There doesn't seem to
        # be anything cleverer to do other than sleep and retry.
        for attempt in range(300):
            try:
                scraperwiki.sqlite.save_var("current_prefix", next_prefix(current_prefix()))
                break
            except scraperwiki.sqlite.SqliteError, e:
                print "Sqlite write error. Retrying. ", e
                time.sleep(1)

# Main
if __name__=="scraper":
#    scraperwiki.sqlite.save_var("current_prefix", "OAA")
    spider()

