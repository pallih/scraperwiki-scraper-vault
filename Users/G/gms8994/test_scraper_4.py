###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import pprint
import re
import sys
import time
import datetime

def parse(fname):
    url = "http://www.in.gov/dor/reference/files/{0}.pdf".format(fname)
    pdfdata = urllib2.urlopen(url).read()
    # print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    keymap = ['peoplesoft-keycode', 'type-of-tax', 'total-collections', 'less-refunds', 'net-collections']

    records = [ ]
    
    record_offset = 0
    page = pages[0]
    offset = 0
    skip_height = 0
    for el in list(page)[18:]:
        if (len(records) <= record_offset):
            records.append(dict())
        if el.tag == "text":
            value = re.sub(r'<b>|<\/b>|\n', r'', gettext_with_bi_tags(el)).strip()
            if value is not "":        
    
                if value[0] == '*':
                    skip_height = el.attrib['height']
    
                if el.attrib['height'] == skip_height:
                    continue
    
                ### DEBUG
                # print "Offset '{0}', text value '{1}', node value '{2}'".format(offset, keymap[offset], value)
                if value == "-":
                    value = 0
    
                records[record_offset][keymap[offset]] = value
        
                if (offset >= len(keymap)-1):
                    offset = 0
                    record_offset = record_offset + 1
    
                    records[record_offset-1]['month-year'] = fname
                    scraperwiki.sqlite.save(['peoplesoft-keycode', 'type-of-tax', 'month-year'], records[record_offset-1], "swdata", 2)
                else:
                    offset = offset + 1

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

# current_month = time.strftime("%m%y", time.localtime())
# parse(current_month)
last_month = (datetime.date.today() + datetime.timedelta(-1*365/12)).strftime("%m%y")
parse(last_month)
two_months_back = (datetime.date.today() + datetime.timedelta(-2*365/12)).strftime("%m%y")
parse(two_months_back)
###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree
import pprint
import re
import sys
import time
import datetime

def parse(fname):
    url = "http://www.in.gov/dor/reference/files/{0}.pdf".format(fname)
    pdfdata = urllib2.urlopen(url).read()
    # print "The pdf file has %d bytes" % len(pdfdata)
    
    xmldata = scraperwiki.pdftoxml(pdfdata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    keymap = ['peoplesoft-keycode', 'type-of-tax', 'total-collections', 'less-refunds', 'net-collections']

    records = [ ]
    
    record_offset = 0
    page = pages[0]
    offset = 0
    skip_height = 0
    for el in list(page)[18:]:
        if (len(records) <= record_offset):
            records.append(dict())
        if el.tag == "text":
            value = re.sub(r'<b>|<\/b>|\n', r'', gettext_with_bi_tags(el)).strip()
            if value is not "":        
    
                if value[0] == '*':
                    skip_height = el.attrib['height']
    
                if el.attrib['height'] == skip_height:
                    continue
    
                ### DEBUG
                # print "Offset '{0}', text value '{1}', node value '{2}'".format(offset, keymap[offset], value)
                if value == "-":
                    value = 0
    
                records[record_offset][keymap[offset]] = value
        
                if (offset >= len(keymap)-1):
                    offset = 0
                    record_offset = record_offset + 1
    
                    records[record_offset-1]['month-year'] = fname
                    scraperwiki.sqlite.save(['peoplesoft-keycode', 'type-of-tax', 'month-year'], records[record_offset-1], "swdata", 2)
                else:
                    offset = offset + 1

# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

# current_month = time.strftime("%m%y", time.localtime())
# parse(current_month)
last_month = (datetime.date.today() + datetime.timedelta(-1*365/12)).strftime("%m%y")
parse(last_month)
two_months_back = (datetime.date.today() + datetime.timedelta(-2*365/12)).strftime("%m%y")
parse(two_months_back)
