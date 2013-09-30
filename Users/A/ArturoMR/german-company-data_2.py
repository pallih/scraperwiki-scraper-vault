# -*- coding: utf-8 -*-

import mechanize
from BeautifulSoup import BeautifulSoup
import re
import sys
import lxml.html
import scraperwiki
import random
from datetime import date

# TODO: Seed random generator with content from
# http://www.random.org/integers/?num=1&min=1&max=10000&col=1&base=10&format=plain&rnd=new

# randomize list
def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

# get rid of unwanted HTML entities and garbage
def cleanup_string(html):
    html = html.replace('&nbsp;', ' ')
    html = re.sub('\s+', ' ', html)
    t = lxml.html.fromstring(html)
    return t.text_content().strip()

# parses entries out of one search result table
# (first splitting table into multiple tables)
def parse_result_table(html, court, register_type):
    # split this damn table by header rows
    html_parts = re.split('<tr>\s*<td\s+colspan="[0-9]"\s+class="RegPortErg_AZ">', html)
    if len(html_parts):
        html = '</table> <table class="scrapableTable"><tr><td class="RegPortErg_AZ">'.join(html_parts)
        soup = BeautifulSoup(html)
        items = soup.findAll("table", { "class": "scrapableTable"} )
        for table in items:
            identifier_line = cleanup_string(table.find("td", {"class": "RegPortErg_AZ"}).find("b").string)
            idmatch = re.search('\s+([0-9]+)$', identifier_line)
            idnum = idmatch.group(1)
            state = cleanup_string(table.find("td", {"class": "RegPortErg_AZ"}).contents[0])
            name = cleanup_string(table.find("td", {"class": "RegPortErg_FirmaKopf"}).contents[0])
            location = cleanup_string(table.find("td", {"class": "RegPortErg_SitzStatusKopf"}).contents[0])
            today = date.today()
            record = {
                'court': court,
                'register_type': register_type,
                'idnum': idnum,
                'state': state,
                'name': name,
                'location': location,
                'last_seen': today.isoformat()
            }
            try:
                scraperwiki.sqlite.save(unique_keys=["court", "register_type", "idnum"], data=record)
            except:
                print "Could not write record", record


# save court status
def save_last_court_id(id):
    scraperwiki.sqlite.save_var('last_court_id', id)

# save register_type status
def save_last_register_type_id(id):
    scraperwiki.sqlite.save_var('last_register_type_id', id)

# get court status
def get_last_court_id():
    val = scraperwiki.sqlite.get_var('last_court_id')
    if val != None:
        return int(val)
    return None

# get dict of courts from html form
def get_courts_from_html(html):
    courts = {}
    soup = BeautifulSoup(html)
    options = soup.find("select", {'id': 'searchRegisterForm:registerDataCircuitId'}).findAll('option')
    for option in options:
        #print option.contents, option['value']
        if int(option['value']) > 0:
            courts[int(option['value'])] = option.contents[0]
    return courts

# returns a randomly selected user agent strings
def get_random_ua_string():
    ua = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MRA 4.6 (build 01425))',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; de; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0'
    ]
    ua = shuffle(ua)
    return ua[0]

def shift_list(l, n):
    n = n % len(l)
    head = l[:n]
    del l[:n]
    l.extend(head)
    return l

# shift the list so that the last_id is at the beginning
def shift_ids(ids, last_id):
    if last_id in ids:
        return shift_list(ids, ids.index(last_id)+1)
    else:
        return ids

# loop through a complete search result for a given
# court ID and register type ID
#
def iterate_search_result(browser, court_id, register_type_id):
    global courts
    global register_types
    print "Getting entries of type "+ register_types[register_type_id] +" from court " + courts[court_id]

    browser.open(url)
    
    browser.select_form("searchRegisterForm")
    forms = browser.forms()
    
    browser["searchRegisterForm:registerDataCircuitId"] = [ str(court_id) ]
    browser["searchRegisterForm:registerDataRegisterType"] = [ str(register_type_id) ]
    
    response = browser.submit()
    
    links = list(browser.links(url_regex="registerPortal\.html"))
    # NOTE: This isn't too robust yet. There is hardly any qualification that this is the right link.
    response2 = browser.follow_link(links[0])
    
    first_result_page = response2.read()
    
    soup = BeautifulSoup(first_result_page)
    numhits = soup.find("div", { "id": "result_stats"} ).find("strong").string
    matches = re.search(r'([0-9]+)\s+Firm', numhits)
    if matches:
        print matches.group(1), "organizations within this search result (allegedly)."
        if int(matches.group(1)):
            # specify 100elements per page
            browser.select_form("hppForm")
            browser["hppForm:hitsperpage"] = ["100"]
            response = browser.submit()
            
            # get number of result pages
            link = browser.find_link(text_regex=r"Ende", nr=1)
            num_pages = 1
            for name, value in link.attrs:
                if name == 'href':
                    num_match = re.search(r'\.([0-9]+)=page', value)
                    if num_match:
                        num_pages = int(num_match.group(1))
            urlmask = link.base_url + link.url
            urlmask = re.sub('\.'+ str(num_pages) +'=page', '.%NUM%=page', urlmask)
            print "num pages:", num_pages
            #print "Reading page 1"
            html = response.get_data()
            parse_result_table(html, courts[court_id], register_types[register_type_id])
            
            # we randomize the sequence of result pages in order to cover all entries at some point
            randompages = shuffle(range(2,num_pages))
            
            # collect urls to be retried later
            retry_urls = []

            # loop through all results pages
            for pagenum in randompages:
                #print "Reading page", pagenum
                page_url = urlmask.replace('%NUM%', str(pagenum))
                try:
                    response = browser.open(page_url)
                    html = response.get_data()
                    parse_result_table(html, courts[court_id], register_types[register_type_id])
                except:
                    print "Error. Will try page "+ str(pagenum) + " later."
                    retry_urls.append(page_url)
            
            # handle failed attempts
            for page_url in retry_urls:
                print "Second attempt for URL " + page_url
                try:
                    response = browser.open(page_url)
                    html = response.get_data()
                    parse_result_table(html, courts[court_id], register_types[register_type_id])
                except:
                    print "Second attempt failed."


