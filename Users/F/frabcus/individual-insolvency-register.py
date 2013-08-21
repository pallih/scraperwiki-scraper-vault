import scraperwiki.datastore
import scraperwiki.geo
import lxml.html
import re
import sys
import mechanize
import datetime


###################################
# Parameters

name_or_trading = 'NAME' # or 'TRADING'
court = 'ALL'

###################################
# Helper functions

def only(seq):
    assert len(seq)==1
    return seq[0]

def parse_name_page(response_html, br):
    page = lxml.html.document_fromstring(response_html)
    table = only(page.cssselect('table[id=MyTable]'))
    for tr in table.cssselect('tr'):
        tds = tr.cssselect('td')
        tds = [td.text_content().strip() for td in tds]
        if tds[0] == 'Forename':
            continue
    
        rec = {}
        rec['forename'] = tds[0]
        rec['surname'] = tds[1]
        if tds[2] != '':
            rec['date_of_birth'] = datetime.date(int(tds[2][6:10]), int(tds[2][3:5]), int(tds[2][0:2]))
        else:
            rec['date_of_birth'] = None
        rec['court'] = tds[3]
        rec['case_number'] = tds[4]
        rec['start_date'] = datetime.date(int(tds[5][6:10]), int(tds[5][3:5]), int(tds[5][0:2]))
        rec['case_type'] = tds[6]
        
        # get their address from the subpage
        detail_response = br.follow_link(text_regex=r"^%s$" % rec['surname'])    
        detail_response_html = detail_response.read()
        #print [detail_response_html]
        #address = re.findall('<strong>Last Known Address</strong>\s+</td>\s+<td valign="top">([^<]+)</td>', detail_response_html)
        address = re.compile('(?s)<strong>Last Known Address</strong>\s+</td>\s+<td valign="top">(.+?)</td>', re.MULTILINE).findall(detail_response_html)[0]
        address = address.strip()
        address = address.replace('<br>', ', ')
        address = re.sub(', $', '', address)
        postcode = re.findall("[A-Z]+\d+\s*\d+[A-Z]+", address)
        if postcode:
            postcode = postcode[0]
        br.back()
        rec['address'] = address
        rec['postcode'] = postcode
        latlng = None
        if postcode:
            print "geocoding postcode", postcode
            latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)

        # XXX I've no idea what the unique key here should be, needs research    
        rec['latlng_lat'], rec['latlng_lng'] = latlng
        scraperwiki.sqlite.save(['court', 'case_number'], rec)

    page_info = re.findall("Page <font color='#ff0000'><strong>(\d+)</strong></font> of <font color='#ff0000'><strong>(\d+)</strong></font> pages", response_html)[0]
    print "page of:", page_info
    page_number = int(page_info[0])
    page_total = int(page_info[1])
    
    if page_number == page_total:
        return None
    return page_number + 1

###################################
# Main loop

# load in initial page
br = mechanize.Browser()
br.open("http://www.insolvencydirect.bis.gov.uk/eiir/")
br.select_form(name="frmMaster")

# choose whether it is people or companies we're working on 
br.form.find_control('OPTION').readonly = False
br['OPTION'] = name_or_trading
response = br.submit()

br.select_form(name="OfficeCourtForm")
br.form.find_control('court').readonly = False
br.form.find_control('name').readonly = False
br['court'] = court
br['name'] = court
response = br.submit()

alphabet = map(chr, range(65, 91)) # A to Z
for letter in alphabet:
    print "Going to letter %s" % letter
    br.select_form(name="NameDetails")
    br['surnamesearch'] = letter
    response = br.submit()
    response_html = response.read()

    back_count = 1
    while 1:
        next_page = parse_name_page(response_html, br)
        if not next_page:
            break
        back_count = back_count + 1
        print "Going to page %d" % next_page
        response = br.follow_link(text_regex=r"^%d$" % next_page)    
        response_html = response.read()
    
    br.back(back_count)
