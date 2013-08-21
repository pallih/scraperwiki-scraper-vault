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

def parse_list(el):
    """ Takes a listing page and indexes all the listings in it """
    el = pq(el)
    name = strip_tags(el.children(".title a").html())
    phone = strip_tags(el.children(".phone").html())
    email  = strip_tags(el.children(".email a").attr("href"))
    if email:
        email = email.replace("mailto:", "")
    source_url = el.children(".title a").attr("href")

    data = {
        'name': name,
        'source_url': 'http://www.guidestockholm.com%s' % source_url,
        'email': email,
        'phone': phone,
    }
    scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="guidestockholm")


def parse_listing_pages(start_url):
    # not iterate over the pages
    print "On page %s" % start_url
    root = get_url(start_url)

    # check if there are items, if not stop since you exceeded the total pages
    for el in root("#guides-list li"):
        parse_list(el)
    print "Finished"

start_url = "http://www.guidestockholm.com/Guides/(lang)/English"
parse_listing_pages(start_url)

