import urllib
import scraperwiki
import re
import time
import mechanize
from BeautifulSoup import BeautifulSoup

START_URL = \
'http://www.charitycommission.gov.uk' + \
'/ShowCharity/RegisterOfCharities/AdvancedSearch.aspx'

# 15 is a little too slow, but 10 is causing an exception for running too long
SLEEP_NICE = 7 #seconds

scraperwiki.metadata.save('data_columns',
  ['number','name','status', 
    'trustee.id','trustee.name','trustee.link', 
    'contact.name',
    'contact.address.line1',
    'contact.address.line2',
    'contact.address.line3',
    'contact.address.line4',
    'contact.address.line5',
    'contact.address.line6',
    'contact.telephone',
    'contact.email',
    'contact.website'
  ])

registered_id_url = {}

def do_scrape( url, params=None ):
    br = mechanize.Browser()
    if False:
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        #br.set_debug_responses(True)
        #print "\n".join([x for x in dir(br) if not x.startswith('_') ])
    br.set_handle_robots(False)
    # br.addheaders = [ ('User-Agent', USER_AGENT) ]

    reqbody = None
    if params:
        reqbody = urllib.urlencode( params )
    br.open( url, data=reqbody )
    return br

def results_page( browser, soup ):
    global SLEEP_TIME
    dataTable = soup.find('table', {'id':'ctl00_MainContent_gridView'})
    for tr in dataTable.findAll('tr'):
        tds = tr.findAll('td')
        if 0 == len(tds):
            # it's the header, don't worry
            continue
        elif 1 == len(tds) and tds[0]['colspan']=='3':
            # footer, we're done here
            break
        elif 3 != len(tds):
            print "BOGUS, expected 3 but found %d td children" % len(tds)
            continue
        num_link = tds[0].find('a')
        num = num_link.text
        reg_url = num_link['href']
        if not reg_url.startswith('http'):
            base_url = urllib.basejoin( browser.geturl(), './' )
            reg_url = urllib.basejoin( base_url, reg_url )
        name = tds[1].text
        status = tds[2].text
        record = {}
        record['number'] = num
        record['name'] = name
        record['status'] = status
        registered_id_url[ num ] = reg_url
        scraperwiki.datastore.save(['number'], record)
    nextLink = soup.find('input',{'type':'submit','value':'Next'})
    if not nextLink:
        print "Done"
        return False
    nextName = nextLink['name']
    # print "Sleeping %d seconds..." % SLEEP_NICE
    time.sleep( SLEEP_NICE )
    browser.select_form('aspnetForm')
    browser.submit( name=nextName, type='submit' )
    return True

def pagination( advSearchURL ):
    brow = do_scrape( advSearchURL )
    brow.select_form('aspnetForm')

    # namespace mangling
    advSearchData = brow
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateFrom$DropDownListDay'] = ['1']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateFrom$DropDownListMonth'] = ['January']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateFrom$DropDownListYear'] = ['1'] # 2011
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateTo$DropDownListDay'] = ['1']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateTo$DropDownListMonth'] = ['December']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateTo$DropDownListYear'] = ['1'] # 2011
    
    brow.submit(name='ctl00$MainContent$buttonSearch',type='submit')
    html = brow.response().get_data()
    while html:
        soup = BeautifulSoup( html )
        if not results_page( brow, soup ):
            break
        html = brow.response().get_data()
        # again!
    # bye!

def run_contacts( browser, charityid ):

    html = browser.response().get_data()
    soup = BeautifulSoup( html )
    fieldmap = {}
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblContactName' \
            ] = 'contact.name'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine1' \
            ] = 'contact.address.line1'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine2' \
            ] = 'contact.address.line2'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine3' \
            ] = 'contact.address.line3'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine4' \
            ] = 'contact.address.line4'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine5' \
            ] = 'contact.address.line5'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine6' \
            ] = 'contact.address.line6'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblPhone' \
            ] = 'contact.telephone'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_hlEmail' \
            ] = 'contact.email'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_hlWebsite' \
            ] = 'contact.website'
    if True: # lexical scoping
        record = {}
        record['contact.charityid'] = charityid
        for fid in fieldmap.keys():
            record_name = fieldmap[ fid ]
            it = soup.find(name=None, attrs={'id':fid})
            record[ record_name ] = it.text
        scraperwiki.datastore.save(['contact.charityid','contact.name'], record)
    trustees_div = soup.find('div', \
                          {'class':'ScrollingSelectionLeftColumn'})
    # this spanid is in a different div :(
    # ctl00_MainContent_shTrustees_cvalHeader
    if not trustees_div:
        print "Unable to find any Trustees for %s" % dataurl
        return
    trustees_by_id = {}
    for tee in trustees_div.findAll('a'):
        tee_link = tee['href']
        if not tee_link.startswith('http'):
            base_url = browser.geturl()
            base_url = urllib.basejoin( base_url, './' )
            tee_link = urllib.basejoin( base_url, tee_link )
        ma = re.search(r'TID=(\d+)',tee_link)
        if not ma:
            print "Unable to identify TrusteeID in %s" % tee_link
            continue
        tee_id = ma.group(1)
        record = {}
        record['trustee.id'] = tee_id
        record['trustee.name'] = tee.text
        record['trustee.link'] = tee_link
        scraperwiki.datastore.save(['trustee.id'], record)
        trustees_by_id[ tee_id ] = record

