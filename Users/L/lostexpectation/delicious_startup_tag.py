# Blank Python
base_url = "http://www.delicious.com"
start_url = "http://www.delicious.com/tag/startup?"
extra_q = "&detail=3&setcount=100"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import scraperwiki
import BeautifulSoup
from datetime import datetime
import time

next_url = start_url
while next_url:
    print "getting %s%s" % (next_url,extra_q)
    html = scraperwiki.scrape("%s%s" % (next_url,extra_q))
    soup = BeautifulSoup.BeautifulSoup(html)
    bmlist = soup.find("ul",id="bookmarklist").findAll("li",recursive=False)
    current_date = None
    for li in bmlist:
        data_div = li.find("div",{ "class" : "data" })
        meta_div = li.find("div",{ "class" : "meta" })
        date_div = li.find("div",{ "class" : "dateGroup" })
        item = {}
        if(date_div):
            date_string = date_div.span.string.strip()
            try:
                current_date = datetime.fromtimestamp(time.mktime(time.strptime(date_string, u'%d %b %y')))
            except:
                current_date = None
        id = li['id'].split("-")[1]
        item["date"] = current_date
        item['id'] = id
        item['title'] = data_div.h4.a.string
        item['href'] = data_div.h4.a['href']
        item['user_name'] = meta_div.find("a",{"class":"user user-tag"})['title']
        item['user_uid'] = meta_div.find("a",{"class":"user user-tag"})['href']
        a_tags = meta_div.findAll("a",rel="tag")
        item['tags'] = []
        for a_tag in a_tags:
            tag = {}
            tag['text'] = a_tag.string
            tag['uri'] = a_tag['href']
            item['tags'].append(tag)
        scraperwiki.datastore.save(['id'],item)
    next_url_a = soup.find("a",{"class":"pn next"})
    if next_url_a:
        next_url = base_url + next_url_a["href"]
    else:
        next_url = None
    
# Blank Python
base_url = "http://www.delicious.com"
start_url = "http://www.delicious.com/tag/startup?"
extra_q = "&detail=3&setcount=100"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import scraperwiki
import BeautifulSoup
from datetime import datetime
import time

next_url = start_url
while next_url:
    print "getting %s%s" % (next_url,extra_q)
    html = scraperwiki.scrape("%s%s" % (next_url,extra_q))
    soup = BeautifulSoup.BeautifulSoup(html)
    bmlist = soup.find("ul",id="bookmarklist").findAll("li",recursive=False)
    current_date = None
    for li in bmlist:
        data_div = li.find("div",{ "class" : "data" })
        meta_div = li.find("div",{ "class" : "meta" })
        date_div = li.find("div",{ "class" : "dateGroup" })
        item = {}
        if(date_div):
            date_string = date_div.span.string.strip()
            try:
                current_date = datetime.fromtimestamp(time.mktime(time.strptime(date_string, u'%d %b %y')))
            except:
                current_date = None
        id = li['id'].split("-")[1]
        item["date"] = current_date
        item['id'] = id
        item['title'] = data_div.h4.a.string
        item['href'] = data_div.h4.a['href']
        item['user_name'] = meta_div.find("a",{"class":"user user-tag"})['title']
        item['user_uid'] = meta_div.find("a",{"class":"user user-tag"})['href']
        a_tags = meta_div.findAll("a",rel="tag")
        item['tags'] = []
        for a_tag in a_tags:
            tag = {}
            tag['text'] = a_tag.string
            tag['uri'] = a_tag['href']
            item['tags'].append(tag)
        scraperwiki.datastore.save(['id'],item)
    next_url_a = soup.find("a",{"class":"pn next"})
    if next_url_a:
        next_url = base_url + next_url_a["href"]
    else:
        next_url = None
    
# Blank Python
base_url = "http://www.delicious.com"
start_url = "http://www.delicious.com/tag/startup?"
extra_q = "&detail=3&setcount=100"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import scraperwiki
import BeautifulSoup
from datetime import datetime
import time

next_url = start_url
while next_url:
    print "getting %s%s" % (next_url,extra_q)
    html = scraperwiki.scrape("%s%s" % (next_url,extra_q))
    soup = BeautifulSoup.BeautifulSoup(html)
    bmlist = soup.find("ul",id="bookmarklist").findAll("li",recursive=False)
    current_date = None
    for li in bmlist:
        data_div = li.find("div",{ "class" : "data" })
        meta_div = li.find("div",{ "class" : "meta" })
        date_div = li.find("div",{ "class" : "dateGroup" })
        item = {}
        if(date_div):
            date_string = date_div.span.string.strip()
            try:
                current_date = datetime.fromtimestamp(time.mktime(time.strptime(date_string, u'%d %b %y')))
            except:
                current_date = None
        id = li['id'].split("-")[1]
        item["date"] = current_date
        item['id'] = id
        item['title'] = data_div.h4.a.string
        item['href'] = data_div.h4.a['href']
        item['user_name'] = meta_div.find("a",{"class":"user user-tag"})['title']
        item['user_uid'] = meta_div.find("a",{"class":"user user-tag"})['href']
        a_tags = meta_div.findAll("a",rel="tag")
        item['tags'] = []
        for a_tag in a_tags:
            tag = {}
            tag['text'] = a_tag.string
            tag['uri'] = a_tag['href']
            item['tags'].append(tag)
        scraperwiki.datastore.save(['id'],item)
    next_url_a = soup.find("a",{"class":"pn next"})
    if next_url_a:
        next_url = base_url + next_url_a["href"]
    else:
        next_url = None
    
# Blank Python
base_url = "http://www.delicious.com"
start_url = "http://www.delicious.com/tag/startup?"
extra_q = "&detail=3&setcount=100"
# (extracts the values to use.  more sections are needed below to help show what functions to call next)

import scraperwiki
import BeautifulSoup
from datetime import datetime
import time

next_url = start_url
while next_url:
    print "getting %s%s" % (next_url,extra_q)
    html = scraperwiki.scrape("%s%s" % (next_url,extra_q))
    soup = BeautifulSoup.BeautifulSoup(html)
    bmlist = soup.find("ul",id="bookmarklist").findAll("li",recursive=False)
    current_date = None
    for li in bmlist:
        data_div = li.find("div",{ "class" : "data" })
        meta_div = li.find("div",{ "class" : "meta" })
        date_div = li.find("div",{ "class" : "dateGroup" })
        item = {}
        if(date_div):
            date_string = date_div.span.string.strip()
            try:
                current_date = datetime.fromtimestamp(time.mktime(time.strptime(date_string, u'%d %b %y')))
            except:
                current_date = None
        id = li['id'].split("-")[1]
        item["date"] = current_date
        item['id'] = id
        item['title'] = data_div.h4.a.string
        item['href'] = data_div.h4.a['href']
        item['user_name'] = meta_div.find("a",{"class":"user user-tag"})['title']
        item['user_uid'] = meta_div.find("a",{"class":"user user-tag"})['href']
        a_tags = meta_div.findAll("a",rel="tag")
        item['tags'] = []
        for a_tag in a_tags:
            tag = {}
            tag['text'] = a_tag.string
            tag['uri'] = a_tag['href']
            item['tags'].append(tag)
        scraperwiki.datastore.save(['id'],item)
    next_url_a = soup.find("a",{"class":"pn next"})
    if next_url_a:
        next_url = base_url + next_url_a["href"]
    else:
        next_url = None
    
