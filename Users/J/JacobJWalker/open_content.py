# This scraper, which needs to be named, goes through a list of domains and using google determines how many pages have open content
# Note, this scrapes google through a proxy for research purposes, as allowed and protected by fair use and Google not being evil (in theory)


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse
import urllib2
import random
import time


# Find Proxies at http://hidemyass.com/proxy-list/search-225446
possible_as_rights = ['cc_publicdomain', 'cc_attribute', 'cc_sharealike', 'cc_noncommercial', 'cc_nonderived']

# Load Proxy Server List
scraperwiki.sqlite.attach("hide_my_ass_proxy_list_ip_14", "proxylist")
all_proxies = scraperwiki.sqlite.select("ipaddress from proxylist.hidemyass where port=80")
print all_proxies


# Load Domains from Webometrics Ranking Web of Universities Scraper
scraperwiki.sqlite.attach("webometrics_ranking_web_of_universities", "webometrics")
all_domains = scraperwiki.sqlite.select("domain from webometrics.swdata")

try:
    current_index = int(scraperwiki.sqlite.get_var('last_index'))
except:
    current_index = 0

while current_index <= len(all_domains):
    scraperwiki.sqlite.save_var('last_index', current_index)
    domain = all_domains[current_index]['domain']


    # Add domain to the data dictionary that will be saved to the database
    data = {'domain' : domain}
    
    try:
        # Loop through possible rights getting a count of each
        for as_rights in possible_as_rights:
        
            # Create the URL for the Google Result Page
            url = 'http://www.google.com/search?as_sitesearch=' + domain + '&as_rights=(' + as_rights + ')'
            #url = 'http://www.effectiveeducation.org'
            
            # Use a proxy to scrape Google Results
            #proxy = 'http://' + all_proxies[random.randrange(0, len(all_proxies))]['ipaddress'] + ':80'
            proxy = 'http://1.2.3.4:80'
    
            # Print Debugging Information
            print 'Proxy: ' + proxy
            print 'Domain: ' + domain
    
            proxy_handler = urllib2.ProxyHandler({'http':  proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            html_file = opener.open(url)
            html = html_file.read()
            html_file.close
        
            # Find the resultStats for the particular as_rights and put it in the data dictionary
            root = lxml.html.fromstring(html)
            result_stats = root.cssselect("div[id=resultStats]")
            for stat in result_stats:
                data[as_rights] = stat.text_content().replace('About ','').replace(' results','').replace(' result','').replace(",",'')
                #print data
    except Exception as inst:
        print str(inst)
        current_index = current_index - 1
        time.sleep(random.randrange(1,60))

    # Write to the database
    scraperwiki.sqlite.save(unique_keys=['domain'], data=data)

    current_index = current_index + 1
# This scraper, which needs to be named, goes through a list of domains and using google determines how many pages have open content
# Note, this scrapes google through a proxy for research purposes, as allowed and protected by fair use and Google not being evil (in theory)


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse
import urllib2
import random
import time


# Find Proxies at http://hidemyass.com/proxy-list/search-225446
possible_as_rights = ['cc_publicdomain', 'cc_attribute', 'cc_sharealike', 'cc_noncommercial', 'cc_nonderived']

# Load Proxy Server List
scraperwiki.sqlite.attach("hide_my_ass_proxy_list_ip_14", "proxylist")
all_proxies = scraperwiki.sqlite.select("ipaddress from proxylist.hidemyass where port=80")
print all_proxies


# Load Domains from Webometrics Ranking Web of Universities Scraper
scraperwiki.sqlite.attach("webometrics_ranking_web_of_universities", "webometrics")
all_domains = scraperwiki.sqlite.select("domain from webometrics.swdata")

try:
    current_index = int(scraperwiki.sqlite.get_var('last_index'))
except:
    current_index = 0

while current_index <= len(all_domains):
    scraperwiki.sqlite.save_var('last_index', current_index)
    domain = all_domains[current_index]['domain']


    # Add domain to the data dictionary that will be saved to the database
    data = {'domain' : domain}
    
    try:
        # Loop through possible rights getting a count of each
        for as_rights in possible_as_rights:
        
            # Create the URL for the Google Result Page
            url = 'http://www.google.com/search?as_sitesearch=' + domain + '&as_rights=(' + as_rights + ')'
            #url = 'http://www.effectiveeducation.org'
            
            # Use a proxy to scrape Google Results
            #proxy = 'http://' + all_proxies[random.randrange(0, len(all_proxies))]['ipaddress'] + ':80'
            proxy = 'http://1.2.3.4:80'
    
            # Print Debugging Information
            print 'Proxy: ' + proxy
            print 'Domain: ' + domain
    
            proxy_handler = urllib2.ProxyHandler({'http':  proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            html_file = opener.open(url)
            html = html_file.read()
            html_file.close
        
            # Find the resultStats for the particular as_rights and put it in the data dictionary
            root = lxml.html.fromstring(html)
            result_stats = root.cssselect("div[id=resultStats]")
            for stat in result_stats:
                data[as_rights] = stat.text_content().replace('About ','').replace(' results','').replace(' result','').replace(",",'')
                #print data
    except Exception as inst:
        print str(inst)
        current_index = current_index - 1
        time.sleep(random.randrange(1,60))

    # Write to the database
    scraperwiki.sqlite.save(unique_keys=['domain'], data=data)

    current_index = current_index + 1
# This scraper, which needs to be named, goes through a list of domains and using google determines how many pages have open content
# Note, this scrapes google through a proxy for research purposes, as allowed and protected by fair use and Google not being evil (in theory)


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse
import urllib2
import random
import time


# Find Proxies at http://hidemyass.com/proxy-list/search-225446
possible_as_rights = ['cc_publicdomain', 'cc_attribute', 'cc_sharealike', 'cc_noncommercial', 'cc_nonderived']

# Load Proxy Server List
scraperwiki.sqlite.attach("hide_my_ass_proxy_list_ip_14", "proxylist")
all_proxies = scraperwiki.sqlite.select("ipaddress from proxylist.hidemyass where port=80")
print all_proxies


# Load Domains from Webometrics Ranking Web of Universities Scraper
scraperwiki.sqlite.attach("webometrics_ranking_web_of_universities", "webometrics")
all_domains = scraperwiki.sqlite.select("domain from webometrics.swdata")

try:
    current_index = int(scraperwiki.sqlite.get_var('last_index'))
except:
    current_index = 0

while current_index <= len(all_domains):
    scraperwiki.sqlite.save_var('last_index', current_index)
    domain = all_domains[current_index]['domain']


    # Add domain to the data dictionary that will be saved to the database
    data = {'domain' : domain}
    
    try:
        # Loop through possible rights getting a count of each
        for as_rights in possible_as_rights:
        
            # Create the URL for the Google Result Page
            url = 'http://www.google.com/search?as_sitesearch=' + domain + '&as_rights=(' + as_rights + ')'
            #url = 'http://www.effectiveeducation.org'
            
            # Use a proxy to scrape Google Results
            #proxy = 'http://' + all_proxies[random.randrange(0, len(all_proxies))]['ipaddress'] + ':80'
            proxy = 'http://1.2.3.4:80'
    
            # Print Debugging Information
            print 'Proxy: ' + proxy
            print 'Domain: ' + domain
    
            proxy_handler = urllib2.ProxyHandler({'http':  proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            html_file = opener.open(url)
            html = html_file.read()
            html_file.close
        
            # Find the resultStats for the particular as_rights and put it in the data dictionary
            root = lxml.html.fromstring(html)
            result_stats = root.cssselect("div[id=resultStats]")
            for stat in result_stats:
                data[as_rights] = stat.text_content().replace('About ','').replace(' results','').replace(' result','').replace(",",'')
                #print data
    except Exception as inst:
        print str(inst)
        current_index = current_index - 1
        time.sleep(random.randrange(1,60))

    # Write to the database
    scraperwiki.sqlite.save(unique_keys=['domain'], data=data)

    current_index = current_index + 1
# This scraper, which needs to be named, goes through a list of domains and using google determines how many pages have open content
# Note, this scrapes google through a proxy for research purposes, as allowed and protected by fair use and Google not being evil (in theory)


# Import Libraries
import scraperwiki
import lxml.html
from lxml.etree import tostring
from urlparse import urlparse
import urllib2
import random
import time


# Find Proxies at http://hidemyass.com/proxy-list/search-225446
possible_as_rights = ['cc_publicdomain', 'cc_attribute', 'cc_sharealike', 'cc_noncommercial', 'cc_nonderived']

# Load Proxy Server List
scraperwiki.sqlite.attach("hide_my_ass_proxy_list_ip_14", "proxylist")
all_proxies = scraperwiki.sqlite.select("ipaddress from proxylist.hidemyass where port=80")
print all_proxies


# Load Domains from Webometrics Ranking Web of Universities Scraper
scraperwiki.sqlite.attach("webometrics_ranking_web_of_universities", "webometrics")
all_domains = scraperwiki.sqlite.select("domain from webometrics.swdata")

try:
    current_index = int(scraperwiki.sqlite.get_var('last_index'))
except:
    current_index = 0

while current_index <= len(all_domains):
    scraperwiki.sqlite.save_var('last_index', current_index)
    domain = all_domains[current_index]['domain']


    # Add domain to the data dictionary that will be saved to the database
    data = {'domain' : domain}
    
    try:
        # Loop through possible rights getting a count of each
        for as_rights in possible_as_rights:
        
            # Create the URL for the Google Result Page
            url = 'http://www.google.com/search?as_sitesearch=' + domain + '&as_rights=(' + as_rights + ')'
            #url = 'http://www.effectiveeducation.org'
            
            # Use a proxy to scrape Google Results
            #proxy = 'http://' + all_proxies[random.randrange(0, len(all_proxies))]['ipaddress'] + ':80'
            proxy = 'http://1.2.3.4:80'
    
            # Print Debugging Information
            print 'Proxy: ' + proxy
            print 'Domain: ' + domain
    
            proxy_handler = urllib2.ProxyHandler({'http':  proxy})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            html_file = opener.open(url)
            html = html_file.read()
            html_file.close
        
            # Find the resultStats for the particular as_rights and put it in the data dictionary
            root = lxml.html.fromstring(html)
            result_stats = root.cssselect("div[id=resultStats]")
            for stat in result_stats:
                data[as_rights] = stat.text_content().replace('About ','').replace(' results','').replace(' result','').replace(",",'')
                #print data
    except Exception as inst:
        print str(inst)
        current_index = current_index - 1
        time.sleep(random.randrange(1,60))

    # Write to the database
    scraperwiki.sqlite.save(unique_keys=['domain'], data=data)

    current_index = current_index + 1
