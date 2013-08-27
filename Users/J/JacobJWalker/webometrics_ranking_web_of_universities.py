# Webometrics Ranking Web of Universities contains one of the most comprehensive list of world universities
# This scraper downloads their list and rankings from http://www.webometrics.info/en/world?page=x for research purposes

# Import Libraries
import scraperwiki
import lxml.html
import time
from urlparse import urlparse
import urllib


# Defines the get_domain function to use later on
def get_domain(url, tlds):
    url_elements = urlparse(url)[1].split('.')
    # url_elements = ["abcde","co","uk"]

    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds:
        if (exception_candidate in tlds):
            return ".".join(url_elements[i:])
        if (candidate in tlds or wildcard_candidate in tlds):
            return ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"

    return urlparse(url)[1]


# Loads the TLD List to be used later in the program
tld_file = scraperwiki.scrape('http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1')
tlds = tld_file.splitlines()
for index in range(len(tlds)):
    tlds[index] = tlds[index].strip()
    if tlds[index][0:2] == '//':
        tlds[index] = ''
tlds = filter(None, tlds)


# Crawl through World Rankings Getting and Storing University Data

base_url = "http://www.webometrics.info/en/world?page="
try:
    current_page = int(scraperwiki.sqlite.get_var('last_page'))
except:
    current_page = 1
end_page = 120
if current_page >= end_page:
    current_page = 1
crawl_delay = 10 # This is the last known value from the robots.txt file

while current_page <= end_page:
    scraperwiki.sqlite.save_var('last_page', current_page)
    url = base_url + str(current_page)
    try:
        html = scraperwiki.scrape(url)
    except Exception as inst:
        # If there is an error, display it, and then wait a minute and try the loop again
        print "Error on Page: " + str(current_page) + " " + str(inst)
        time.sleep(60)
        continue

    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds):

            #Write Data
            data = { 
                'world_ranking' : int(tds[0].text_content()), 
                'university_name' : tds[1].text_content().replace("(1)","").replace("(2)","").replace("(3)","").replace("(4)",""),
                'url' : str(tds[1].xpath('a/@href'))[2:-3],
                'domain' : get_domain(str(tds[1].xpath('a/@href'))[2:-3],tlds),
                'country_code' : str(tds[3].xpath('center/img/@src'))[-8:-6],
                'presence_rank' : int(tds[4].text_content()),
                'impact_rank' : int(tds[5].text_content()),
                'openness_rank' : int(tds[6].text_content()),
                'excellence_rank' : int(tds[7].text_content()),
            }
            scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    current_page = current_page + 1
    time.sleep(crawl_delay)

# Webometrics Ranking Web of Universities contains one of the most comprehensive list of world universities
# This scraper downloads their list and rankings from http://www.webometrics.info/en/world?page=x for research purposes

# Import Libraries
import scraperwiki
import lxml.html
import time
from urlparse import urlparse
import urllib


# Defines the get_domain function to use later on
def get_domain(url, tlds):
    url_elements = urlparse(url)[1].split('.')
    # url_elements = ["abcde","co","uk"]

    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds:
        if (exception_candidate in tlds):
            return ".".join(url_elements[i:])
        if (candidate in tlds or wildcard_candidate in tlds):
            return ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"

    return urlparse(url)[1]


# Loads the TLD List to be used later in the program
tld_file = scraperwiki.scrape('http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1')
tlds = tld_file.splitlines()
for index in range(len(tlds)):
    tlds[index] = tlds[index].strip()
    if tlds[index][0:2] == '//':
        tlds[index] = ''
tlds = filter(None, tlds)


# Crawl through World Rankings Getting and Storing University Data

base_url = "http://www.webometrics.info/en/world?page="
try:
    current_page = int(scraperwiki.sqlite.get_var('last_page'))
except:
    current_page = 1
end_page = 120
if current_page >= end_page:
    current_page = 1
crawl_delay = 10 # This is the last known value from the robots.txt file

