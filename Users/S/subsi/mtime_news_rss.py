import scraperwiki
import re, ast, cgi, os
import datetime
from dateutil import parser


sourcescraper = 'mtime_news_fulltext'
scraperwiki.sqlite.attach(sourcescraper, "news")
_params_ = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))



def main():
    link = "http://news.mtime.com/movie/2/"
    title = "Mtime News Occident"
    showRssFeed(newsFeed, title, link)



def newsFeed():
    conf = scraperwiki.sqlite.select("* from news.conf where name='urls'")
    urls = str(tuple(ast.literal_eval(conf[0]["value"])))
    dataset = scraperwiki.sqlite.select("* from news.swdata where url in %s order by time desc" % urls)
    for item in dataset:
        prefix = ""
        if bool(item["fails"]): prefix += "[X]"
        if bool(item["updated"]): prefix += "[U]"
        if prefix: prefix +=" "
        time = item["time"][:-3]
        title = "%s%s (%s)" % (prefix, item["title"], time)
        guid = "%s#%s" % (item["url"], re.sub(r"\D", "", time))
        showRssItem(guid, title, item["url"], chnfmt(parser.parse(time)), item["content"])



def showRssItem(guid, title, link, time, description):
    print """
    <item>
        <title><![CDATA[%s]]></title>
        <link>%s</link>
        <pubDate>%s</pubDate>
        <guid isPermaLink="false">%s</guid>
        <description><![CDATA[
""" % (title, link, time, guid)
    if callable(description): description()
    else: print description
    print "]]></description></item>"


def showRssFeed(itemsbuilder, title, link, description=None):
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')
    now = datetime.datetime.now()
    print """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <pubDate>%s</pubDate>
    <generator>ScraperWiki subsi</generator>
""" % (title, link, description or title, utcfmt(now))
    itemsbuilder()
    print "</channel></rss>"



def utcfmt(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z+0000")

def chnfmt(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z+0800")

#########
main()

import scraperwiki
import re, ast, cgi, os
import datetime
from dateutil import parser


sourcescraper = 'mtime_news_fulltext'
scraperwiki.sqlite.attach(sourcescraper, "news")
_params_ = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))



def main():
    link = "http://news.mtime.com/movie/2/"
    title = "Mtime News Occident"
    showRssFeed(newsFeed, title, link)



def newsFeed():
    conf = scraperwiki.sqlite.select("* from news.conf where name='urls'")
    urls = str(tuple(ast.literal_eval(conf[0]["value"])))
    dataset = scraperwiki.sqlite.select("* from news.swdata where url in %s order by time desc" % urls)
    for item in dataset:
        prefix = ""
        if bool(item["fails"]): prefix += "[X]"
        if bool(item["updated"]): prefix += "[U]"
        if prefix: prefix +=" "
        time = item["time"][:-3]
        title = "%s%s (%s)" % (prefix, item["title"], time)
        guid = "%s#%s" % (item["url"], re.sub(r"\D", "", time))
        showRssItem(guid, title, item["url"], chnfmt(parser.parse(time)), item["content"])



def showRssItem(guid, title, link, time, description):
    print """
    <item>
        <title><![CDATA[%s]]></title>
        <link>%s</link>
        <pubDate>%s</pubDate>
        <guid isPermaLink="false">%s</guid>
        <description><![CDATA[
""" % (title, link, time, guid)
    if callable(description): description()
    else: print description
    print "]]></description></item>"


def showRssFeed(itemsbuilder, title, link, description=None):
    scraperwiki.utils.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')
    now = datetime.datetime.now()
    print """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>%s</title>
    <link>%s</link>
    <description>%s</description>
    <pubDate>%s</pubDate>
    <generator>ScraperWiki subsi</generator>
""" % (title, link, description or title, utcfmt(now))
    itemsbuilder()
    print "</channel></rss>"



def utcfmt(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z+0000")

def chnfmt(dt):
    return dt.strftime("%a, %d %b %Y %H:%M:%S %z+0800")

#########
main()

