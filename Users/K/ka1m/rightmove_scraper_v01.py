# Scrapes postcode avg rental data off Rightmove landlord intelligence page

import scraperwiki
import lxml.html
import mechanize 
import cgi
import time

def scrape():
    for item in root.cssselect("section#ahp span"):
        cleandata = item.text.translate(None, ',')
        ARP = int(cleandata)
    
    for item in root.cssselect("section#pm span"):
        cleandata = item.text.translate(None, ',')
        POM = int(cleandata)
        
    for item in root.cssselect("section#ts span"):
        cleandata = item.text.translate(None, ',')
        TS = int(cleandata)
    data = {'ARP': ARP, 'POM': POM, 'TS': TS}
    print data
    # scraperwiki.sqlite.save(unique_keys=['country'], data=data)

html = scraperwiki.scrape("http://www.rightmove.co.uk/landlord-intelligence/#landing_l")
root = lxml.html.fromstring(html)
url = "http://www.rightmove.co.uk/landlord-intelligence/#landing_l"
cj = mechanize.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

br.open(url)

# br.select_form(nr=0)
br.form = list(br.forms())[0]
br.form.set_all_readonly(False) # allow changing the .value of all controls

br.set_all_readonly(False)
br.find_control("u_submitpostcode").disable = True
br["u_postcode"] = "N43NG"
request = br.click()
response = br.open(request)
# response = br.submit()

print response.read()

# Trying to check what is being submitted & returned
# request = br.click()
# response = br.open(request)
# html = response.read()
# print html

# html = scraperwiki.scrape(response.read())
# scrape()

# scraperwiki.sqlite.save(unique_keys=['ARP', 'POM', 'TS'], data=data)
# Tried delaying before retrieval: time.sleep(10)
# imported from http://goo.gl/cyiKB (didn't work)
# br.form.new_control('text','__EVENTARGUMENT',{'value':''})
# br.form.new_control('text','__EVENTTARGET',{'value':''})
# br.form.fixup()
# br["__EVENTTARGET"] = 'lbSearch'
# br["__EVENTARGUMENT"] = ''
# Scrapes postcode avg rental data off Rightmove landlord intelligence page

import scraperwiki
import lxml.html
import mechanize 
import cgi
import time

def scrape():
    for item in root.cssselect("section#ahp span"):
        cleandata = item.text.translate(None, ',')
        ARP = int(cleandata)
    
    for item in root.cssselect("section#pm span"):
        cleandata = item.text.translate(None, ',')
        POM = int(cleandata)
        
    for item in root.cssselect("section#ts span"):
        cleandata = item.text.translate(None, ',')
        TS = int(cleandata)
    data = {'ARP': ARP, 'POM': POM, 'TS': TS}
    print data
    # scraperwiki.sqlite.save(unique_keys=['country'], data=data)

html = scraperwiki.scrape("http://www.rightmove.co.uk/landlord-intelligence/#landing_l")
root = lxml.html.fromstring(html)
url = "http://www.rightmove.co.uk/landlord-intelligence/#landing_l"
cj = mechanize.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# Want debugging messages?
br.set_debug_http(True)
br.set_debug_redirects(True)
br.set_debug_responses(True)

br.open(url)

# br.select_form(nr=0)
br.form = list(br.forms())[0]
br.form.set_all_readonly(False) # allow changing the .value of all controls

br.set_all_readonly(False)
br.find_control("u_submitpostcode").disable = True
br["u_postcode"] = "N43NG"
request = br.click()
response = br.open(request)
# response = br.submit()

print response.read()

# Trying to check what is being submitted & returned
# request = br.click()
# response = br.open(request)
# html = response.read()
# print html

# html = scraperwiki.scrape(response.read())
# scrape()

# scraperwiki.sqlite.save(unique_keys=['ARP', 'POM', 'TS'], data=data)
# Tried delaying before retrieval: time.sleep(10)
# imported from http://goo.gl/cyiKB (didn't work)
# br.form.new_control('text','__EVENTARGUMENT',{'value':''})
# br.form.new_control('text','__EVENTTARGET',{'value':''})
# br.form.fixup()
# br["__EVENTTARGET"] = 'lbSearch'
# br["__EVENTARGUMENT"] = ''
