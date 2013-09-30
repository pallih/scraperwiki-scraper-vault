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
    data = urllib.urlencode({"submit": 1, "submit": "Ok"})
    req = urllib2.Request(url, data, header)
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
    name = strip_tags(pq(el).find(".Name a").html())
    adress = strip_tags(pq(el).find(".Adresse").html())
    telefon = strip_tags(pq(el).find(".Telefon").html()).replace("Tel:","")
    mobile = strip_tags(pq(el).find(".Mobil").html()).replace("Mobil:","")
    email = strip_tags(pq(el).find(".E-Mail a").html())
    website = strip_tags(pq(el).find(".Website a").html())
    profile = strip_tags(pq(el).find(".Profil").html()).replace("Profil:","")
    
    data = {
        'name': name,
        'adress': adress,
        'tel': telefon,
        'mobile': mobile,
        'website': website,
        'email': email,
        'profile': profile,
    }
    scraperwiki.sqlite.save(unique_keys=['name', 'email'], data=data, table_name="findaguide.at")

def parse_listing_pages(start_url):
    root = get_url(start_url)

    # check if there are items, if not stop since you exceeded the total pages
    for el in root(".data"):
        parse_list(el)
    
    print "Finished"

start_url = "http://www.findaguide.at/"
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
    data = urllib.urlencode({"submit": 1, "submit": "Ok"})
    req = urllib2.Request(url, data, header)
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
    name = strip_tags(pq(el).find(".Name a").html())
    adress = strip_tags(pq(el).find(".Adresse").html())
    telefon = strip_tags(pq(el).find(".Telefon").html()).replace("Tel:","")
    mobile = strip_tags(pq(el).find(".Mobil").html()).replace("Mobil:","")
    email = strip_tags(pq(el).find(".E-Mail a").html())
    website = strip_tags(pq(el).find(".Website a").html())
    profile = strip_tags(pq(el).find(".Profil").html()).replace("Profil:","")
    
    data = {
        'name': name,
        'adress': adress,
        'tel': telefon,
        'mobile': mobile,
        'website': website,
        'email': email,
        'profile': profile,
    }
    scraperwiki.sqlite.save(unique_keys=['name', 'email'], data=data, table_name="findaguide.at")

def parse_listing_pages(start_url):
    root = get_url(start_url)

    # check if there are items, if not stop since you exceeded the total pages
    for el in root(".data"):
        parse_list(el)
    
    print "Finished"

start_url = "http://www.findaguide.at/"
parse_listing_pages(start_url)



