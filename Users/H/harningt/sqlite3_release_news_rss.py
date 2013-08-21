# Blank Python
sourcescraper = 'sqlite3_release_news'
SQL = "title as title, content as description, source || '#' || key as link, key as guid, date as pubDate from news_items ORDER BY date DESC"

import datetime
import dateutil.parser
import scraperwiki

from lxml.builder import E
from lxml import etree

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml+rss")

# Site seems to deal w/ time in GMT, so force output as GMT - %Z does not appear to work

channel = E.channel(
    E.title("SQLite3 Release News"),
    E.link("https://sqlite.org/news.html"),
    E.description("SQLite3 Release News in RSS form"),
    E.lastBuildDate(datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")))

scraperwiki.sqlite.attach(sourcescraper)

for data in scraperwiki.sqlite.select(SQL):
    try:
        mytitle = E.title(data.get("title"))
        mylink = E.link(data.get("link"))
        mydesc = E.description(data.get("description"))
        myguid = E.guid(data.get("guid"), isPermalink="false")
        mypubdate = E.pubDate(dateutil.parser.parse(data.get("pubDate")).strftime("%a, %d %b %Y %H:%M:%S GMT"))
        item = E.item(mytitle, mylink, mydesc, myguid, mypubdate)
    except ValueError:
        print repr(title)
        print repr(link)
        print repr(description)
        raise
    channel.append(item)

rss = E.rss(channel, version = "2.0")

print etree.tostring(rss)
