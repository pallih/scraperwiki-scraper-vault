import scraperwiki           
import lxml.html
import urllib2
import urllib
import re
from lxml import etree

print "Starting"

header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=de45029e5e2fab4f6e5eef56515d6c1c; __utma=123692957.1658163614.1349740913.1349740913.1352756518.2; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }

omit_category = ["accessible"]
start_count = 0
category_cache = {}


def get_url(url):
    req = urllib2.Request(url, None, header)  
    response = urllib2.urlopen(req)
    root = lxml.html.fromstring(response.read())
    return root

def parse_field(element):
    field_string = etree.tostring(element, method="text", encoding="UTF-8")
    if ":" in field_string:
        field_string = field_string.split(":")[1]
    return field_string

def parse_list(root, category):
    """ Takes a listing page and indexes all the listings in it """
    for el in root.cssselect("body center table td.wbg div table td.pl table td.sp.np div.b a"): 
        page_url = "http://www.tours.com" + el.get("href");
        print "Tours.com Url: %s" % page_url  
        page = get_url(page_url)
        
        links = page.cssselect("body div.lbbg.pp div.p.s a")
        operator_url = links[-1].get("href")
        operator_email = links[-2].get("href").replace("mailto:", "") # we want valid emails
        operator     = parse_field(page.cssselect("body div.lbbg.pp div.p")[0]) 
        information  = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[0])
        origin       = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[1])
        destinations = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[2])
        languages    = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[3])
        #print "Operator Url: %s" % operator_url
        #print "Operator Email: %s" % operator_email
        #print "Operator: %s" % operator
        #print "information: %s" % information
        #print "destinations: %s" % destinations
        #print "origin: %s" % origin
        #print "languages: %s" % languages
        #print "category: %s" % category
        #print "---------------------------------"

        if category_cache.get(page_url, False):
            category_cache[page_url].append(category)
        else:
            category_cache[page_url] = [category]

        data = {
            'source_url': page_url,
            'url': operator_url,
            'email': operator_email,
            'operator': operator,
            'categories': ", ".join(category_cache[page_url]),
            'destinations': destinations,
            'origin': origin,
            'languages': languages,
            'information': information,
        }
        scraperwiki.sqlite.save(unique_keys=['source_url', 'url', 'email'], data=data, table_name="tours_com")


def parse_category(category):
    if category in omit_category:
        print "Omitting category %s" % category

    category_url = category.replace("_", " ")
    base_url = "http://www.tours.com/tours_vacations.htm?kwd=%s&pg=%s" 
    # not iterate over the pages 
    count = 0

    #if start_count:
    #    count = start_count
    #    start_count = 0

    while True:
        url = base_url % (category_url, count) # targets each page in the list
        print "On page %s" % url
        root = get_url(url)
    
        # check if there are items, if not stop since you exceeded the total pages
        if not root.cssselect("body center table td.wbg div table td.pl table td.sp.np div.b a"):
            print "Reached end at page %s" % count
            break
    
        # this will parse the first listing page
        parse_list(root, category)
        print "Finished page %s" % count
        count = count + 1


start_url = "http://www.tours.com/by_type.htm"
page = get_url(start_url)
links = page.cssselect("body td.wbg td.pl table a")

block = True
for link in links:
    href = link.get("href")
    category = re.search(r"(\w+).htm", href).group(1)
    if category == "research" or block == False:
        parse_category(category)
        block = False
    else:
        print "Skipping %s" % category
import scraperwiki           
import lxml.html
import urllib2
import urllib
import re
from lxml import etree

print "Starting"

header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=de45029e5e2fab4f6e5eef56515d6c1c; __utma=123692957.1658163614.1349740913.1349740913.1352756518.2; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }

omit_category = ["accessible"]
start_count = 0
category_cache = {}


def get_url(url):
    req = urllib2.Request(url, None, header)  
    response = urllib2.urlopen(req)
    root = lxml.html.fromstring(response.read())
    return root

def parse_field(element):
    field_string = etree.tostring(element, method="text", encoding="UTF-8")
    if ":" in field_string:
        field_string = field_string.split(":")[1]
    return field_string

def parse_list(root, category):
    """ Takes a listing page and indexes all the listings in it """
    for el in root.cssselect("body center table td.wbg div table td.pl table td.sp.np div.b a"): 
        page_url = "http://www.tours.com" + el.get("href");
        print "Tours.com Url: %s" % page_url  
        page = get_url(page_url)
        
        links = page.cssselect("body div.lbbg.pp div.p.s a")
        operator_url = links[-1].get("href")
        operator_email = links[-2].get("href").replace("mailto:", "") # we want valid emails
        operator     = parse_field(page.cssselect("body div.lbbg.pp div.p")[0]) 
        information  = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[0])
        origin       = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[1])
        destinations = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[2])
        languages    = parse_field(page.cssselect("body div.lbbg.pp div.p.s")[3])
        #print "Operator Url: %s" % operator_url
        #print "Operator Email: %s" % operator_email
        #print "Operator: %s" % operator
        #print "information: %s" % information
        #print "destinations: %s" % destinations
        #print "origin: %s" % origin
        #print "languages: %s" % languages
        #print "category: %s" % category
        #print "---------------------------------"

        if category_cache.get(page_url, False):
            category_cache[page_url].append(category)
        else:
            category_cache[page_url] = [category]

        data = {
            'source_url': page_url,
            'url': operator_url,
            'email': operator_email,
            'operator': operator,
            'categories': ", ".join(category_cache[page_url]),
            'destinations': destinations,
            'origin': origin,
            'languages': languages,
            'information': information,
        }
        scraperwiki.sqlite.save(unique_keys=['source_url', 'url', 'email'], data=data, table_name="tours_com")


def parse_category(category):
    if category in omit_category:
        print "Omitting category %s" % category

    category_url = category.replace("_", " ")
    base_url = "http://www.tours.com/tours_vacations.htm?kwd=%s&pg=%s" 
    # not iterate over the pages 
    count = 0

    #if start_count:
    #    count = start_count
    #    start_count = 0

    while True:
        url = base_url % (category_url, count) # targets each page in the list
        print "On page %s" % url
        root = get_url(url)
    
        # check if there are items, if not stop since you exceeded the total pages
        if not root.cssselect("body center table td.wbg div table td.pl table td.sp.np div.b a"):
            print "Reached end at page %s" % count
            break
    
        # this will parse the first listing page
        parse_list(root, category)
        print "Finished page %s" % count
        count = count + 1


start_url = "http://www.tours.com/by_type.htm"
page = get_url(start_url)
links = page.cssselect("body td.wbg td.pl table a")

block = True
for link in links:
    href = link.get("href")
    category = re.search(r"(\w+).htm", href).group(1)
    if category == "research" or block == False:
        parse_category(category)
        block = False
    else:
        print "Skipping %s" % category
