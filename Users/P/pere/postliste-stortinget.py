# Based on the scraper advanced-scraping-pdf
# See also 
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/?url=http%3A%2F%2Fwww.stortinget.no%2FGlobal%2Fpdf%2Fpostjournal%2Fpj-2012-05-09.pdf
import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import urlparse
import resource
import sys
postlistelib=scraperwiki.swimport('postliste-python-lib')

def find_journal_pdfs(parser, listurl):
#    print "Finding PDFs on " + listurl
    html = postlistelib.fetch_url_harder(listurl)

    root = lxml.html.fromstring(html)
    pdfurls = []
    for ahref in root.cssselect("div.mainbody a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            pdfurls.append(url)
    return pdfurls

def fetch_and_preprocess(parser, pdfurl):
    pdfcontent = postlistelib.fetch_url_harder(pdfurl)
    parser.preprocess(pdfurl, pdfcontent)
    pdfcontent = None

def add_pdf_lists(parser, pdfurls):
    for period in [
         "",
         "_2010-2011",
         "-2009-2010",
         "-2008-2009",
        ]:
        url = "http://www.stortinget.no/no/Stortinget-og-demokratiet/Administrasjonen/Dokumentoffentlighet/Stortingets-offentlige-postjournal" + period + "/"
        pdfurls.extend(find_journal_pdfs(parser, url))


def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        raise

def no_cpu_left(arg, spent, soft, hard):
     report_errors(arg)

agency = 'Stortinget'
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

if False:
    pdfurl = "http://www.stortinget.no/Global/pdf/postjournal/pj-2010-06-04-05.pdf"
    parse_pdf(pdfurl)
    exit(0)

pdfurls = []
add_pdf_lists(parser, pdfurls)

# Fetch all journal PDFs
errors = []
for pdfurl in pdfurls:
    postlistelib.exit_if_no_cpu_left(0, callback=no_cpu_left, arg = errors)
    try:
        parser.fetch_and_preprocess(pdfurl)
    except ValueError, e:
        errors.append(e)
    except IndexError, e:
        errors.append(e)
try:
    parser.process_pages()
except ValueError, e:
    errors.append(e)
except IndexError, e:
    errors.append(e)

report_errors(errors)

# Based on the scraper advanced-scraping-pdf
# See also 
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/?url=http%3A%2F%2Fwww.stortinget.no%2FGlobal%2Fpdf%2Fpostjournal%2Fpj-2012-05-09.pdf
import scraperwiki
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
import urlparse
import resource
import sys
postlistelib=scraperwiki.swimport('postliste-python-lib')

def find_journal_pdfs(parser, listurl):
#    print "Finding PDFs on " + listurl
    html = postlistelib.fetch_url_harder(listurl)

    root = lxml.html.fromstring(html)
    pdfurls = []
    for ahref in root.cssselect("div.mainbody a"):
        href = ahref.attrib['href']
        url = urlparse.urljoin(listurl, href)
        if -1 != href.find("file://"):
#            print "Skipping non-http URL " + url
            continue
        if parser.is_already_scraped(url):
            True
#            print "Skipping already scraped " + url
        else:
#            print "Will process " + url
            pdfurls.append(url)
    return pdfurls

def fetch_and_preprocess(parser, pdfurl):
    pdfcontent = postlistelib.fetch_url_harder(pdfurl)
    parser.preprocess(pdfurl, pdfcontent)
    pdfcontent = None

def add_pdf_lists(parser, pdfurls):
    for period in [
         "",
         "_2010-2011",
         "-2009-2010",
         "-2008-2009",
        ]:
        url = "http://www.stortinget.no/no/Stortinget-og-demokratiet/Administrasjonen/Dokumentoffentlighet/Stortingets-offentlige-postjournal" + period + "/"
        pdfurls.extend(find_journal_pdfs(parser, url))


def report_errors(errors):
    if 0 < len(errors):
        print "Errors:"
        for e in errors:
            print e
        raise

def no_cpu_left(arg, spent, soft, hard):
     report_errors(arg)

agency = 'Stortinget'
parser = postlistelib.PDFJournalParser(agency=agency)
#parser.debug = True

if False:
    pdfurl = "http://www.stortinget.no/Global/pdf/postjournal/pj-2010-06-04-05.pdf"
    parse_pdf(pdfurl)
    exit(0)

pdfurls = []
add_pdf_lists(parser, pdfurls)

# Fetch all journal PDFs
errors = []
for pdfurl in pdfurls:
    postlistelib.exit_if_no_cpu_left(0, callback=no_cpu_left, arg = errors)
    try:
        parser.fetch_and_preprocess(pdfurl)
    except ValueError, e:
        errors.append(e)
    except IndexError, e:
        errors.append(e)
try:
    parser.process_pages()
except ValueError, e:
    errors.append(e)
except IndexError, e:
    errors.append(e)

report_errors(errors)

