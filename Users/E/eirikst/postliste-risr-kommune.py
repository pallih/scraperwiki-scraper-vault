# -*- coding: UTF-8 -*-
# Based on the scraper advanced-scraping-pdf
# See also
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/?url=http%3A%2F%2Fwww.stortinget.no%2FGlobal%2Fpdf%2Fpostjournal%2Fpj-2012-05-09.pdf

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
#import resource
import sys
#import urlparse
#import gc
import re
#lazycache=scraperwiki.swimport('lazycache')
#postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Risør kommune'

import mechanize

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://159.171.0.169/ris/Modules/innsyn.aspx?mode=pl&SelPanel=0&ObjectType=ePhorteRegistryEntry&VariantType=Innsyn&ViewType=List&Query=RecordDate%3a%28-7%29+AND+DocumentType%3a%28I%2cU%29'
br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

html = response.read()



for pagenum in range(6):
    print "Page %d  page length %d" % (pagenum, len(html))
    #print html
    #print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)
    
    
    mnextlink = re.search("javascript:__doPostBack\('ctl00\$ctl00\$ctl00\$WebPartManager\$wp1243460126ViewPart\$ctl04',''\).>Neste", html)
    #print mnextlink
    if not mnextlink:
        break
    
    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ctl00$ctl00$ctl00$WebPartManager$wp1243460126ViewPart$ctl04' #'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    br.submit()
    
    html = br.response().read()
    #print len(html)




# def report_errors(errors):
#     if 0 < len(errors):
#         print "Errors:"
#         for e in errors:
#             print e
#         exit(1)
# def out_of_cpu(arg, spent, hard, soft):
#     report_errors(arg)
# 
# def process_pdf(parser, pdfurl, errors):
#     errors = []
#     postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
#     try:
#         pdfcontent = scraperwiki.scrape(pdfurl)
#         parser.preprocess(pdfurl, pdfcontent)
#         pdfcontent = None
# #    except ValueError, e:
# #        errors.append(e)
#     except IndexError, e:
#         errors.append(e)
# 
# def process_page_queue(parser, errors):
#     try:
#         parser.process_pages()
#         postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
#     except scraperwiki.CPUTimeExceededError, e:
#         errors.append("Processing pages interrupted")
# 
# def process_journal_pdfs(parser, listurl, errors):
# #    print "Finding PDFs on " + listurl
# #    u = urllib.parse.urlparse(listurl)
#     html = scraperwiki.scrape(listurl)
#     root = lxml.html.fromstring(html)
#     html = None
#     for ahref in root.cssselect("table a"):
#         href = ahref.attrib['href']
#         url = urlparse.urljoin(listurl, href)
#         if -1 != href.find("file://"):
# #            print "Skipping non-http URL " + url
#             continue
#         if parser.is_already_scraped(url):
#             True
# #            print "Skipping already scraped " + url
#         else:
# #            print "Will process " + url
#             process_pdf(parser, url, errors)
# 
# def test_small_pdfs():
#     # Test with some smaller PDFs
#     errors = []
#     process_pdf("http://home.nuug.no/~pere/uio-postjournal/2011-16.pdf", errors)
#     process_pdf("http://home.nuug.no/~pere/uio-postjournal/2011-52.pdf", errors)
#     process_page_queue(errors)
#     report_errors(errors)
#     exit(0)
# 
# #test_small_pdfs()
# errors = []
# parser = postlistelib.PDFJournalParser(agency=agency)
# process_journal_pdfs(parser, "http://www.havn.oslo.kommune.no/postjournal/", errors)
# process_page_queue(parser, errors)
# report_errors(errors)

# -*- coding: UTF-8 -*-
# Based on the scraper advanced-scraping-pdf
# See also
# https://views.scraperwiki.com/run/pdf-to-html-preview-1/?url=http%3A%2F%2Fwww.stortinget.no%2FGlobal%2Fpdf%2Fpostjournal%2Fpj-2012-05-09.pdf