while current_page <= end_page:
    scraperwiki.sqlite.save_var('last_page', current_page)
    url = base_url + str(current_page)
    try:
        html = scraperwiki.scrape(url)
    except Exception as inst:
        # If there is an error, display it, and then wait a minute and try the loop again
        print "Error on Page: " + str(current_page) + " " + str(inst)
        time.sleep(60)
        continue

    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds):

            #Write Data
            data = { 
                'world_ranking' : int(tds[0].text_content()), 
                'university_name' : tds[1].text_content().replace("(1)","").replace("(2)","").replace("(3)","").replace("(4)",""),
                'url' : str(tds[1].xpath('a/@href'))[2:-3],
                'domain' : get_domain(str(tds[1].xpath('a/@href'))[2:-3],tlds),
                'country_code' : str(tds[3].xpath('center/img/@src'))[-8:-6],
                'presence_rank' : int(tds[4].text_content()),
                'impact_rank' : int(tds[5].text_content()),
                'openness_rank' : int(tds[6].text_content()),
                'excellence_rank' : int(tds[7].text_content()),
            }
            scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    current_page = current_page + 1
    time.sleep(crawl_delay)

# Webometrics Ranking Web of Universities contains one of the most comprehensive list of world universities
# This scraper downloads their list and rankings from http://www.webometrics.info/en/world?page=x for research purposes

# Import Libraries
import scraperwiki
import lxml.html
import time
from urlparse import urlparse
import urllib


# Defines the get_domain function to use later on
def get_domain(url, tlds):
    url_elements = urlparse(url)[1].split('.')
    # url_elements = ["abcde","co","uk"]

    for i in range(-len(url_elements), 0):
        last_i_elements = url_elements[i:]
        #    i=-3: ["abcde","co","uk"]
        #    i=-2: ["co","uk"]
        #    i=-1: ["uk"] etc

        candidate = ".".join(last_i_elements) # abcde.co.uk, co.uk, uk
        wildcard_candidate = ".".join(["*"] + last_i_elements[1:]) # *.co.uk, *.uk, *
        exception_candidate = "!" + candidate

        # match tlds:
        if (exception_candidate in tlds):
            return ".".join(url_elements[i:])
        if (candidate in tlds or wildcard_candidate in tlds):
            return ".".join(url_elements[i-1:])
            # returns "abcde.co.uk"

    return urlparse(url)[1]


# Loads the TLD List to be used later in the program
tld_file = scraperwiki.scrape('http://mxr.mozilla.org/mozilla/source/netwerk/dns/src/effective_tld_names.dat?raw=1')
tlds = tld_file.splitlines()
for index in range(len(tlds)):
    tlds[index] = tlds[index].strip()
    if tlds[index][0:2] == '//':
        tlds[index] = ''
tlds = filter(None, tlds)


# Crawl through World Rankings Getting and Storing University Data

base_url = "http://www.webometrics.info/en/world?page="
try:
    current_page = int(scraperwiki.sqlite.get_var('last_page'))
except:
    current_page = 1
end_page = 120
if current_page >= end_page:
    current_page = 1
crawl_delay = 10 # This is the last known value from the robots.txt file

while current_page <= end_page:
    scraperwiki.sqlite.save_var('last_page', current_page)
    url = base_url + str(current_page)
    try:
        html = scraperwiki.scrape(url)
    except Exception as inst:
        # If there is an error, display it, and then wait a minute and try the loop again
        print "Error on Page: " + str(current_page) + " " + str(inst)
        time.sleep(60)
        continue

    root = lxml.html.fromstring(html)
    for tr in root.cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds):

            #Write Data
            data = { 
                'world_ranking' : int(tds[0].text_content()), 
                'university_name' : tds[1].text_content().replace("(1)","").replace("(2)","").replace("(3)","").replace("(4)",""),
                'url' : str(tds[1].xpath('a/@href'))[2:-3],
                'domain' : get_domain(str(tds[1].xpath('a/@href'))[2:-3],tlds),
                'country_code' : str(tds[3].xpath('center/img/@src'))[-8:-6],
                'presence_rank' : int(tds[4].text_content()),
                'impact_rank' : int(tds[5].text_content()),
                'openness_rank' : int(tds[6].text_content()),
                'excellence_rank' : int(tds[7].text_content()),
            }
            scraperwiki.sqlite.save(unique_keys=['url'], data=data)

    current_page = current_page + 1
    time.sleep(crawl_delay)

