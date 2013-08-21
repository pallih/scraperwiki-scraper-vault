import scraperwiki
import lxml.html
import mechanize
import urllib2

def scrape_table():
    print "in scrape_table"
    url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table.ResultsTable tr")
    for row in rows:
        bid = {}
        cells = row.cssselect("td")
        if cells:
            bid['id']                  = cells[0].text        
            bid['status']              = cells[1].text        
            bid['broadcast_date']      = cells[2].text        
            bid['due_date']            = cells[3].text        
            bid['name']                = cells[4].cssselect('p')[0].text_content()        
            scraperwiki.sqlite.save(unique_keys=['id'], data=bid)

def do(br):
    #url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    scrape_table()
    
    #br = mechanize.Browser()
    #br.set_handle_robots(False)
    #br.set_handle_equiv(True)
    #br.set_handle_redirect(True)
    #br.set_handle_referer(True)
    #br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)
    #response = br.open(url)
    #print response
           
    br.select_form(name="_ResultsState")       
    br.form.set_all_readonly(False)
            
    br["UTLIST_NORM_POSTED"] = "0"
    br["UTLIST_PAGENUMBER"] = "2"     
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(br._ua_handlers["_cookies"].cookiejar))
    #opener.open(url)   
    response = br.submit()
    #response = br.follow_link(text_regex='next')
    print response
    
def init():
    url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)
    response = br.open(url)
    print response
    return br

br = init()
count = 1
while count <= 2:
    do(br)
    print "done with iteration " + str(count)
    count += 1
import scraperwiki
import lxml.html
import mechanize
import urllib2

def scrape_table():
    print "in scrape_table"
    url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table.ResultsTable tr")
    for row in rows:
        bid = {}
        cells = row.cssselect("td")
        if cells:
            bid['id']                  = cells[0].text        
            bid['status']              = cells[1].text        
            bid['broadcast_date']      = cells[2].text        
            bid['due_date']            = cells[3].text        
            bid['name']                = cells[4].cssselect('p')[0].text_content()        
            scraperwiki.sqlite.save(unique_keys=['id'], data=bid)

def do(br):
    #url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    scrape_table()
    
    #br = mechanize.Browser()
    #br.set_handle_robots(False)
    #br.set_handle_equiv(True)
    #br.set_handle_redirect(True)
    #br.set_handle_referer(True)
    #br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)
    #response = br.open(url)
    #print response
           
    br.select_form(name="_ResultsState")       
    br.form.set_all_readonly(False)
            
    br["UTLIST_NORM_POSTED"] = "0"
    br["UTLIST_PAGENUMBER"] = "2"     
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(br._ua_handlers["_cookies"].cookiejar))
    #opener.open(url)   
    response = br.submit()
    #response = br.follow_link(text_regex='next')
    print response
    
def init():
    url = 'http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275'
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #br.set_debug_http(True)
    #br.set_debug_redirects(True)
    #br.set_debug_responses(True)
    response = br.open(url)
    print response
    return br

br = init()
count = 1
while count <= 2:
    do(br)
    print "done with iteration " + str(count)
    count += 1