def run_summary( browser, charityid ):
    '''
http://www.charitycommission.gov.uk/Showcharity/RegisterOfCharities/CharityWithoutPartB.aspx?RegisteredCharityNumber=1055335&SubsidiaryNumber=0
'''
    html = browser.response().get_data()
    soup = BeautifulSoup( html )
    if False: #TODO
        fieldmap = {}
        fieldmap[ \
        'ctl00$MainContent$ucDisplay$ucActivities$ucTextAreaInput$txtTextEntry' \
            ] = 'charity.activities'
        fieldmap[ \
        'ctl00$MainContent$ucDisplay$ucWhereOperates$ucTextAreaInput$txtTextEntry' \
            ] = 'charity.where'
    try:
        browser.follow_link(url_regex=r'ContactAndTrustees.*RegisteredCharityNumber')
    except Exception, ex:
        print "Unable to find RegisteredCharityNumber link due to %s" % ex
        return
    run_contacts( browser, charityid )


def run_registered_list( registered_id_url ):
    global SLEEP_NICE
    for charityid in registered_id_url.keys():
        the_url = registered_id_url[ charityid ]
        # print "FETCH-DETAILS",rid,"\t",r_url
        browser = do_scrape( the_url )
        run_summary( browser, charityid )
        # print "Sleeping %d seconds..." % SLEEP_NICE
        time.sleep( SLEEP_NICE )

# Action!
pagination( START_URL )
print "Found %d registered charities..." % (len(registered_id_url))
run_registered_list( registered_id_url )

import urllib
import scraperwiki
import re
import time
import mechanize
from BeautifulSoup import BeautifulSoup

START_URL = \
'http://www.charitycommission.gov.uk' + \
'/ShowCharity/RegisterOfCharities/AdvancedSearch.aspx'

# 15 is a little too slow, but 10 is causing an exception for running too long
SLEEP_NICE = 7 #seconds

scraperwiki.metadata.save('data_columns',
  ['number','name','status', 
    'trustee.id','trustee.name','trustee.link', 
    'contact.name',
    'contact.address.line1',
    'contact.address.line2',
    'contact.address.line3',
    'contact.address.line4',
    'contact.address.line5',
    'contact.address.line6',
    'contact.telephone',
    'contact.email',
    'contact.website'
  ])

registered_id_url = {}

def do_scrape( url, params=None ):
    br = mechanize.Browser()
    if False:
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        #br.set_debug_responses(True)
        #print "\n".join([x for x in dir(br) if not x.startswith('_') ])
    br.set_handle_robots(False)
    # br.addheaders = [ ('User-Agent', USER_AGENT) ]

    reqbody = None
    if params:
        reqbody = urllib.urlencode( params )
    br.open( url, data=reqbody )
    return br

def results_page( browser, soup ):
    global SLEEP_TIME
    dataTable = soup.find('table', {'id':'ctl00_MainContent_gridView'})
    for tr in dataTable.findAll('tr'):
        tds = tr.findAll('td')
        if 0 == len(tds):
            # it's the header, don't worry
            continue
        elif 1 == len(tds) and tds[0]['colspan']=='3':
            # footer, we're done here
            break
        elif 3 != len(tds):
            print "BOGUS, expected 3 but found %d td children" % len(tds)
            continue
        num_link = tds[0].find('a')
        num = num_link.text
        reg_url = num_link['href']
        if not reg_url.startswith('http'):
            base_url = urllib.basejoin( browser.geturl(), './' )
            reg_url = urllib.basejoin( base_url, reg_url )
        name = tds[1].text
        status = tds[2].text
        record = {}
        record['number'] = num
        record['name'] = name
        record['status'] = status
        registered_id_url[ num ] = reg_url
        scraperwiki.datastore.save(['number'], record)
    nextLink = soup.find('input',{'type':'submit','value':'Next'})
    if not nextLink:
        print "Done"
        return False
    nextName = nextLink['name']
    # print "Sleeping %d seconds..." % SLEEP_NICE
    time.sleep( SLEEP_NICE )
    browser.select_form('aspnetForm')
    browser.submit( name=nextName, type='submit' )
    return True

