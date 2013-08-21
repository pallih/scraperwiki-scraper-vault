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

def parse_list(root):
    """ Takes a listing page and indexes all the listings in it """
    for el in root(".listing a.property_title"):
        page_url = "http://www.tripadvisor.com" + el.get("href");
        print "Url: %s" % page_url
        page = get_url(page_url)

        name = strip_tags(page("#HEADING_GROUP h1").html())
        ranking = page(".sprite-ratings").attr("content")
        #activity = strip_tags(page(".row-fluid  *[itemprop=title]").html())
        address = strip_tags(page(".format_address").html())
        #url = strip_tags(page(".row-fluid .row-fluid *[itemprop=url] a").attr("href"))
        telephone = strip_tags(page(".sprite-greenPhone").next().html())
        email_raw = strip_tags(page(".sprite-greenEmail").next().attr("onclick"))
        email = email_regex.findall(email_raw)  
        if email:
            email = email[0]
        description = strip_tags(page(".listing_description").html()).strip()[:1200]
        
        print email
        data = {
            'name': name,
            'source_url': page_url,
            #'url': url,
            'ranking': ranking,
            'email': email,
            #'activity': activity,
            'address': address,
            'telephone': telephone,
            'description': description,
        }
        scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="tripadvisor_toronto")


def parse_listing_pages(start_url):
    # not iterate over the pages
    count = 0
    while True:
        url = start_url % (count) # targets each page in the list
        print "On page %s" % url
        root = get_url(url)

        # check if there are items, if not stop since you exceeded the total pages
        if not root(".listing"):
            print "Reached end at page %s" % count
            break

        # this will parse the first listing page
        parse_list(root)
        print "Finished page %s" % count
        count = count + 30

start_url = "http://www.tripadvisor.com/AttractionsAjax-g155019?cat=25&o=a%s&sortOrder=popularity"
parse_listing_pages(start_url)

