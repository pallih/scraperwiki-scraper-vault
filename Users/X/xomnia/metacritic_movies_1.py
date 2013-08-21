#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import lxml.html
import scraperwiki
import dateutil.parser
import logging

baseurl = "http://www.metacritic.com/browse/dvds/release-date/new-releases/date?view=condensed"
page_ext = "&page=%s"
sources = ("dvd", "theater")
indices = [""] + ["/%s" % chr(n) for n in range(ord("a"), ord("z") + 1)]
unique_keys=("title", "release_date")

item_xpath = "//div[@class='module products_module list_product_summaries_module ']/div[@class='body']/div[@class='body_wrap']/ol/li"
next_page_xpath = "//div[@class='page_nav']/div[@class='page_nav_wrap']/div[@class='page_flipper']/span[@class='flipper next']/a[@class='action']/span[@class='text']"
inst_xpaths = {
    "title": "h3[@class='product_title']/a",
    "release_date": "li[@class='stat release_date']/span[@class='data']",
    "rating": "li[@class='stat rating']/span[@class='data']",
    "score": "span[contains(@class, 'metascore')]",
    "user_score": "li[@class='stat product_avguserscore']/span[contains(@class,'textscore')]",
    "cast": "li[@class='stat cast']/span[@class='data']",
    "genres": "li[@class='stat genre']/span[@class='data']",
    "runtime": "li[@class='stat runtime']/span[@class='data']",
}
def inst_clean(value):
    if value == "tbd": return None
    return value

def clean_spacing(value):
    return ", ".join(re.split(",\s+", value))

inst_cleans = {
    "genres": clean_spacing,
    "cast": clean_spacing,
    "release_date": lambda x: x and dateutil.parser.parse(x).date(),
    "runtime": lambda x: x and int(x.split()[0]),
    "score": lambda x: x and int(x),
    "user_score": lambda x: x and float(x),
}

def parse_detail_page(html):
    data = []
    root = lxml.html.fromstring(html)
    for item in root.xpath(item_xpath):
        inst = {}
        for key, inst_xpath in inst_xpaths.iteritems():
            value = item.xpath("descendant::%s" % inst_xpath)
            value = value and inst_clean(value[0].text.strip()) or None
            if value and key in inst_cleans:
                func = inst_cleans[key]
                value = func(value)
            inst[key] = value # is None and -1 or value
        data.append(inst)

    scraperwiki.sqlite.save(unique_keys=unique_keys, data=data)

    return root.xpath(next_page_xpath)


for source in sources:
    for index in indices:
        scrapeurl = indexurl = baseurl % {"source": source, "index": index}
        page = 0
        while 1:
            html = scraperwiki.scrape(scrapeurl)
            if not html: break

            more_pages = parse_detail_page(html)

            if more_pages:
                page += 1
                scrapeurl = "%s%s" % (indexurl, page_ext % page)
                continue
            break