def pagination( advSearchURL ):
    brow = do_scrape( advSearchURL )
    brow.select_form('aspnetForm')

    # namespace mangling
    advSearchData = brow
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateFrom$DropDownListDay'] = ['1']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateFrom$DropDownListMonth'] = ['January']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateFrom$DropDownListYear'] = ['1'] # 2011
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateTo$DropDownListDay'] = ['1']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateTo$DropDownListMonth'] = ['December']
    advSearchData['ctl00$MainContent$searchdatesRegistration$searchdatesSearchdateTo$DropDownListYear'] = ['1'] # 2011
    
    brow.submit(name='ctl00$MainContent$buttonSearch',type='submit')
    html = brow.response().get_data()
    while html:
        soup = BeautifulSoup( html )
        if not results_page( brow, soup ):
            break
        html = brow.response().get_data()
        # again!
    # bye!

def run_contacts( browser, charityid ):

    html = browser.response().get_data()
    soup = BeautifulSoup( html )
    fieldmap = {}
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblContactName' \
            ] = 'contact.name'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine1' \
            ] = 'contact.address.line1'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine2' \
            ] = 'contact.address.line2'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine3' \
            ] = 'contact.address.line3'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine4' \
            ] = 'contact.address.line4'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine5' \
            ] = 'contact.address.line5'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblAddressLine6' \
            ] = 'contact.address.line6'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_lblPhone' \
            ] = 'contact.telephone'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_hlEmail' \
            ] = 'contact.email'
    fieldmap[ \
        'ctl00_MainContent_ucDisplay_ucContactDetails_hlWebsite' \
            ] = 'contact.website'
    if True: # lexical scoping
        record = {}
        record['contact.charityid'] = charityid
        for fid in fieldmap.keys():
            record_name = fieldmap[ fid ]
            it = soup.find(name=None, attrs={'id':fid})
            record[ record_name ] = it.text
        scraperwiki.datastore.save(['contact.charityid','contact.name'], record)
    trustees_div = soup.find('div', \
                          {'class':'ScrollingSelectionLeftColumn'})
    # this spanid is in a different div :(
    # ctl00_MainContent_shTrustees_cvalHeader
    if not trustees_div:
        print "Unable to find any Trustees for %s" % dataurl
        return
    trustees_by_id = {}
    for tee in trustees_div.findAll('a'):
        tee_link = tee['href']
        if not tee_link.startswith('http'):
            base_url = browser.geturl()
            base_url = urllib.basejoin( base_url, './' )
            tee_link = urllib.basejoin( base_url, tee_link )
        ma = re.search(r'TID=(\d+)',tee_link)
        if not ma:
            print "Unable to identify TrusteeID in %s" % tee_link
            continue
        tee_id = ma.group(1)
        record = {}
        record['trustee.id'] = tee_id
        record['trustee.name'] = tee.text
        record['trustee.link'] = tee_link
        scraperwiki.datastore.save(['trustee.id'], record)
        trustees_by_id[ tee_id ] = record

def run_summary( browser, charityid ):
    '''
http://www.charitycommission.gov.uk/Showcharity/RegisterOfCharities/CharityWithoutPartB.aspx?RegisteredCharityNumber=1055335&SubsidiaryNumber=0
'''
    html = browser.response().get_data()
    soup = BeautifulSoup( html )
    if False: #TODO
        fieldmap = {}
        fieldmap[ \
        'ctl00$MainContent$ucDisplay$ucActivities$ucTextAreaInput$txtTextEntry' \
            ] = 'charity.activities'
        fieldmap[ \
        'ctl00$MainContent$ucDisplay$ucWhereOperates$ucTextAreaInput$txtTextEntry' \
            ] = 'charity.where'
    try:
        browser.follow_link(url_regex=r'ContactAndTrustees.*RegisteredCharityNumber')
    except Exception, ex:
        print "Unable to find RegisteredCharityNumber link due to %s" % ex
        return
    run_contacts( browser, charityid )


def run_registered_list( registered_id_url ):
    global SLEEP_NICE
    for charityid in registered_id_url.keys():
        the_url = registered_id_url[ charityid ]
        # print "FETCH-DETAILS",rid,"\t",r_url
        browser = do_scrape( the_url )
        run_summary( browser, charityid )
        # print "Sleeping %d seconds..." % SLEEP_NICE
        time.sleep( SLEEP_NICE )

# Action!
pagination( START_URL )
print "Found %d registered charities..." % (len(registered_id_url))
run_registered_list( registered_id_url )

