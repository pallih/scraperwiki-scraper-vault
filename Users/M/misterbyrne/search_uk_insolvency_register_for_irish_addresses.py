import scraperwiki
import lxml.html
import re
import string
import httplib
import os
import dateutil.parser

#Attempt to deal with bad servers - http://bobrochel.blogspot.ie/2010/11/bad-servers-chunked-encoding-and.html

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

# Scrape the UK Insolvency register for Irish Addresses

BASE_HOST = "http://www.insolvencydirect.bis.gov.uk"
BASE_URL = BASE_HOST + "/eiir/"
URL_TEMPLATE = "/eiir/IIRSearchNames.asp?court=ALL&CourtName=ALL&Office=&OfficeName=&page=%d&surnamesearch=%s&forenamesearch=ALLFORENAMES&OPTION=NAME&tradingnamesearch="

def make_absolute(url):
    if re.match("^http://", url): return url
    if re.match("^/eiir/", url): return BASE_HOST + url
    else: return BASE_URL + url

def queue_scrape(url):
    try:
        result = scraperwiki.sqlite.select("1 from scrapequeue where url = ?", [url])
    except Exception,e:
        print str(e)
        result = []
    if not result:
        scraperwiki.sqlite.save(unique_keys = ["url"], data = { "url": url, "scraped": 0 }, table_name = "scrapequeue")
        return True
    else:
        return False

def get_scrapes(n):
    result = scraperwiki.sqlite.select("* from scrapequeue where scraped = 0 limit ?", [n])
    if result:
        return [row["url"] for row in result]
    else:
        return None

def flag_scraped(url):
    scraperwiki.sqlite.save(unique_keys = ["url"], data = { "url": url, "scraped": 1 }, table_name = "scrapequeue")

def flag_error(url):
    scraperwiki.sqlite.save(unique_keys = ["url"], data = { "url": url, "scraped": 2 }, table_name = "scrapequeue")

