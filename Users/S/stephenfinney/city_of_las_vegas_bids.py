import scraperwiki
import dateutil.parser
import lxml.html
import urlparse
import mechanize
import cookielib

#html = scraperwiki.scrape(html)
#print html
#root = lxml.html.fromstring(html)

# tds = root.cssselect('td')


def create_table():
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Bid ID' str, 'Title' str, 'Status' str, 'Broadcast Date' date, 'Due Date' date)")
    scraperwiki.sqlite.commit()


def initialize(url):
    #scrape_then_next_page('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275', 1)
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    #scrape_table(root)
    #br = mechanize.Browser()
    #br.set_handle_robots(False)
    #br.select_form(name="_ResultsState")
    #br.form.set_all_readonly(False)
    

    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    #scrape_table(root)
    br = mechanize.Browser()

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    response = br.open(url)
    scrape_then_next_page(url, br, 1)


def scrape_then_next_page(url, br, page_number):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #br = mechanize.Browser()

    #cj = cookielib.LWPCookieJar()
    #br.set_cookiejar(cj)

    #br.set_handle_robots(False)
    #response = br.open(url)
    br.select_form(name="_ResultsState")
    br.form.set_all_readonly(False)
    #next_link = root.cssselect("a.next")
    print "On page number: " + str(page_number)

    if page_number < 20:
        print "Inside if statement..."
        #br = mechanize.Browser()
        #br.set_handle_robots(False)
        #response = br.open(url)
        
        #br.select_form(name="_ResultsState")
        #print br.form
        
        #br.form.set_all_readonly(False)
        
        br["UTLIST_NORM_POSTED"] = "0"
        br["UTLIST_PAGENUMBER"] = str(page_number)
        
        #response = br.submit()
        #print response.read()    
        response = br.submit()

        page_number += 1
        scrape_then_next_page(url, br, page_number)


def scrape_table(root):
    rows = root.cssselect("table.ResultsTable tr")
    
    for row in rows:
        bid = {}
        cells = row.cssselect("td")
    
        if cells:
            bid['Bid ID']              = cells[0].text
            #print bid['Bid ID']
        
            bid['Status']              = cells[1].text
            #print bid['Status']
        
            bid['Broadcast Date']      = dateutil.parser.parse(cells[2].text.strip()).date().strftime('%m/%d/%y')
            #print bid['Broadcast Date']
        
            bid['Due Date']            = dateutil.parser.parse(cells[3].text.strip()).date().strftime('%m/%d/%y')
            #print bid['Due Date']
        
            bid['Title']               = cells[4].cssselect('p')[0].text_content()
            #print bid['Title']
    
            #bid['details_link']        = td[5].cssselect('a')[0].get('href'),
            #bid['planholders_link']    = td[5].cssselect('a')[1].get('href'),
            #bid['download_order_link'] = td[5].cssselect('a')[2].get('href'),
    
            scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=bid)

create_table()
initialize('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275')
#page_number = 1
import scraperwiki
import dateutil.parser
import lxml.html
import urlparse
import mechanize
import cookielib

#html = scraperwiki.scrape(html)
#print html
#root = lxml.html.fromstring(html)

# tds = root.cssselect('td')


def create_table():
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Bid ID' str, 'Title' str, 'Status' str, 'Broadcast Date' date, 'Due Date' date)")
    scraperwiki.sqlite.commit()


def initialize(url):
    #scrape_then_next_page('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275', 1)
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    #scrape_table(root)
    #br = mechanize.Browser()
    #br.set_handle_robots(False)
    #br.select_form(name="_ResultsState")
    #br.form.set_all_readonly(False)
    

    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    #scrape_table(root)
    br = mechanize.Browser()

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    response = br.open(url)
    scrape_then_next_page(url, br, 1)


def scrape_then_next_page(url, br, page_number):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #br = mechanize.Browser()

    #cj = cookielib.LWPCookieJar()
    #br.set_cookiejar(cj)

    #br.set_handle_robots(False)
    #response = br.open(url)
    br.select_form(name="_ResultsState")
    br.form.set_all_readonly(False)
    #next_link = root.cssselect("a.next")
    print "On page number: " + str(page_number)

    if page_number < 20:
        print "Inside if statement..."
        #br = mechanize.Browser()
        #br.set_handle_robots(False)
        #response = br.open(url)
        
        #br.select_form(name="_ResultsState")
        #print br.form
        
        #br.form.set_all_readonly(False)
        
        br["UTLIST_NORM_POSTED"] = "0"
        br["UTLIST_PAGENUMBER"] = str(page_number)
        
        #response = br.submit()
        #print response.read()    
        response = br.submit()

        page_number += 1
        scrape_then_next_page(url, br, page_number)


