import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
import time
from mechanize import ParseResponse
import urllib
import urllib2
import lxml.html
import re

# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
#print "ok mechanize"
    
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
    
#print "ok cookie"
    
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
    
#print "ok options"
    
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
#print "ok handle"
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)
    
# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
print "ok headers"
#--- end headers
url = "http://www.legis.ga.gov/Legislation/en-US/Search.aspx"
j = 2051
my_list = ["['1']", "['2']", "['3']"]
#---- end declarations

response = br.open(url)
html = response.read()
#print "ok have got html"
#print html
root = lxml.html.fromstring(html)
#print "ok have lxml'd it"

for form in br.forms():#    print "Form name:", form.name
    print form

for i in range(6000):
    form = br.select_form(nr=0)
#    print form
#    print "form selected"
    #print type(form)
    
    br.form.set_all_readonly(False)
    
    print "ok giting post_url"
    post_url, post_data, headers =  br.form.click_request_data()
    print post_url
    print post_data
    print headers
    print "ok that was the info"

    br.form.set_all_readonly(False)
    print "ok have set all to false"

    eventtarget_control = br.form.find_control("__EVENTTARGET")
    eventargument_control = br.form.find_control("__EVENTARGUMENT")
    viewstate_control = br.form.find_control("__VIEWSTATE")
    eventvalidation_control = br.form.find_control("__EVENTVALIDATION")
    requestdigest_control = br.form.find_control("__REQUESTDIGEST")
 
    print "ok have found the event target etc data"

    br.form['__EVENTTARGET'] = str(eventtarget_control.value)
    br.form['__EVENTARGUMENT'] = str(eventargument_control.value)
    br.form['__VIEWSTATE'] = str(viewstate_control.value)
    br.form['__EVENTVALIDATION'] = str(eventvalidation_control.value)
    br.form['__REQUESTDIGEST'] = str(requestdigest_control.value)
    br.form['ctl00$SPWebPartManager1$g_2cab3920_24b8_44c5_bff4_215b7b409b78$Number'] = str(j)
    
    print "ok have set the data to post"
    print "and this is bill number:"
    print j
    
    time.sleep(5)

    response = br.submit(name="ctl00$SPWebPartManager1$g_d53a2f93_1b7a_4bc1_920e_5744843a0677$ctl00")
    print "ok have hit submit for bill number:"
    print j
    print "and heres what it is:"
    html = response.read()
    print html
    root = lxml.html.fromstring(html)
    for div in root.cssselect('div.oddLegRow'):
        print "ok doing odd rows for bill number:" 
        print j
        time.sleep(1)
        print div.text_content()
        data = {
        'row10' : div.text_content(),
         }
        scraperwiki.sqlite.save(unique_keys=['row10'], data = data)
    for div in root.cssselect('div.evenLegRow'):
        print "ok doing even rows for bill number:"
        print j
        time.sleep(1)
        print div.text_content()
        data = {
        'row10' : div.text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=['row10'], data = data)
    time.sleep(5)
    j = j + 1import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import cookielib
import time
from mechanize import ParseResponse
import urllib
import urllib2
import lxml.html
import re

# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())
#print "ok mechanize"
    
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
    
#print "ok cookie"
    
# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
    
#print "ok options"
    
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    
#print "ok handle"
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)
    
# User-Agent 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
print "ok headers"
#--- end headers
url = "http://www.legis.ga.gov/Legislation/en-US/Search.aspx"
j = 2051
my_list = ["['1']", "['2']", "['3']"]
#---- end declarations

response = br.open(url)
html = response.read()
#print "ok have got html"
#print html
root = lxml.html.fromstring(html)
#print "ok have lxml'd it"

for form in br.forms():#    print "Form name:", form.name
    print form

for i in range(6000):
    form = br.select_form(nr=0)
#    print form
#    print "form selected"
    #print type(form)
    
    br.form.set_all_readonly(False)
    
    print "ok giting post_url"
    post_url, post_data, headers =  br.form.click_request_data()
    print post_url
    print post_data
    print headers
    print "ok that was the info"

    br.form.set_all_readonly(False)
    print "ok have set all to false"

    eventtarget_control = br.form.find_control("__EVENTTARGET")
    eventargument_control = br.form.find_control("__EVENTARGUMENT")
    viewstate_control = br.form.find_control("__VIEWSTATE")
    eventvalidation_control = br.form.find_control("__EVENTVALIDATION")
    requestdigest_control = br.form.find_control("__REQUESTDIGEST")
 
    print "ok have found the event target etc data"

    br.form['__EVENTTARGET'] = str(eventtarget_control.value)
    br.form['__EVENTARGUMENT'] = str(eventargument_control.value)
    br.form['__VIEWSTATE'] = str(viewstate_control.value)
    br.form['__EVENTVALIDATION'] = str(eventvalidation_control.value)
    br.form['__REQUESTDIGEST'] = str(requestdigest_control.value)
    br.form['ctl00$SPWebPartManager1$g_2cab3920_24b8_44c5_bff4_215b7b409b78$Number'] = str(j)
    
    print "ok have set the data to post"
    print "and this is bill number:"
    print j
    
    time.sleep(5)

    response = br.submit(name="ctl00$SPWebPartManager1$g_d53a2f93_1b7a_4bc1_920e_5744843a0677$ctl00")
    print "ok have hit submit for bill number:"
    print j
    print "and heres what it is:"
    html = response.read()
    print html
    root = lxml.html.fromstring(html)
    for div in root.cssselect('div.oddLegRow'):
        print "ok doing odd rows for bill number:" 
        print j
        time.sleep(1)
        print div.text_content()
        data = {
        'row10' : div.text_content(),
         }
        scraperwiki.sqlite.save(unique_keys=['row10'], data = data)
    for div in root.cssselect('div.evenLegRow'):
        print "ok doing even rows for bill number:"
        print j
        time.sleep(1)
        print div.text_content()
        data = {
        'row10' : div.text_content(),
        }
        scraperwiki.sqlite.save(unique_keys=['row10'], data = data)
    time.sleep(5)
    j = j + 1