def scrape_table(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    count = 0
    for link in root.cssselect("a"):
        href = link.get("href").strip()
        if queue_scrape(make_absolute(href)):
            count = count + 1
    if count > 0:
        print "'%s' added %d new links" % (url, count)

def scrape_value(document, key):
    matches = document.xpath("//tr[normalize-space(td/strong/text())='" + key + "']/td[2]//text()")
    return os.linesep.join([s.strip() for s in matches])

def scrape_detail(url):
    html = scraperwiki.scrape(url)
    document = lxml.html.fromstring(html)
    data = {
        "Title": scrape_value(document, "Title"),
        "Forename": scrape_value(document, "Forename(s)"),
        "Surname": scrape_value(document, "Surname"),
        "Gender": scrape_value(document, "Gender"),
        "Occupation": scrape_value(document, "Occupation"),
        "DateOfBirth": dateutil.parser.parse(scrape_value(document, "Date of Birth")).date(),
        "LastKnownAddress": scrape_value(document, "Last Known Address"),
        "Court": scrape_value(document, "Court"),
        "Type": scrape_value(document, "Type "),
        "Number": scrape_value(document, "Number"),
        "Year": scrape_value(document, "Case Year"),
        "OrderDate": dateutil.parser.parse(scrape_value(document, "Order Date")).date(),
        "Status": scrape_value(document, "Status"),
        "CaseDescription": scrape_value(document, "Case Description"),
        "CaseUrl": url
    }
    print(data)
    scraperwiki.sqlite.save(unique_keys = ["CaseUrl"], data = data, table_name = "details")

def scrape(url):
    try:
        if re.search("/eiir/IIRSearchNames.asp", url):
            scrape_table(url)
        elif re.search("IIRCaseIndivDetail.asp", url):
            scrape_detail(url)
        flag_scraped(url)
    except Exception, e:
        print url
        print str(e)
        flag_error(url)

for letter in string.uppercase:
    queue_scrape(BASE_HOST + URL_TEMPLATE % (1, letter))

while True:
    urls = get_scrapes(10)
    if not urls:
        print "done!"
        break
    for url in urls:
        scrape(url)
import scraperwiki
import lxml.html
import re
import string
import httplib
import os
import dateutil.parser

#Attempt to deal with bad servers - http://bobrochel.blogspot.ie/2010/11/bad-servers-chunked-encoding-and.html

def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except httplib.IncompleteRead, e:
            return e.partial

    return inner

httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

# Scrape the UK Insolvency register for Irish Addresses

BASE_HOST = "http://www.insolvencydirect.bis.gov.uk"
BASE_URL = BASE_HOST + "/eiir/"
URL_TEMPLATE = "/eiir/IIRSearchNames.asp?court=ALL&CourtName=ALL&Office=&OfficeName=&page=%d&surnamesearch=%s&forenamesearch=ALLFORENAMES&OPTION=NAME&tradingnamesearch="

def make_absolute(url):
    if re.match("^http://", url): return url
    if re.match("^/eiir/", url): return BASE_HOST + url
    else: return BASE_URL + url

def queue_scrape(url):
    try:
        result = scraperwiki.sqlite.select("1 from scrapequeue where url = ?", [url])
    except Exception,e:
        print str(e)
        result = []
    if not result:
        scraperwiki.sqlite.save(unique_keys = ["url"], data = { "url": url, "scraped": 0 }, table_name = "scrapequeue")
        return True
    else:
        return False

def get_scrapes(n):
    result = scraperwiki.sqlite.select("* from scrapequeue where scraped = 0 limit ?", [n])
    if result:
        return [row["url"] for row in result]
    else:
        return None

def flag_scraped(url):
    scraperwiki.sqlite.save(unique_keys = ["url"], data = { "url": url, "scraped": 1 }, table_name = "scrapequeue")

def flag_error(url):
    scraperwiki.sqlite.save(unique_keys = ["url"], data = { "url": url, "scraped": 2 }, table_name = "scrapequeue")

def scrape_table(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    count = 0
    for link in root.cssselect("a"):
        href = link.get("href").strip()
        if queue_scrape(make_absolute(href)):
            count = count + 1
    if count > 0:
        print "'%s' added %d new links" % (url, count)

def scrape_value(document, key):
    matches = document.xpath("//tr[normalize-space(td/strong/text())='" + key + "']/td[2]//text()")
    return os.linesep.join([s.strip() for s in matches])

def scrape_detail(url):
    html = scraperwiki.scrape(url)
    document = lxml.html.fromstring(html)
    data = {
        "Title": scrape_value(document, "Title"),
        "Forename": scrape_value(document, "Forename(s)"),
        "Surname": scrape_value(document, "Surname"),
        "Gender": scrape_value(document, "Gender"),
        "Occupation": scrape_value(document, "Occupation"),
        "DateOfBirth": dateutil.parser.parse(scrape_value(document, "Date of Birth")).date(),
        "LastKnownAddress": scrape_value(document, "Last Known Address"),
        "Court": scrape_value(document, "Court"),
        "Type": scrape_value(document, "Type "),
        "Number": scrape_value(document, "Number"),
        "Year": scrape_value(document, "Case Year"),
        "OrderDate": dateutil.parser.parse(scrape_value(document, "Order Date")).date(),
        "Status": scrape_value(document, "Status"),
        "CaseDescription": scrape_value(document, "Case Description"),
        "CaseUrl": url
    }
    print(data)
    scraperwiki.sqlite.save(unique_keys = ["CaseUrl"], data = data, table_name = "details")

def scrape(url):
    try:
        if re.search("/eiir/IIRSearchNames.asp", url):
            scrape_table(url)
        elif re.search("IIRCaseIndivDetail.asp", url):
            scrape_detail(url)
        flag_scraped(url)
    except Exception, e:
        print url
        print str(e)
        flag_error(url)

for letter in string.uppercase:
    queue_scrape(BASE_HOST + URL_TEMPLATE % (1, letter))

while True:
    urls = get_scrapes(10)
    if not urls:
        print "done!"
        break
    for url in urls:
        scrape(url)
