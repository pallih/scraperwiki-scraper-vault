#!/usr/bin/env python
# Copyright (c) 2010 Ben Webb <bjwebb67@googlemail.com>
# Released as free software under the MIT license.
# http://www.opensource.org/licenses/mit-license.php

import BeautifulSoup
import scraperwiki
from scraperwiki import datastore
import re

for url in ["http://nafis.co.uk/index.php?option=com_comprofiler&task=userslist&listid=2&Itemid=73",
            "http://nafis.co.uk/index.php?option=com_comprofiler&task=usersList&listid=2&Itemid=73&limitstart=154"]:
    html = scraperwiki.scrape(url)
    page1 = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
    for td in page1.findAll(attrs={"class": "cbUserListCol1"}):
        a = td.find("a")
        m = re.search("user=([0-9]+)", a["href"])
        id = m.group(1)
        html = scraperwiki.scrape(a["href"])
        page = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
        
        data = {}
        data["id"] = id
        for tr in page.findAll("tr"):
            try:
                td1 = tr.find(attrs={"class":"titleCell"})
                key = "".join(td1.findAll(text=True)).encode("utf-8")
                key = str(key).strip(":? ")
                td2 = tr.find(attrs={"class":"fieldCell"})
                value = "".join(td2.findAll(text=True)).encode("utf-8")
                data[key] = value
            except AttributeError: continue
        print data
        datastore.save(unique_keys=["id"], data=data)
        #!/usr/bin/env python
# Copyright (c) 2010 Ben Webb <bjwebb67@googlemail.com>
# Released as free software under the MIT license.
# http://www.opensource.org/licenses/mit-license.php

import BeautifulSoup
import scraperwiki
from scraperwiki import datastore
import re

for url in ["http://nafis.co.uk/index.php?option=com_comprofiler&task=userslist&listid=2&Itemid=73",
            "http://nafis.co.uk/index.php?option=com_comprofiler&task=usersList&listid=2&Itemid=73&limitstart=154"]:
    html = scraperwiki.scrape(url)
    page1 = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
    for td in page1.findAll(attrs={"class": "cbUserListCol1"}):
        a = td.find("a")
        m = re.search("user=([0-9]+)", a["href"])
        id = m.group(1)
        html = scraperwiki.scrape(a["href"])
        page = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
        
        data = {}
        data["id"] = id
        for tr in page.findAll("tr"):
            try:
                td1 = tr.find(attrs={"class":"titleCell"})
                key = "".join(td1.findAll(text=True)).encode("utf-8")
                key = str(key).strip(":? ")
                td2 = tr.find(attrs={"class":"fieldCell"})
                value = "".join(td2.findAll(text=True)).encode("utf-8")
                data[key] = value
            except AttributeError: continue
        print data
        datastore.save(unique_keys=["id"], data=data)
        