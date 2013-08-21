import scraperwiki
import base64
import lxml.html
import chardet
import urllib
import urlparse
import re
import datetime
import pprint
import copy
from array import array

import urllib
import tempfile
import os
from lxml import etree, cssselect
import re

# set re to recognize unicode characters as words
re.UNICODE

# to disable a listing (for testing purposes), put an underscore at the beginning
fund_listings = {
    "CPPIB_Foreign" : "http://dl.dropbox.com/u/1470822/Foreign_PublicEquityHoldings_March312011.pdf",
    "CPPIB_Cdn": "http://dl.dropbox.com/u/1470822/CDN_PublicEquityHoldings_March312011.pdf", # "http://www.cppib.ca/files/PDF/CDN_PublicEquityHoldings_March312011.pdf",
    "OTPP"  : "http://www.otpp.com/wps/wcm/connect/otpp_en/Home/Investments/Major+Investments/Corporate+Shares+%28Alphabetical+listing%29/",
    "_Caisse" : "http://dl.dropbox.com/u/1470822/Caisse-2010-Public%20Equities.pdf",
}

# parser = PDFParser(CPPIB_pdf)


def css(selector, xml):
    return cssselect.CSSSelector(selector)(xml)

def pdftoxml(pdfdata):
    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()
    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name # "temph.xml"
    cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)
    pdffout.close()
    #xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata

def scraper_pdf(pdfurl):
    pdfdata = urllib.urlopen(pdfurl).read()
    pdfxml = pdftoxml(pdfdata)
    # encd = chardet.detect(pdfxml)['encoding']
    # parser = etree.XMLParser(ns_clean=True,recover=True,encoding="UTF-8")
    xml = etree.fromstring(pdfxml)
    return xml

def otpp(url):
    html = scraperwiki.scrape(url) 
    root = lxml.html.fromstring(html)
    fund = "OTPP"    
    equity_list = []
    failure_list = []

    for el in root.cssselect("div.divBodyFullSpan table tbody"): 
        for tr in el.cssselect("tr.tablehighlight03"):
            # print lxml.html.tostring(tr)
            company = tr.cssselect("td")[0].text
            shares = tr.cssselect("td div")[0].text
            value = tr.cssselect("td div")[1].text
            country = ''
            
            data ={ 'id'     : fund + company,
                'Fund'   : fund,
                'Company': company,
                'Shares' : shares,
                'Value'  : value,
                'Country': country }
            
            if data:
                equity_list.append(data)
            else:
                failure_list.append([company, shares, value, country])
        
    for row in equity_list:
        scraperwiki.sqlite.save(unique_keys=['id'], data=row)
    
    pprint.pprint(failure_list)

