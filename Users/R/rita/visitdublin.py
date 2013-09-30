import scraperwiki
import lxml.html
import urllib2
import urllib
import re
from lxml import etree
from pyquery import PyQuery as pq

print "Starting"

header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=de45029e5e2fab4f6e5eef56515d6c1c; __utma=123692957.1658163614.1349740913.1349740913.1352756518.2; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }
email_regex = re.compile(r'([\w]+@+[\w]+\.+[\w]+)')
phone_regex = re.compile(r'Telephone : ([0-9\w\+\s]+)')

def get_url(url):
    req = urllib2.Request(url, None, header)
    response = urllib2.urlopen(req)
    root = lxml.html.fromstring(response.read())
    return root

def get_page(url):
    req = urllib2.Request(url, None, header)
    response = urllib2.urlopen(req)
    root = pq(response.read().decode('utf-8'))
    return root

def parse_field(element):
    field_string = element.html()
    if ":" in field_string:
        field_string = field_string.split(":")[1]
    return field_string

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    if value:
        return re.sub(r'<[^>]*?>', '', value)
    return ""

def parse_list(page_url):
    """ Takes a listing page and indexes all the listings in it """
    print "Parsing: %s" % page_url

    remainder = page_url.replace("http://www.visitdublin.com/asset/see_and_do/", "")
    remainder_cats = remainder.split("/")
    category = remainder_cats[0]
    if category in ["famous_dubliners", "visitor_attractions", "casinos", "study_in_dublin", "theatres_and_venues"]:
        return

    page = get_page(page_url)
    
    name = strip_tags(page(".detail-add strong").html())
    if not name:
        return

    telephone = phone_regex.findall(page(".detail-add").html())
    if telephone:
        telephone = telephone[0]

    email_raw = page(".detail-add").html()
    email = email_regex.findall(email_raw)  
    if email:
        email = email[0]
    description = strip_tags(page("#divDescription").html()).strip()[:1200]
    
    if not (email or telephone):
        return 

    data = {
        'category': category,
        'name': name,
        'source_url': page_url,
        'email': email,
        'telephone': telephone,
        'description': description,
    }
    print email, telephone, page_url
    scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="visit_dublin")


def parse_sitemap(start_url):
    print "On page %s" % start_url
    root = get_url(start_url)

    # check if there are items, if not stop since you exceeded the total pages
    for item in root.cssselect("urlset url loc"):
        if "asset/see_and_do" in item.text.lower():
            parse_list(item.text.lower())

    print "Finished"

start_url = "http://www.visitdublin.com/sitemap.xml"
parse_sitemap(start_url)

import scraperwiki
import lxml.html
import urllib2
import urllib
import re
from lxml import etree
from pyquery import PyQuery as pq

print "Starting"

header = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.47 Safari/536.11',
           'Cookie': 'PHPSESSID=de45029e5e2fab4f6e5eef56515d6c1c; __utma=123692957.1658163614.1349740913.1349740913.1352756518.2; __utmb=204497347.1.10.1342787814; __utmc=204497347; __utmz=204497347.1341998344.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)' }
email_regex = re.compile(r'([\w]+@+[\w]+\.+[\w]+)')
phone_regex = re.compile(r'Telephone : ([0-9\w\+\s]+)')

def get_url(url):
    req = urllib2.Request(url, None, header)
    response = urllib2.urlopen(req)
    root = lxml.html.fromstring(response.read())
    return root

def get_page(url):
    req = urllib2.Request(url, None, header)
    response = urllib2.urlopen(req)
    root = pq(response.read().decode('utf-8'))
    return root

def parse_field(element):
    field_string = element.html()
    if ":" in field_string:
        field_string = field_string.split(":")[1]
    return field_string

def strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    if value:
        return re.sub(r'<[^>]*?>', '', value)
    return ""

def parse_list(page_url):
    """ Takes a listing page and indexes all the listings in it """
    print "Parsing: %s" % page_url

    remainder = page_url.replace("http://www.visitdublin.com/asset/see_and_do/", "")
    remainder_cats = remainder.split("/")
    category = remainder_cats[0]
    if category in ["famous_dubliners", "visitor_attractions", "casinos", "study_in_dublin", "theatres_and_venues"]:
        return

    page = get_page(page_url)
    
    name = strip_tags(page(".detail-add strong").html())
    if not name:
        return

    telephone = phone_regex.findall(page(".detail-add").html())
    if telephone:
        telephone = telephone[0]

    email_raw = page(".detail-add").html()
    email = email_regex.findall(email_raw)  
    if email:
        email = email[0]
    description = strip_tags(page("#divDescription").html()).strip()[:1200]
    
    if not (email or telephone):
        return 

    data = {
        'category': category,
        'name': name,
        'source_url': page_url,
        'email': email,
        'telephone': telephone,
        'description': description,
    }
    print email, telephone, page_url
    scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="visit_dublin")


def parse_sitemap(start_url):
    print "On page %s" % start_url
    root = get_url(start_url)

    # check if there are items, if not stop since you exceeded the total pages
    for item in root.cssselect("urlset url loc"):
        if "asset/see_and_do" in item.text.lower():
            parse_list(item.text.lower())

    print "Finished"

start_url = "http://www.visitdublin.com/sitemap.xml"
parse_sitemap(start_url)

