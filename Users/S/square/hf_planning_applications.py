import scraperwiki
from datetime import datetime
from lxml.html import tostring, fromstring
import httplib2, urllib

http = httplib2.Http()

base_url = "http://public-access.lbhf.gov.uk"

def get_applications(results):
    for result in results:
        ahref = result.cssselect("a")[0]
        link = ahref.attrib["href"]
        title = ahref.text_content().strip()
        address = result.cssselect("p.address")[0].text_content().strip()
        metainfo = result.cssselect("p.metaInfo")[0].text_content().split("|")

        reference = metainfo[0].replace("Ref. No:", "").strip()
        str_date_registered = metainfo[1].replace("Registered:", "").strip()
        if (str_date_registered != ''):
            date_registered = datetime.strptime(str_date_registered, '%a %d %b %Y')
        status = metainfo[2].replace("Status:", "").strip()

        print reference, link, title, address, date_registered, status

        data = {
            'reference' : reference,
            'link' : base_url + link,
            'title' : title,
            'address' : address,
            'date_registered' : date_registered,
            'date_scraped' : datetime.now(),
            'status' : status
        }
        scraperwiki.sqlite.save(unique_keys=['reference'], data=data)

def get_paged_results(cookie, page=0, total_pages=0):
    print 'get_paged_results', page, total_pages
    if page == 0:
        page = 1
    results_per_page = 100

    headers = {
        'Cookie' : cookie,
        'Content-type': 'application/x-www-form-urlencoded', 
        'connection': 'close'}
    body = {
        'searchCriteria.page': page,
        'searchCriteria.resultsPerPage': results_per_page,
        'action': 'page'
    }
    response, content = http.request(base_url + "/online-applications/pagedSearchResults.do", 'POST', headers=headers, body=urllib.urlencode(body))

    root = fromstring(content.decode('utf-8'))
    results = root.cssselect("ul#searchresults li")
    get_applications(results)

    if total_pages == 0:
        # first time through this function, check for more results
        pager = root.cssselect('div#searchResultsContainer p span.showing')
        if len(pager) > 0:
            number_of_results = pager[0].text_content().replace('Showing 1-' + str(results_per_page) + ' of ','')
            print number_of_results
            total_pages = (int(number_of_results) / results_per_page) + 1
            get_paged_results(cookie, 2, total_pages)
    elif page != total_pages:
        # second or greater time through this function, get next page if not finished
        get_paged_results(cookie, page + 1, total_pages)

def get_results(cookie, date_type, week):
    headers = {
        'Cookie' : cookie,
        'Content-type': 'application/x-www-form-urlencoded', 
        'connection': 'close'}
    body = {
        'week': week,
        'searchType': 'Application',
        'dateType': date_type
    }
    response, content = http.request(base_url + "/online-applications/weeklyListResults.do?action=firstPage", 'POST', headers=headers, body=urllib.urlencode(body))

    root = fromstring(content.decode('utf-8'))
    pager = root.cssselect('div#searchResultsContainer p span.showing')
    if len(pager) == 0:
        results = root.cssselect("ul#searchresults li")
        get_applications(results)
    else:
        # there is more than one page of results, get more results per page and then page from there
        get_paged_results(cookie)

def run_scraper():
    response, content = http.request(base_url + "/online-applications/search.do?action=weeklyList")

    cookie = response['set-cookie']
    root = fromstring(content.decode('utf-8'))
    week = root.cssselect('form#weeklyListForm fieldset select#week option')[0].text_content()

    get_results(cookie, 'DC_Validated', week)
    get_results(cookie, 'DC_Decided', week)

run_scraper()
import scraperwiki
from datetime import datetime
from lxml.html import tostring, fromstring
import httplib2, urllib

http = httplib2.Http()

base_url = "http://public-access.lbhf.gov.uk"

def get_applications(results):
    for result in results:
        ahref = result.cssselect("a")[0]
        link = ahref.attrib["href"]
        title = ahref.text_content().strip()
        address = result.cssselect("p.address")[0].text_content().strip()
        metainfo = result.cssselect("p.metaInfo")[0].text_content().split("|")

        reference = metainfo[0].replace("Ref. No:", "").strip()
        str_date_registered = metainfo[1].replace("Registered:", "").strip()
        if (str_date_registered != ''):
            date_registered = datetime.strptime(str_date_registered, '%a %d %b %Y')
        status = metainfo[2].replace("Status:", "").strip()

        print reference, link, title, address, date_registered, status

        data = {
            'reference' : reference,
            'link' : base_url + link,
            'title' : title,
            'address' : address,
            'date_registered' : date_registered,
            'date_scraped' : datetime.now(),
            'status' : status
        }
        scraperwiki.sqlite.save(unique_keys=['reference'], data=data)

def get_paged_results(cookie, page=0, total_pages=0):
    print 'get_paged_results', page, total_pages
    if page == 0:
        page = 1
    results_per_page = 100

    headers = {
        'Cookie' : cookie,
        'Content-type': 'application/x-www-form-urlencoded', 
        'connection': 'close'}
    body = {
        'searchCriteria.page': page,
        'searchCriteria.resultsPerPage': results_per_page,
        'action': 'page'
    }
    response, content = http.request(base_url + "/online-applications/pagedSearchResults.do", 'POST', headers=headers, body=urllib.urlencode(body))

    root = fromstring(content.decode('utf-8'))
    results = root.cssselect("ul#searchresults li")
    get_applications(results)

    if total_pages == 0:
        # first time through this function, check for more results
        pager = root.cssselect('div#searchResultsContainer p span.showing')
        if len(pager) > 0:
            number_of_results = pager[0].text_content().replace('Showing 1-' + str(results_per_page) + ' of ','')
            print number_of_results
            total_pages = (int(number_of_results) / results_per_page) + 1
            get_paged_results(cookie, 2, total_pages)
    elif page != total_pages:
        # second or greater time through this function, get next page if not finished
        get_paged_results(cookie, page + 1, total_pages)

def get_results(cookie, date_type, week):
    headers = {
        'Cookie' : cookie,
        'Content-type': 'application/x-www-form-urlencoded', 
        'connection': 'close'}
    body = {
        'week': week,
        'searchType': 'Application',
        'dateType': date_type
    }
    response, content = http.request(base_url + "/online-applications/weeklyListResults.do?action=firstPage", 'POST', headers=headers, body=urllib.urlencode(body))

    root = fromstring(content.decode('utf-8'))
    pager = root.cssselect('div#searchResultsContainer p span.showing')
    if len(pager) == 0:
        results = root.cssselect("ul#searchresults li")
        get_applications(results)
    else:
        # there is more than one page of results, get more results per page and then page from there
        get_paged_results(cookie)

def run_scraper():
    response, content = http.request(base_url + "/online-applications/search.do?action=weeklyList")

    cookie = response['set-cookie']
    root = fromstring(content.decode('utf-8'))
    week = root.cssselect('form#weeklyListForm fieldset select#week option')[0].text_content()

    get_results(cookie, 'DC_Validated', week)
    get_results(cookie, 'DC_Decided', week)

run_scraper()