def scrape_table(root):
    rows = root.cssselect("table.ResultsTable tr")
    
    for row in rows:
        bid = {}
        cells = row.cssselect("td")
    
        if cells:
            bid['Bid ID']              = cells[0].text
            #print bid['Bid ID']
        
            bid['Status']              = cells[1].text
            #print bid['Status']
        
            bid['Broadcast Date']      = dateutil.parser.parse(cells[2].text.strip()).date().strftime('%m/%d/%y')
            #print bid['Broadcast Date']
        
            bid['Due Date']            = dateutil.parser.parse(cells[3].text.strip()).date().strftime('%m/%d/%y')
            #print bid['Due Date']
        
            bid['Title']               = cells[4].cssselect('p')[0].text_content()
            #print bid['Title']
    
            #bid['details_link']        = td[5].cssselect('a')[0].get('href'),
            #bid['planholders_link']    = td[5].cssselect('a')[1].get('href'),
            #bid['download_order_link'] = td[5].cssselect('a')[2].get('href'),
    
            scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=bid)

create_table()
initialize('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275')
#page_number = 1
import scraperwiki
import dateutil.parser
import lxml.html
import urlparse
import mechanize
import cookielib

#html = scraperwiki.scrape(html)
#print html
#root = lxml.html.fromstring(html)

# tds = root.cssselect('td')


def create_table():
    print "Creating table for data..."
    scraperwiki.sqlite.execute("drop table swdata")
    scraperwiki.sqlite.execute("create table swdata('Bid ID' str, 'Title' str, 'Status' str, 'Broadcast Date' date, 'Due Date' date)")
    scraperwiki.sqlite.commit()


def initialize(url):
    #scrape_then_next_page('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275', 1)
    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    #scrape_table(root)
    #br = mechanize.Browser()
    #br.set_handle_robots(False)
    #br.select_form(name="_ResultsState")
    #br.form.set_all_readonly(False)
    

    #html = scraperwiki.scrape(url)
    #root = lxml.html.fromstring(html)
    #scrape_table(root)
    br = mechanize.Browser()

    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    response = br.open(url)
    scrape_then_next_page(url, br, 1)


def scrape_then_next_page(url, br, page_number):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(root)
    #br = mechanize.Browser()

    #cj = cookielib.LWPCookieJar()
    #br.set_cookiejar(cj)

    #br.set_handle_robots(False)
    #response = br.open(url)
    br.select_form(name="_ResultsState")
    br.form.set_all_readonly(False)
    #next_link = root.cssselect("a.next")
    print "On page number: " + str(page_number)

    if page_number < 20:
        print "Inside if statement..."
        #br = mechanize.Browser()
        #br.set_handle_robots(False)
        #response = br.open(url)
        
        #br.select_form(name="_ResultsState")
        #print br.form
        
        #br.form.set_all_readonly(False)
        
        br["UTLIST_NORM_POSTED"] = "0"
        br["UTLIST_PAGENUMBER"] = str(page_number)
        
        #response = br.submit()
        #print response.read()    
        response = br.submit()

        page_number += 1
        scrape_then_next_page(url, br, page_number)


def scrape_table(root):
    rows = root.cssselect("table.ResultsTable tr")
    
    for row in rows:
        bid = {}
        cells = row.cssselect("td")
    
        if cells:
            bid['Bid ID']              = cells[0].text
            #print bid['Bid ID']
        
            bid['Status']              = cells[1].text
            #print bid['Status']
        
            bid['Broadcast Date']      = dateutil.parser.parse(cells[2].text.strip()).date().strftime('%m/%d/%y')
            #print bid['Broadcast Date']
        
            bid['Due Date']            = dateutil.parser.parse(cells[3].text.strip()).date().strftime('%m/%d/%y')
            #print bid['Due Date']
        
            bid['Title']               = cells[4].cssselect('p')[0].text_content()
            #print bid['Title']
    
            #bid['details_link']        = td[5].cssselect('a')[0].get('href'),
            #bid['planholders_link']    = td[5].cssselect('a')[1].get('href'),
            #bid['download_order_link'] = td[5].cssselect('a')[2].get('href'),
    
            scraperwiki.sqlite.save(unique_keys=['Bid ID'], data=bid)

create_table()
initialize('http://www.demandstar.com/supplier/bids/agency_inc/bid_list.asp?f=search&LP=BB&mi=%20116275')
#page_number = 1
