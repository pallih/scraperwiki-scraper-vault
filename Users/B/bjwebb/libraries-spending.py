#!/usr/bin/env python
# Copyright (c) 2010 Ben Webb <bjwebb67@googlemail.com>
# Released under the GPL, as per ScraperWiki terms.

import BeautifulSoup
import scraperwiki
from scraperwiki import datastore

url = "http://openlylocal.com/dataset_topics/4800"
    
html = scraperwiki.scrape(url)
page = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
for datapoint in page.findAll(attrs={"class": "datapoint"}):
    data = {}
    a = datapoint.find(attrs={"class": "description"}).a
    data["olurl"] = a["href"]
    data["name"] = a.contents[0]
    data["cost"] = datapoint.find(attrs={"class": "value"}).contents[0]
    datastore.save(unique_keys=["olurl"], data=data)

