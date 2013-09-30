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
email_regex = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')

def get_url(url):
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

def parse_list(url):
    """ Takes a listing page and indexes all the listings in it """
    root = get_url(url)
    name = strip_tags(root("h1.fn.org").html())
    location = strip_tags(root(".place-box_info__list dd p:first").html())
    phone = root(".place-box_info__contact").html()
    if phone:
        phone = strip_tags(phone.split("<br")[0])
    website = strip_tags(root(".place-box_info__contact a:last").attr("href"))
    data = {
        'name': name,
        'location': location,
        'website': website,
        'source_url': url,
        'phone': phone,
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="qype_eating_drinking_berlin")

pages = range(878, 1294)

def parse_listing_pages(start_url):
    # not iterate over the pages

    for page in pages:
        url = start_url % page
        print "On page %s" % url
        root = get_url(url)

        # check if there are items, if not stop since you exceeded the total pages
        for el in root(".category-review__name a"):
            parse_list("http://www.qype.co.uk%s" % pq(el).attr("href"))
    
    print "Finished"

start_url = "http://www.qype.co.uk/de300-berlin/categories/883-eating-and-drinking-in-berlin?page=%s"
parse_listing_pages(start_url)



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
email_regex = re.compile(r'(\b[\w.]+@+[\w.]+.+[\w.]\b)')

def get_url(url):
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

def parse_list(url):
    """ Takes a listing page and indexes all the listings in it """
    root = get_url(url)
    name = strip_tags(root("h1.fn.org").html())
    location = strip_tags(root(".place-box_info__list dd p:first").html())
    phone = root(".place-box_info__contact").html()
    if phone:
        phone = strip_tags(phone.split("<br")[0])
    website = strip_tags(root(".place-box_info__contact a:last").attr("href"))
    data = {
        'name': name,
        'location': location,
        'website': website,
        'source_url': url,
        'phone': phone,
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="qype_eating_drinking_berlin")

pages = range(878, 1294)

def parse_listing_pages(start_url):
    # not iterate over the pages

    for page in pages:
        url = start_url % page
        print "On page %s" % url
        root = get_url(url)

        # check if there are items, if not stop since you exceeded the total pages
        for el in root(".category-review__name a"):
            parse_list("http://www.qype.co.uk%s" % pq(el).attr("href"))
    
    print "Finished"

start_url = "http://www.qype.co.uk/de300-berlin/categories/883-eating-and-drinking-in-berlin?page=%s"
parse_listing_pages(start_url)