url = "https://www.unternehmensregister.de/ureg/search1.2.html"
current_court_id = 0
current_register_type = 1


# TODO: Read this directly from source
register_types = {
    1: "HRA",
    2: "HRB",
#    4: "Genossenschaftsregister",
#    5: "Partnerschaftsregister"
}

br = mechanize.Browser()
br.addheaders = [("User-agent", get_random_ua_string())]
br.set_handle_robots(False)

# First page request. If this fails, we end here.
try:
    response = br.open(url)
except e:
    print "Error in first HTTP request."
    print e
    sys.exit(1)

# Read courts dict from form
courts = get_courts_from_html(response.get_data())


# select random court for testing
#court_ids = shuffle(courts.keys())
court_ids = courts.keys()

# fast forwrd to where we left last time
last_court_id = get_last_court_id()
if last_court_id != None:
    court_ids = shift_ids(court_ids, last_court_id)

for court_id in court_ids:
    save_last_court_id(court_id)
    for register_type_id in register_types.keys():
        save_last_register_type_id(register_type_id)
        iterate_search_result(br, court_id, register_type_id)

# -*- coding: utf-8 -*-

import mechanize
from BeautifulSoup import BeautifulSoup
import re
import sys
import lxml.html
import scraperwiki
import random
from datetime import date

# TODO: Seed random generator with content from
# http://www.random.org/integers/?num=1&min=1&max=10000&col=1&base=10&format=plain&rnd=new

# randomize list
def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

# get rid of unwanted HTML entities and garbage
def cleanup_string(html):
    html = html.replace('&nbsp;', ' ')
    html = re.sub('\s+', ' ', html)
    t = lxml.html.fromstring(html)
    return t.text_content().strip()

# parses entries out of one search result table
# (first splitting table into multiple tables)
def parse_result_table(html, court, register_type):
    # split this damn table by header rows
    html_parts = re.split('<tr>\s*<td\s+colspan="[0-9]"\s+class="RegPortErg_AZ">', html)
    if len(html_parts):
        html = '</table> <table class="scrapableTable"><tr><td class="RegPortErg_AZ">'.join(html_parts)
        soup = BeautifulSoup(html)
        items = soup.findAll("table", { "class": "scrapableTable"} )
        for table in items:
            identifier_line = cleanup_string(table.find("td", {"class": "RegPortErg_AZ"}).find("b").string)
            idmatch = re.search('\s+([0-9]+)$', identifier_line)
            idnum = idmatch.group(1)
            state = cleanup_string(table.find("td", {"class": "RegPortErg_AZ"}).contents[0])
            name = cleanup_string(table.find("td", {"class": "RegPortErg_FirmaKopf"}).contents[0])
            location = cleanup_string(table.find("td", {"class": "RegPortErg_SitzStatusKopf"}).contents[0])
            today = date.today()
            record = {
                'court': court,
                'register_type': register_type,
                'idnum': idnum,
                'state': state,
                'name': name,
                'location': location,
                'last_seen': today.isoformat()
            }
            try:
                scraperwiki.sqlite.save(unique_keys=["court", "register_type", "idnum"], data=record)
            except:
                print "Could not write record", record


# save court status
def save_last_court_id(id):
    scraperwiki.sqlite.save_var('last_court_id', id)

# save register_type status
def save_last_register_type_id(id):
    scraperwiki.sqlite.save_var('last_register_type_id', id)

# get court status
def get_last_court_id():
    val = scraperwiki.sqlite.get_var('last_court_id')
    if val != None:
        return int(val)
    return None

