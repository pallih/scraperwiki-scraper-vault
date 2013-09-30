import scraperwiki
import mechanize
import re
import cookielib

url = 'http://groceries.asda.com/asda-estore/catalog/sectionpagecontainer.jsp?departmentid=1214921923714'
br = mechanize.Browser()
cj = mechanize.CookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=3)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.107 Safari/535.1')]

request = mechanize.Request(url)
response = br.open(url)


cj.extract_cookies(response, request)

request2 = mechanize.Request(url)
cj.add_cookie_header(request2)

response2 = br.open("http://groceries.asda.com/asda-estore/emerchandizing_section.jsp?departmentid=1214921923714&pageConfiguration=10000001&lastLogDetails=")

html = response2.read()
print response2.geturl()

#snag the itemimage

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
items = root.cssselect('.itemimage') 
for item in items:
    print lxml.html.tostring(item) # the full HTML tag
    print item.text # just the text inside the HTML tag
    

    record = { "td" : lxml.html.tostring(item) } # column name and value
    scraperwiki.datastore.save(["td"], record) # save the records one by one
import scraperwiki
import mechanize
import re
import cookielib

url = 'http://groceries.asda.com/asda-estore/catalog/sectionpagecontainer.jsp?departmentid=1214921923714'
br = mechanize.Browser()
cj = mechanize.CookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=3)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.107 Safari/535.1')]

request = mechanize.Request(url)
response = br.open(url)


cj.extract_cookies(response, request)

request2 = mechanize.Request(url)
cj.add_cookie_header(request2)

response2 = br.open("http://groceries.asda.com/asda-estore/emerchandizing_section.jsp?departmentid=1214921923714&pageConfiguration=10000001&lastLogDetails=")

html = response2.read()
print response2.geturl()

#snag the itemimage

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
items = root.cssselect('.itemimage') 
for item in items:
    print lxml.html.tostring(item) # the full HTML tag
    print item.text # just the text inside the HTML tag
    

    record = { "td" : lxml.html.tostring(item) } # column name and value
    scraperwiki.datastore.save(["td"], record) # save the records one by one