def cppib(xml, fund_name):
    print "Number of pages: ", len(xml)
    
    # print out a page, so that you can see the structure
    
    
    fund = "CPPIB"
    pages = 0
    equity_list = []
    failure_list = []
    text_nodes = []
    
    
    # create a list of textnodes that represent all the text entries in the file
    #   this will be analyzed below

    print_page = ''
    for page in xml:
    
        page_parsed = []
    
        # print out html in each page for review and to check structure
        # comment out once you've got the scraper working
        if pages == 10:
            print_page = etree.tostring(page)
        pages+=1
        for i in page.xpath('text'):
            try:
                # test to make sure you are adding an lxml.etree._Element
                if i.get("height") == ("16" or 16) and type(i)==lxml.etree._Element:
                    page_parsed.append(i)
            except:
                print "that wasn't a text node!"
    
        text_nodes.extend([el for el in page_parsed])
    
    print print_page 
    
    # some setup for analyzing text_nodes
    slice_start = 0
    slice_end = 6 if fund_name == "CPPIB_Foreign" else 3
    print 'length of text_nodes:', len(text_nodes)
    
    '''
    Analyze the patterns of text nodes

                        
    ----------------------------------------------------------------------------------
    
    Need to iterate over each slice, checking for the following patterns:
    
        a = alpha(mixed)
        d = decimal (only)
    
    Possible patterns are as noted above in each of the if clauses. We can distinguish
    between the "a"'s at the beginning and end of lines because
    they have "top" attributes that tell you where they are relative to each other.
    If the second "a" has a "top" that is less than the "a" being examined, then
    you know that you are dealing with 2.
    '''
    
    while slice_end <= len(text_nodes) and fund_name == 'CPPIB_Foreign':
        
        #---<
        ## print '======================================= START'
        ## print 'slice_start:', slice_start, '\tslice_end:', slice_end
        ## pprint.pprint([i.text for i in text_nodes[slice_start:slice_end]])
        #--->
    
        data = {}
        company = ''
        shares = ''
        value = ''
        country = ''
    
        pattern = ''
        text_node = [ lxml.etree._Element ]*6
        for i, el in enumerate(text_nodes[slice_start:slice_end]):
            _slice_start = slice_start
            _slice_end = slice_end
    
    
            try:
                if slice_end - slice_start != 6:
                    print "There was a problem, you need 6 elements in the slice."
                    break
                else:
        
                    el.text = el.text.strip(u"\xa0")
                    # English version of regex "[^\W\d_]": "Any character that is not a non-alphanumeric
                    # character ([^\W] is the same as \w), but that is also not a digit and not an underscore".
                    # from here: http://stackoverflow.com/questions/8923949/matching-only-a-unicode-letter-in-python-re
                    ## pprint.pprint([str(type(x)) for x in text_node])
        
                    # however, not used below, only need to search for \d
                    if re.search("^([\d,]+)$", el.text):
                        pattern += 'd'
                    else:
                        pattern += 'a'
                    # assign the node object to a list that represents the objects underlying the pattern
                    text_node[i] = el
        
        
                    # perversely, some "columns" are actually both a word and a number, separated by spaces,
                    # so if the line starts with a word and ends with numbers, chop it
                    # in two and insert a new text_node into text_nodes
                    regex = r'([\d,]+)$' # match any trailing numbers
                    if re.search(regex, el.text) and pattern[-1] == 'a':
                        m = re.split(regex, el.text)
                        if m:
                            text_nodes[slice_start+i].text = m[0]
                            text_node[i].text = m[0]
                            insert_no = slice_start+i+1
                            text_nodes.insert(insert_no, copy.deepcopy(el))
                            text_nodes[insert_no].text = m[1]
                            text_node.insert(i+1, text_nodes[insert_no])
                            ## print 'text_node', text_node[i+1].text
                            
                            if len(pattern)-1 >= i+1:
                                n = array("c", pattern)
                                n[i+1] = 'd'
                                pattern = n.tostring()
        
                        #---<
                        '''
                        for i in text_nodes[slice_start:slice_end]:
                            print i.text
                        '''
                        #--->
    
            except:
                failure_list.append([_slice_start, _slice_end, el])
    
        # analyze patterns in the text_nodes slice
    
        if re.search("^d.+", pattern):
            # some pages start with a decimal, so pop it and continue on
            slice_end += 1
            slice_start = max(0,slice_end - 6)
    
        elif pattern == 'addaad' and int(text_node[3].get("top")) < int(text_node[4].get("top")):
            # this is the "regular" case no double-lines
            company = text_node[0].text
            shares = text_node[1].text
            value = text_node[2].text
            country = text_node[3].text
            slice_end += 4
            slice_start = max(0,slice_end - 6)
    
        elif pattern == 'addaad' and int(text_node[3].get("top")) > int(text_node[4].get("top")) and int(text_node[4].get("top")) == int(text_node[5].get("top")):
            # this is an end of page pattern where we want to keep the two following nodes
            company = text_node[0].text
            shares = text_node[1].text
            value = text_node[2].text
            country = text_node[3].text
            slice_end += 4
            slice_start = max(0,slice_end - 6)
    
        elif pattern == 'aaddaa' and ( int(text_node[0].get("top")) < int(text_node[1].get("top")) ) and ( int(text_node[4].get("top")) < int(text_node[3].get("top")) ):
            # first two a's are double-lines and
            # final two a's are double-lines
            company = text_node[0].text + text_node[1].text
            shares = text_node[2].text
            value = text_node[3].text
            country = text_node[4].text + text_node[5].text
            slice_end += 6
            slice_start = max(0,slice_end - 6)
    
        elif pattern == 'aaddaa' and ( int(text_node[0].get("top")) < int(text_node[1].get("top")) ) and ( int(text_node[4].get("top")) != int(text_node[5].get("top")) ):
            # first two a's are double-lines and
            # final a is single line that can be lower (on next page) or higher (on same page)
            company = text_node[0].text + text_node[1].text
            shares = text_node[2].text
            value = text_node[3].text
            country = text_node[4].text
            slice_end += 5
            slice_start = max(0,slice_end - 6)
    
        elif pattern == 'addadd' or pattern == 'addada':
            # these patterns occur at the end of a page and appear to be incorrect orderings
            # discard the last two digits
            company = text_node[0].text
            shares = text_node[1].text
            value = text_node[2].text
            country = text_node[3].text
            slice_end += 6     
            slice_start = max(0,slice_end - 6)   
    
        elif pattern == 'aaddad':
            # first two a's are double-lines and
            # final a is single line, followed by a line on next page
            if int(text_node[0].get("top")) < int(text_node[1].get("top")) and int(text_node[4].get("top")) > int(text_node[5].get("top")):
                company = text_node[0].text + text_node[1].text
                shares = text_node[2].text
                value = text_node[3].text
                country = text_node[4].text
                slice_end += 5
                slice_start = max(0,slice_end - 6)
    
        elif pattern == 'addaaa' and int(text_node[3].get("top")) < int(text_node[2].get("top")):
            # this is the case where a3 and a4 make up a double-lined country
            company = text_node[0].text
            shares = text_node[1].text
            value = text_node[2].text
            country = text_node[3].text + text_node[4].text
            slice_end += 5
            slice_start = max(0,slice_end - 6)
    
        elif pattern == 'addaaa' and int(text_node[3].get("top")) != int(text_node[4].get("top")):
            # this is the case where the node is followed by a single or double-lined company
            # on the same or next page
            company = text_node[0].text
            shares = text_node[1].text
            value = text_node[2].text
            country = text_node[3].text
            slice_end += 4
            slice_start = max(0,slice_end - 6)
    
        else:
            ## slice_end = len(text_nodes)
    
            # the pattern matching failed, move one down in the list
            # and start to look at another 6 element list
            slice_end += 1
            slice_start = max(0,slice_end - 6)
    
        data ={ 'id'     : fund + company,
                'Fund'   : fund,
                'Company': company,
                'Shares' : shares,
                'Value'  : value,
                'Country': country }
    
        #---<
        '''
        if data['Company'] == (None or '') or 'Gintech' in data['Company']:
          print "===================================", slice_start, slice_end
          print "pattern:", pattern
          print [i for i in text_node]
          print 'NODE VALUES: ', text_node[0].text+'\n', text_node[1].text+'\n', text_node[2].text+'\n', text_node[3].text+'\n', text_node[4].text+'\n', text_node[5].text
          print 'VARIABLES: Fund:', fund, '\nCompany:', company, '\nShares:', shares, '\nValue:', value, '\nCountry:', country
          print "tops:",text_node[0].get("top"),text_node[1].get("top"),text_node[2].get("top"),text_node[3].get("top"),text_node[4].get("top"),text_node[5].get("top")
          pprint.pprint(data)
        '''

        #--->    
        
        if data:
            equity_list.append(data)
        else:
            failure_list.append([_slice_start, _slice_end, text_node])
    
    # end CPPIB_Foreign

    while slice_end <= len(text_nodes) and fund_name == 'CPPIB_Cdn':
        
        #---<
        '''
        print '======================================= START'
        print 'slice_start:', slice_start, '\tslice_end:', slice_end
        pprint.pprint([i.text for i in text_nodes[slice_start:slice_end]])
        '''
        #--->
    
        data = {}
        company = ''
        shares = ''
        value = ''
        country = ''
    
        pattern = ''
        text_node = [ lxml.etree._Element ]* 3
        for i, el in enumerate(text_nodes[slice_start:slice_end]):
            _slice_start = slice_start
            _slice_end = slice_end
    
            try:
                if slice_end - slice_start != 3:
                    print "There was a problem, you need 3 elements in the slice."
                    break
                else:
        
                    el.text = el.text.strip(u"\xa0")
                    # English version of regex "[^\W\d_]": "Any character that is not a non-alphanumeric
                    # character ([^\W] is the same as \w), but that is also not a digit and not an underscore".
                    # from here: http://stackoverflow.com/questions/8923949/matching-only-a-unicode-letter-in-python-re
                    ## pprint.pprint([str(type(x)) for x in text_node])
        
                    # however, not used below, only need to search for \d
                    if re.search("^([\d,]+)$", el.text):
                        pattern += 'd'
                    else:
                        pattern += 'a'
                    # assign the node object to a list that represents the objects underlying the pattern
                    text_node[i] = el
        
        
                    # perversely, some "columns" are actually both a word and a number, separated by spaces,
                    # so if the line starts with a word and ends with numbers, chop it
                    # in two and insert a new text_node into text_nodes
                    regex = r'([\d,]+)$' # match any trailing numbers
                    if re.search(regex, el.text) and pattern[-1] == 'a':
                        m = re.split(regex, el.text)
                        if m:
                            text_nodes[slice_start+i].text = m[0]
                            text_node[i].text = m[0]
                            insert_no = slice_start+i+1
                            text_nodes.insert(insert_no, copy.deepcopy(el))
                            text_nodes[insert_no].text = m[1]
                            text_node.insert(i+1, text_nodes[insert_no])
                            ## print 'text_node', text_node[i+1].text
                            
                            if len(pattern)-1 >= i+1:
                                n = array("c", pattern)
                                n[i+1] = 'd'
                                pattern = n.tostring()
         
            except:
                failure_list.append([_slice_start, _slice_end, el])
    
        # analyze patterns in the text_nodes slice
    
        if re.search("^d.+", pattern):
            # some pages start with a decimal, so pop it and continue on
            slice_end += 1
            slice_start = max(0,slice_end - 3)
       
        else:
            company = text_node[0].text if type(text_node[0].text) != 'text' else ''
            shares = text_node[1].text if type(text_node[1].text) != 'text' else ''
            value = text_node[2].text if type(text_node[2].text) != 'text' else ''
            slice_end += 3
            slice_start = max(0,slice_end - 3)
        
        try:
            data ={ 'id'     : fund + company,
                'Fund'   : fund,
                'Company': company,
                'Shares' : shares,
                'Value'  : value,
                'Country': 'Canada',}
        except:
            pass
        
        if data:
            equity_list.append(data)
        else:
            failure_list.append([_slice_start, _slice_end, text_node])    

    # end CPPIB_Cdn

    for row in equity_list:
        scraperwiki.sqlite.save(unique_keys=['id'], data=row)
    
    pprint.pprint(failure_list)

    '''
    
    # actual websites - to be used when the scraper is ready to go:
    fund_listings = [
        "http://www.cppib.ca/files/PDF/Foreign_PublicEquityHoldings_March312011.pdf",
        "",
    ]
    
    '''

