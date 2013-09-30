#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import lxml.html
import scraperwiki
import dateutil.parser
import logging
import urllib2

def scrape (url, params = None) :
    data = params and urllib.urlencode(params) or None

    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    fin = opener.open(url, data)
    text = fin.read()
    fin.close()   # get the mimetype here

    return text


baseurl = "http://www.rottentomatoes.com/%(source)s"
page_ext = "?page=%s"
sources = ("movie/in-theaters/",)
unique_keys=("title", "release_date")

set_xpath = "preceding-sibling::h4[@class='title_box']"
item_xpath = "//div[contains(@class,'movie_item')]"
next_page_xpath = "//div[@class='content_box ']/div[@class='content_body clearfix']/div[@class='right'][2]/a[@class='button pagination right']"
inst_xpaths = {
    "title": "descendant::div/h2/a",
    "release_date": "preceding-sibling::h4[@class='title_box'][1]",
    "rating": "descendant::div[@class='subtle']",
    "score": "descendant::span[@class='tMeterScore']",
    "cast": "descendant::div[@class='media_block_content']/div[2][text()]",
    "runtime": "descendant::div[@class='subtle']",
}
def inst_clean(value):
    return value

def clean_spacing(value):
    return ", ".join(re.split(",\s+", value))

def clean_rating(value):
    return value.split(" - ")[0].split(",")[0]

def clean_runtime(value):
    value = value.split(" - ")
    if len(value) == 1: return
    value = value[0].split(",")
    if len(value) >= 2: value = value[1]
    else: return
    mins = value.split("min.")[0]
    hr = mins.split("hr.")
    if len(hr) == 2:
        hr, mins = hr
        runtime = int(mins)
        runtime += int(hr) * 60
    else:
        runtime = int(mins)
    return runtime

inst_cleans = {
    "cast": clean_spacing,
    "release_date": lambda x: x and dateutil.parser.parse(x).date(),
    "runtime": clean_runtime,
    "rating": clean_rating,
    "score": lambda x: x and int(x.strip("%")),
}
def parse_detail_page(html):
    data = []
    root = lxml.html.fromstring(html)
    for item in root.xpath(item_xpath):
        inst = {}
        for key, inst_xpath in inst_xpaths.iteritems():
            value = item.xpath(inst_xpath)
            value = value and inst_clean(value[0].text.strip()) or None
            if value and key in inst_cleans:
                func = inst_cleans[key]
                value = func(value)
            inst[key] = value # is None and -1 or value
        data.append(inst)

    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)

    return root.xpath(next_page_xpath)


for source in sources:
    scrapeurl = indexurl = baseurl % {"source": source}
    page = 1
    while 1:
        html = scrape(scrapeurl)
        if not html: break

        more_pages = parse_detail_page(html)

        if more_pages:
            page += 1
            scrapeurl = "%s%s" % (indexurl, page_ext % page)
            continue
        break

#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import lxml.html
import scraperwiki
import dateutil.parser
import logging
import urllib2

def scrape (url, params = None) :
    data = params and urllib.urlencode(params) or None

    opener = urllib2.build_opener()
    opener.addheaders = [("User-agent", "Mozilla/5.0")]
    fin = opener.open(url, data)
    text = fin.read()
    fin.close()   # get the mimetype here

    return text


baseurl = "http://www.rottentomatoes.com/%(source)s"
page_ext = "?page=%s"
sources = ("movie/in-theaters/",)
unique_keys=("title", "release_date")

set_xpath = "preceding-sibling::h4[@class='title_box']"
item_xpath = "//div[contains(@class,'movie_item')]"
next_page_xpath = "//div[@class='content_box ']/div[@class='content_body clearfix']/div[@class='right'][2]/a[@class='button pagination right']"
inst_xpaths = {
    "title": "descendant::div/h2/a",
    "release_date": "preceding-sibling::h4[@class='title_box'][1]",
    "rating": "descendant::div[@class='subtle']",
    "score": "descendant::span[@class='tMeterScore']",
    "cast": "descendant::div[@class='media_block_content']/div[2][text()]",
    "runtime": "descendant::div[@class='subtle']",
}
def inst_clean(value):
    return value

def clean_spacing(value):
    return ", ".join(re.split(",\s+", value))

def clean_rating(value):
    return value.split(" - ")[0].split(",")[0]

def clean_runtime(value):
    value = value.split(" - ")
    if len(value) == 1: return
    value = value[0].split(",")
    if len(value) >= 2: value = value[1]
    else: return
    mins = value.split("min.")[0]
    hr = mins.split("hr.")
    if len(hr) == 2:
        hr, mins = hr
        runtime = int(mins)
        runtime += int(hr) * 60
    else:
        runtime = int(mins)
    return runtime

inst_cleans = {
    "cast": clean_spacing,
    "release_date": lambda x: x and dateutil.parser.parse(x).date(),
    "runtime": clean_runtime,
    "rating": clean_rating,
    "score": lambda x: x and int(x.strip("%")),
}
def parse_detail_page(html):
    data = []
    root = lxml.html.fromstring(html)
    for item in root.xpath(item_xpath):
        inst = {}
        for key, inst_xpath in inst_xpaths.iteritems():
            value = item.xpath(inst_xpath)
            value = value and inst_clean(value[0].text.strip()) or None
            if value and key in inst_cleans:
                func = inst_cleans[key]
                value = func(value)
            inst[key] = value # is None and -1 or value
        data.append(inst)

    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)

    return root.xpath(next_page_xpath)


for source in sources:
    scrapeurl = indexurl = baseurl % {"source": source}
    page = 1
    while 1:
        html = scrape(scrapeurl)
        if not html: break

        more_pages = parse_detail_page(html)

        if more_pages:
            page += 1
            scrapeurl = "%s%s" % (indexurl, page_ext % page)
            continue
        break

