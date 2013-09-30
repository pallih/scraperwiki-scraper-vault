#Work in progress - still needs to handle multi-page articles

import scraperwiki
import feedparser
import lxml.html
from time import mktime
from datetime import datetime

scraperwiki.sqlite.execute("DROP TABLE `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`url` text, `article` text, `published_time` text, `title` text,`author` text)")

lecho = feedparser.parse('http://feeds.feedburner.com/AnalysisIntelligence')

already_scraped = []
for each in scraperwiki.sqlite.select('''url from swdata'''):
    already_scraped.append(each['url'])

for each in lecho['entries']:
    url = each['links'][0]['href']
    published_time = datetime.fromtimestamp(mktime(each['updated_parsed']))
    title = each['title']
    if url not in already_scraped:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        content = root.cssselect("div.article p")
        author = root.cssselect("a.i-author")
        authorname = ""
        for each in author:
            if each.text is not None:
                authorname = each.text
        article = ""
        for each in content:
            if each.text is not None:
                article = article + each.text + "\n\n"
        scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "published_time":published_time, "title":title, "article":article, "author":authorname})
        

        
#Work in progress - still needs to handle multi-page articles

import scraperwiki
import feedparser
import lxml.html
from time import mktime
from datetime import datetime

scraperwiki.sqlite.execute("DROP TABLE `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`url` text, `article` text, `published_time` text, `title` text,`author` text)")

lecho = feedparser.parse('http://feeds.feedburner.com/AnalysisIntelligence')

already_scraped = []
for each in scraperwiki.sqlite.select('''url from swdata'''):
    already_scraped.append(each['url'])

for each in lecho['entries']:
    url = each['links'][0]['href']
    published_time = datetime.fromtimestamp(mktime(each['updated_parsed']))
    title = each['title']
    if url not in already_scraped:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        content = root.cssselect("div.article p")
        author = root.cssselect("a.i-author")
        authorname = ""
        for each in author:
            if each.text is not None:
                authorname = each.text
        article = ""
        for each in content:
            if each.text is not None:
                article = article + each.text + "\n\n"
        scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "published_time":published_time, "title":title, "article":article, "author":authorname})
        

        