def strip_nbsp(text):
    text.replace(u'\xa0', ' ') 

def caisse(xml, fund_name):

    print "Number of pages: ", len(xml)
    
    # print out a page, so that you can see the structure
    
    
    fund = "CPPIB"
    pages = 0
    equity_list = []
    failure_list = []
    text_nodes = []
    
    
    # create a list of textnodes that represent all the text entries in the file
    #   this will be analyzed below

    print_page = ''
    for page in xml:
    
        page_parsed = []
    
        # print out html in each page for review and to check structure
        # comment out once you've got the scraper working
        if pages == 10:
            print_page = etree.tostring(page)
        pages+=1
        for i in page.xpath('text'):
            try:
                # test to make sure you are adding an lxml.etree._Element
                if i.get("height") == ("16" or 16) and type(i)==lxml.etree._Element:
                    page_parsed.append(i)
            except:
                print "that wasn't a text node!"
    
        text_nodes.extend([el for el in page_parsed])
    
    print print_page
    
    # some setup for analyzing text_nodes
    slice_start = 0
    slice_end = 6 if fund_name == "CPPIB_Foreign" else 3
    print 'length of text_nodes:', len(text_nodes)
    
    '''
    Analyze the patterns of text nodes

                        
    ----------------------------------------------------------------------------------
    
    Need to iterate over each slice, checking for the following patterns:
    
        a = alpha(mixed)
        d = decimal (only)
    
    Possible patterns are as noted above in each of the if clauses. We can distinguish
    between the "a"'s at the beginning and end of lines because
    they have "top" attributes that tell you where they are relative to each other.
    If the second "a" has a "top" that is less than the "a" being examined, then
    you know that you are dealing with 2.
    '''
    

# --- Main Loop

for fund, holdings in fund_listings.items():

    if fund == 'CPPIB_Foreign': 
        xml = scraper_pdf(holdings)
        cppib(xml, fund)
        
    elif fund == 'CPPIB_Cdn':
        xml = scraper_pdf(holdings)
        cppib(xml, fund)

    elif fund == 'OTPP':
        otpp(holdings)

    elif fund == 'Caisse':
        xml = scraper_pdf(holdings)
        caisse(xml, fund)

    else:
        pass


