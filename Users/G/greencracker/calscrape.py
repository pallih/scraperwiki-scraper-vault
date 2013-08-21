import scraperwiki

import mechanize
import cookielib
import urllib2
print "ok imports"
import time
from BeautifulSoup import BeautifulSoup

#V4383 is january 1
#V4390 is jan 8

viewstate =("/wEPDwUJMTExMjM2ODk4D2QWAgIDD2QWAgIBD2QWBGYPZBYCAgEPDxYCHgRUZXh0BQ5Ib3VzZSBNZWV0aW5nc2RkAgEPZBYCAgEPZBYCZg88KwAKAQAPFgQeC1Zpc2libGVEYXRlBgCAcnAvls4IHgJTRBYBBgBA3Jr4ls4IZGRkDtLNfM6R4MUXpFrEfRIdj8eqXw8=")
viewstate = viewstate.encode()
    
eventvalidation =("/wEWLQLHvPHLCwKfnPm5CAK0q4++DQLl9e7TBALl9fK0DALl9cbfCgLl9eqwAgLIn6b3CALIn8ooAsif3o0LAsif4uYCAsif9tsNAsifmr8FAsifrpAMAsifsvUHAsifhpwCAsifqvENAu+2hNgOAu+2qL0GAu+2vJYBAu+2wMsIAu+21CwC77b4gQsC77aM5QIC77aQ3g0C77bk5ggC77aI2gMCoNXJrQYCoNXdhgECoNXh+wgCoNX13AMCoNWZsAsCoNWtlQICoNWxzg0CoNXFowUCoNWpygMCoNW9rwsCx+yvtgwCx+yz6wcCx+zHzA4Cx+zroQYCx+z/mgECx+yD/ggCx+yX0wMCx+y7tAtFmcOmgVQF5a4znEYz+6BhSToTgQ==")

eventvalidation = eventvalidation.encode()
counter = 0
list_of_dates = ['V4383', 'V4390']
for counter in range (1):
    


    
    
    # Browser
    br = mechanize.Browser()
    print "ok mechanize"
    
    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    
    print "ok cookie"
    
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    
    print "ok options"
    
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
    print "ok handle"
    # Want debugging messages?
    br.set_debug_http(True)
    br.set_debug_redirects(True)
    br.set_debug_responses(True)
    
    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    print "ok headers"
    
    base_url = "http://webmail.legis.ga.gov/Calendar/"
    program_url = base_url + "?Chamber=house"
    r = br.open(program_url)
    
    html = r.read()
    #print br.response().read()
    
    # Show the html title
    print br.title()
    # Show the response headers
    print r.info()
    
    for f in br.forms():
        print f
    
    # Select the first (index zero) form
    br.select_form(nr=0)
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'V4384'
    br['__EVENTARGUMENT'] = 'calMain'
    br['__VIEWSTATE'] = viewstate
    br['__EVENTVALIDATION'] = eventvalidation
    
    
    response = br.submit()
    print type(response) #new line
    raw = br.response().read()#new line
    print type(raw)
    print raw
    soup = BeautifulSoup(raw)
    print "ok soup"
    print soup
    #this brings me to january but doesnt give me the bottom half of hte html

    selecttable = soup.find('table',{'id':"tblItems"})
    #print "got the table"
    rows = selecttable.findAll('tr',{'class':"cssItemsRowDark"})
    #print "got the rows"
    for row in rows:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['col1'] = table_cells[0].text
            record['col2'] = table_cells[1].text
            record['col3'] = table_cells[2].text
            print record
            scraperwiki.sqlite.save(unique_keys=['col1'], data=record)
    counter = counter+1
    time.sleep(30)
    
    