# get dict of courts from html form
def get_courts_from_html(html):
    courts = {}
    soup = BeautifulSoup(html)
    options = soup.find("select", {'id': 'searchRegisterForm:registerDataCircuitId'}).findAll('option')
    for option in options:
        #print option.contents, option['value']
        if int(option['value']) > 0:
            courts[int(option['value'])] = option.contents[0]
    return courts

# returns a randomly selected user agent strings
def get_random_ua_string():
    ua = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MRA 4.6 (build 01425))',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; de; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0'
    ]
    ua = shuffle(ua)
    return ua[0]

def shift_list(l, n):
    n = n % len(l)
    head = l[:n]
    del l[:n]
    l.extend(head)
    return l

# shift the list so that the last_id is at the beginning
def shift_ids(ids, last_id):
    if last_id in ids:
        return shift_list(ids, ids.index(last_id)+1)
    else:
        return ids

# loop through a complete search result for a given
# court ID and register type ID
#
def iterate_search_result(browser, court_id, register_type_id):
    global courts
    global register_types
    print "Getting entries of type "+ register_types[register_type_id] +" from court " + courts[court_id]

    browser.open(url)
    
    browser.select_form("searchRegisterForm")
    forms = browser.forms()
    
    browser["searchRegisterForm:registerDataCircuitId"] = [ str(court_id) ]
    browser["searchRegisterForm:registerDataRegisterType"] = [ str(register_type_id) ]
    
    response = browser.submit()
    
    links = list(browser.links(url_regex="registerPortal\.html"))
    # NOTE: This isn't too robust yet. There is hardly any qualification that this is the right link.
    response2 = browser.follow_link(links[0])
    
    first_result_page = response2.read()
    
    soup = BeautifulSoup(first_result_page)
    numhits = soup.find("div", { "id": "result_stats"} ).find("strong").string
    matches = re.search(r'([0-9]+)\s+Firm', numhits)
    if matches:
        print matches.group(1), "organizations within this search result (allegedly)."
        if int(matches.group(1)):
            # specify 100elements per page
            browser.select_form("hppForm")
            browser["hppForm:hitsperpage"] = ["100"]
            response = browser.submit()
            
            # get number of result pages
            link = browser.find_link(text_regex=r"Ende", nr=1)
            num_pages = 1
            for name, value in link.attrs:
                if name == 'href':
                    num_match = re.search(r'\.([0-9]+)=page', value)
                    if num_match:
                        num_pages = int(num_match.group(1))
            urlmask = link.base_url + link.url
            urlmask = re.sub('\.'+ str(num_pages) +'=page', '.%NUM%=page', urlmask)
            print "num pages:", num_pages
            #print "Reading page 1"
            html = response.get_data()
            parse_result_table(html, courts[court_id], register_types[register_type_id])
            
            # we randomize the sequence of result pages in order to cover all entries at some point
            randompages = shuffle(range(2,num_pages))
            
            # collect urls to be retried later
            retry_urls = []

            # loop through all results pages
            for pagenum in randompages:
                #print "Reading page", pagenum
                page_url = urlmask.replace('%NUM%', str(pagenum))
                try:
                    response = browser.open(page_url)
                    html = response.get_data()
                    parse_result_table(html, courts[court_id], register_types[register_type_id])
                except:
                    print "Error. Will try page "+ str(pagenum) + " later."
                    retry_urls.append(page_url)
            
            # handle failed attempts
            for page_url in retry_urls:
                print "Second attempt for URL " + page_url
                try:
                    response = browser.open(page_url)
                    html = response.get_data()
                    parse_result_table(html, courts[court_id], register_types[register_type_id])
                except:
                    print "Second attempt failed."


url = "https://www.unternehmensregister.de/ureg/search1.2.html"
current_court_id = 0
current_register_type = 1


# TODO: Read this directly from source
register_types = {
    1: "HRA",
    2: "HRB",
#    4: "Genossenschaftsregister",
#    5: "Partnerschaftsregister"
}

br = mechanize.Browser()
br.addheaders = [("User-agent", get_random_ua_string())]
br.set_handle_robots(False)

# First page request. If this fails, we end here.
try:
    response = br.open(url)
except e:
    print "Error in first HTTP request."
    print e
    sys.exit(1)

# Read courts dict from form
courts = get_courts_from_html(response.get_data())


# select random court for testing
#court_ids = shuffle(courts.keys())
court_ids = courts.keys()

# fast forwrd to where we left last time
last_court_id = get_last_court_id()
if last_court_id != None:
    court_ids = shift_ids(court_ids, last_court_id)

for court_id in court_ids:
    save_last_court_id(court_id)
    for register_type_id in register_types.keys():
        save_last_register_type_id(register_type_id)
        iterate_search_result(br, court_id, register_type_id)

