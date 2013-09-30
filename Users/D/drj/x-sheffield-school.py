# David Jones, Climate Code Foundation

import json
import re
import urllib

import lxml.etree

import scraperwiki

# Just for the screenshot
scraperwiki.scrape("http://www.sheffield.gov.uk/education/our-schools")

queryu = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=sheffield-school-url&query=select%20*%20from%20%60swdata%60%20where%20type%20%3D%20'secondary'%20limit%2010"

def kml(tag):
    """Return the string for a KML tag, including its namespace."""
    return "{http://earth.google.com/kml/2.2}" + tag


def scrape1kml(u):
    """*u* is the URL for a single KML file.  scrape it."""
    
    # hat-tip to https://scraperwiki.com/scrapers/test_83/
    tree = lxml.etree.parse(urllib.urlopen(u))
    # doc = tree.getroot()[0]
    # Not quite xpath, but it's fun!
    for placemark in tree.findall("//" + kml('Placemark')):
        name = placemark.find(kml('name')).text
        coord = placemark.find(".//"+kml('coordinates')).text
        lon,lat = coord.split(',')[:2]
        # Note: *description* is itself some parsable HTML
        description = placemark.find(kml('description')).text
        html = lxml.etree.HTML(description)
        print lxml.etree.tostring(html)

        # Extract the URLs that have "urn=" in them, in order to get the Unique Reference Number.
        # Yes, I've been reading the XPath spec:
        # http://www.w3.org/TR/xpath/#section-Expressions
        urnattr, = html.xpath("//a/@href[contains(., 'urn=')]")
        urn = re.search(r'\burn=(\d+)', urnattr).group(1)
        data = dict(name=name, urn=urn, Latitude=lat, Longitude=lon)

        # Do semi-regular optional keys.
        for key,path in [
            ('edubaseurl', "//a/@href[contains(., 'edubase')]"),
            ('ofstedurl', "//a/@href[contains(., 'ofsted')]"),
            ('mailurl', "//a/@href[starts-with(., 'mailto')]"),
            ('website', "//div[starts-with(string(), 'Website')]/a/@href"),
            ('imgurl', "//img/@src"),
          ]:
            strings = html.xpath(path)
            if strings:
                # The above xpath queries should generate 0 or 1 nodes (strings, actually)
                # given the typical input data.
                data[key] = strings[0]   
        # A DIV starting "Telephone".  Doesn't work for all of them, *sigh*.
        telephone = html.xpath("string(//div[starts-with(string(), 'Telephone')])")
        # Weirdly, one school has a \xa0 character in the telephone number.
        telephone = telephone.replace(u'\xa0', u' ')
        print telephone
        m = re.search(r'(?=\d)[\d -]+', telephone)
        if m:
            data['telephone'] = m.group()
        
        # print lxml.etree.tostring(urnnode)
        scraperwiki.sqlite.save(['urn'], data)
    

kmls = json.load(urllib.urlopen(queryu))
for d in kmls:
    url = d['url']
    scrape1kml(url)# David Jones, Climate Code Foundation

import json
import re
import urllib

import lxml.etree

import scraperwiki

# Just for the screenshot
scraperwiki.scrape("http://www.sheffield.gov.uk/education/our-schools")

queryu = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=sheffield-school-url&query=select%20*%20from%20%60swdata%60%20where%20type%20%3D%20'secondary'%20limit%2010"

def kml(tag):
    """Return the string for a KML tag, including its namespace."""
    return "{http://earth.google.com/kml/2.2}" + tag


def scrape1kml(u):
    """*u* is the URL for a single KML file.  scrape it."""
    
    # hat-tip to https://scraperwiki.com/scrapers/test_83/
    tree = lxml.etree.parse(urllib.urlopen(u))
    # doc = tree.getroot()[0]
    # Not quite xpath, but it's fun!
    for placemark in tree.findall("//" + kml('Placemark')):
        name = placemark.find(kml('name')).text
        coord = placemark.find(".//"+kml('coordinates')).text
        lon,lat = coord.split(',')[:2]
        # Note: *description* is itself some parsable HTML
        description = placemark.find(kml('description')).text
        html = lxml.etree.HTML(description)
        print lxml.etree.tostring(html)

        # Extract the URLs that have "urn=" in them, in order to get the Unique Reference Number.
        # Yes, I've been reading the XPath spec:
        # http://www.w3.org/TR/xpath/#section-Expressions
        urnattr, = html.xpath("//a/@href[contains(., 'urn=')]")
        urn = re.search(r'\burn=(\d+)', urnattr).group(1)
        data = dict(name=name, urn=urn, Latitude=lat, Longitude=lon)

        # Do semi-regular optional keys.
        for key,path in [
            ('edubaseurl', "//a/@href[contains(., 'edubase')]"),
            ('ofstedurl', "//a/@href[contains(., 'ofsted')]"),
            ('mailurl', "//a/@href[starts-with(., 'mailto')]"),
            ('website', "//div[starts-with(string(), 'Website')]/a/@href"),
            ('imgurl', "//img/@src"),
          ]:
            strings = html.xpath(path)
            if strings:
                # The above xpath queries should generate 0 or 1 nodes (strings, actually)
                # given the typical input data.
                data[key] = strings[0]   
        # A DIV starting "Telephone".  Doesn't work for all of them, *sigh*.
        telephone = html.xpath("string(//div[starts-with(string(), 'Telephone')])")
        # Weirdly, one school has a \xa0 character in the telephone number.
        telephone = telephone.replace(u'\xa0', u' ')
        print telephone
        m = re.search(r'(?=\d)[\d -]+', telephone)
        if m:
            data['telephone'] = m.group()
        
        # print lxml.etree.tostring(urnnode)
        scraperwiki.sqlite.save(['urn'], data)
    

kmls = json.load(urllib.urlopen(queryu))
for d in kmls:
    url = d['url']
    scrape1kml(url)