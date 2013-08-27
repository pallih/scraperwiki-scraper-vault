# -*- coding: utf-8 -*-
# visits pages found on sitemap.xml, checks Facebook API for open graph interactions

import scraperwiki
import urllib2
from lxml import etree
import json
import time


def scrape(url):
# common scraping function
    retries = 3
    try:
        for i in range(retries):
            data = urllib2.urlopen(url).read()
            return data
    except urllib2.URLError:
        if i + 1 == retries:
            raise
    else:
        time.sleep(30)


def create_list(sitemap_url):
# create a list of target URLs using the sitemap.xml
    urls = []
    sitemap_raw = scrape(sitemap_url)
    sitemap_xml = etree.fromstring(sitemap_raw) #
    # find all the "location" data. The namespaces bit may require tweaking from time to time
    loc=sitemap_xml.xpath('//ns:loc',namespaces={'ns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
    for item in loc:
        urls.append(item.text)
    return urls


def query_graph_api(urls):
# query the Graph API, store data.
    for url in urls:
        print url #debug console
        data = {}
        graph_query = graph_query_root + "%22" + url + "%22"
        graph_query_url = graph_query.encode('utf-8')
        print graph_query_url # debug console
        query_data = scrape(graph_query_url)
        query_json = json.loads(query_data)
        for item in [u'normalized_url', u'share_count', u'like_count', u'comment_count', u'total_count']:
            data[item] = query_json[u'data'][0][item]
        scraperwiki.sqlite.save(unique_keys=[u'normalized_url'], data=data)
        time.sleep(2)




###################
###            ####
### START HERE ####
###            ####
###################


map_url =  "http://nakedsecurity.sophos.com/sitemap.xml"

graph_query_root = "https://graph.facebook.com/fql?q=SELECT%20normalized_url,share_count,like_count,comment_count,total_count%20FROM%20link_stat%20WHERE%20url="

urls = create_list(map_url)

query_graph_api(urls)

# -*- coding: utf-8 -*-
# visits pages found on sitemap.xml, checks Facebook API for open graph interactions

import scraperwiki
import urllib2
from lxml import etree
import json
import time


def scrape(url):
# common scraping function
    retries = 3
    try:
        for i in range(retries):
            data = urllib2.urlopen(url).read()
            return data
    except urllib2.URLError:
        if i + 1 == retries:
            raise
    else:
        time.sleep(30)


def create_list(sitemap_url):
# create a list of target URLs using the sitemap.xml
    urls = []
    sitemap_raw = scrape(sitemap_url)
    sitemap_xml = etree.fromstring(sitemap_raw) #
    # find all the "location" data. The namespaces bit may require tweaking from time to time
    loc=sitemap_xml.xpath('//ns:loc',namespaces={'ns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
    for item in loc:
        urls.append(item.text)
    return urls


def query_graph_api(urls):
# query the Graph API, store data.
    for url in urls:
        print url #debug console
        data = {}
        graph_query = graph_query_root + "%22" + url + "%22"
        graph_query_url = graph_query.encode('utf-8')
        print graph_query_url # debug console
        query_data = scrape(graph_query_url)
        query_json = json.loads(query_data)
        for item in [u'normalized_url', u'share_count', u'like_count', u'comment_count', u'total_count']:
            data[item] = query_json[u'data'][0][item]
        scraperwiki.sqlite.save(unique_keys=[u'normalized_url'], data=data)
        time.sleep(2)




###################
###            ####
### START HERE ####
###            ####
###################


map_url =  "http://nakedsecurity.sophos.com/sitemap.xml"

graph_query_root = "https://graph.facebook.com/fql?q=SELECT%20normalized_url,share_count,like_count,comment_count,total_count%20FROM%20link_stat%20WHERE%20url="

urls = create_list(map_url)

query_graph_api(urls)

# -*- coding: utf-8 -*-
# visits pages found on sitemap.xml, checks Facebook API for open graph interactions

import scraperwiki
import urllib2
from lxml import etree
import json
import time


def scrape(url):
# common scraping function
    retries = 3
    try:
        for i in range(retries):
            data = urllib2.urlopen(url).read()
            return data
    except urllib2.URLError:
        if i + 1 == retries:
            raise
    else:
        time.sleep(30)


def create_list(sitemap_url):
# create a list of target URLs using the sitemap.xml
    urls = []
    sitemap_raw = scrape(sitemap_url)
    sitemap_xml = etree.fromstring(sitemap_raw) #
    # find all the "location" data. The namespaces bit may require tweaking from time to time
    loc=sitemap_xml.xpath('//ns:loc',namespaces={'ns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
    for item in loc:
        urls.append(item.text)
    return urls


def query_graph_api(urls):
# query the Graph API, store data.
    for url in urls:
        print url #debug console
        data = {}
        graph_query = graph_query_root + "%22" + url + "%22"
        graph_query_url = graph_query.encode('utf-8')
        print graph_query_url # debug console
        query_data = scrape(graph_query_url)
        query_json = json.loads(query_data)
        for item in [u'normalized_url', u'share_count', u'like_count', u'comment_count', u'total_count']:
            data[item] = query_json[u'data'][0][item]
        scraperwiki.sqlite.save(unique_keys=[u'normalized_url'], data=data)
        time.sleep(2)




###################
###            ####
### START HERE ####
###            ####
###################


map_url =  "http://nakedsecurity.sophos.com/sitemap.xml"

graph_query_root = "https://graph.facebook.com/fql?q=SELECT%20normalized_url,share_count,like_count,comment_count,total_count%20FROM%20link_stat%20WHERE%20url="

urls = create_list(map_url)

query_graph_api(urls)