import scraperwiki
import json
from BeautifulSoup import BeautifulSoup
import datetime
import dateutil.parser
import lxml.html
#import resource
import sys
#import urlparse
#import gc
import re
#lazycache=scraperwiki.swimport('lazycache')
#postlistelib=scraperwiki.swimport('postliste-python-lib')

agency = 'Risør kommune'

import mechanize

# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://159.171.0.169/ris/Modules/innsyn.aspx?mode=pl&SelPanel=0&ObjectType=ePhorteRegistryEntry&VariantType=Innsyn&ViewType=List&Query=RecordDate%3a%28-7%29+AND+DocumentType%3a%28I%2cU%29'
br = mechanize.Browser()

# sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)

html = response.read()



for pagenum in range(6):
    print "Page %d  page length %d" % (pagenum, len(html))
    #print html
    #print "Clinicians found:", re.findall("PDetails.aspx\?ProviderId.*?>(.*?)</a>", html)
    
    
    mnextlink = re.search("javascript:__doPostBack\('ctl00\$ctl00\$ctl00\$WebPartManager\$wp1243460126ViewPart\$ctl04',''\).>Neste", html)
    #print mnextlink
    if not mnextlink:
        break
    
    br.select_form(name='aspnetForm')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'ctl00$ctl00$ctl00$WebPartManager$wp1243460126ViewPart$ctl04' #'ProviderSearchResultsTable1$NextLinkButton'
    br['__EVENTARGUMENT'] = ''
    br.submit()
    
    html = br.response().read()
    #print len(html)




# def report_errors(errors):
#     if 0 < len(errors):
#         print "Errors:"
#         for e in errors:
#             print e
#         exit(1)
# def out_of_cpu(arg, spent, hard, soft):
#     report_errors(arg)
# 
# def process_pdf(parser, pdfurl, errors):
#     errors = []
#     postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
#     try:
#         pdfcontent = scraperwiki.scrape(pdfurl)
#         parser.preprocess(pdfurl, pdfcontent)
#         pdfcontent = None
# #    except ValueError, e:
# #        errors.append(e)
#     except IndexError, e:
#         errors.append(e)
# 
# def process_page_queue(parser, errors):
#     try:
#         parser.process_pages()
#         postlistelib.exit_if_no_cpu_left(0, out_of_cpu, errors)
#     except scraperwiki.CPUTimeExceededError, e:
#         errors.append("Processing pages interrupted")
# 
# def process_journal_pdfs(parser, listurl, errors):
# #    print "Finding PDFs on " + listurl
# #    u = urllib.parse.urlparse(listurl)
#     html = scraperwiki.scrape(listurl)
#     root = lxml.html.fromstring(html)
#     html = None
#     for ahref in root.cssselect("table a"):
#         href = ahref.attrib['href']
#         url = urlparse.urljoin(listurl, href)
#         if -1 != href.find("file://"):
# #            print "Skipping non-http URL " + url
#             continue
#         if parser.is_already_scraped(url):
#             True
# #            print "Skipping already scraped " + url
#         else:
# #            print "Will process " + url
#             process_pdf(parser, url, errors)
# 
# def test_small_pdfs():
#     # Test with some smaller PDFs
#     errors = []
#     process_pdf("http://home.nuug.no/~pere/uio-postjournal/2011-16.pdf", errors)
#     process_pdf("http://home.nuug.no/~pere/uio-postjournal/2011-52.pdf", errors)
#     process_page_queue(errors)
#     report_errors(errors)
#     exit(0)
# 
# #test_small_pdfs()
# errors = []
# parser = postlistelib.PDFJournalParser(agency=agency)
# process_journal_pdfs(parser, "http://www.havn.oslo.kommune.no/postjournal/", errors)
# process_page_queue(parser, errors)
# report_errors(errors)

