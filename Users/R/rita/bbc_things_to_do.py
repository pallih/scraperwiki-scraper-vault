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
    name = strip_tags(root("#activityTitle").html())
    location = strip_tags(root(".location").html())
    organizer = strip_tags(root(".run-by").html())
    if organizer:
        organizer = organizer.replace("Run by:", "")
    description = strip_tags(root("#shortDescription").html())
    phone = strip_tags(root("#telephone p").html())
    if phone:
        phone = phone.replace("Telephone", "")
    email  = strip_tags(root("#email a").attr("href"))
    if email:
        email = email.replace("mailto:", "")
    website = strip_tags(root("#website a").attr("href"))
    cost = strip_tags(root("#cost p").html())
    data = {
        'name': name,
        'location': location,
        'organizer': organizer,
        'description': description,
        'website': website,
        'source_url': url,
        'email': email,
        'phone': phone,
        'cost': cost,
    }
    scraperwiki.sqlite.save(unique_keys=['source_url'], data=data, table_name="bbc_things_to_do")

pages = range(1, 605)
page_size = 9

def parse_listing_pages(start_url):
    # not iterate over the pages

    for page in pages:
        url = start_url % {"page": page, "offset": (page-1) * 9}
        print "On page %s" % url
        root = get_url(url)

        # check if there are items, if not stop since you exceeded the total pages
        for el in root(".activityDetails h3 a"):
            parse_list("http://www.bbc.co.uk%s" % pq(el).attr("href"))
    
    print "Finished"

start_url = "http://www.bbc.co.uk/thingstodo/activities?max=9&sort[0]=start&order[0]=asc&page=%(page)s&offset=%(offset)s&distance=30&sameDay=false&limit=9"
parse_listing_pages(start_url)



