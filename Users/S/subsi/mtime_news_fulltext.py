import scraperwiki
import lxml.html
import os, re, ast
import urllib2, gzip, StringIO
import datetime
from dateutil import parser


def main():
    fetchAndSaveNews()
    



def fetchAndSaveNews():
    url = "http://news.mtime.com/movie/2/"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    urls = []
    for li in root.cssselect("ul.news_lists li"):
        link = li.cssselect("a")[0]
        item = {
            "time": parseChnTime(li.cssselect("span")[0].text),
            "url": link.attrib["href"],
            "title": link.text,
            "updated": False,
        }
        urls.append(item["url"])
        if not needSave(item): continue
        print item["title"]
        (success, content) = fetchNewsContent(item["url"])
        item["fails"] = not success
        if success:
            item["content"] = content
        if success or not item["updated"]:
            scraperwiki.sqlite.save(["url"], item)
    scraperwiki.sqlite.save(["name"], {"name":"urls", "value":urls}, "conf")



def needSave(item):
    dataset = scraperwiki.sqlite.select("time, fails, title from swdata where url=?", item["url"])
    if not dataset: return True
    data = dataset[0]
    item["updated"] = True
    if data["title"] != item["title"]: return True
    if data["time"] != item["time"]: return True
    if bool(data["fails"]): return True
    return False


def fetchNewsContent(url):
    try:
        html = fetchZippedHtml(url)
        root = lxml.html.fromstring(html)
        contentdiv = root.cssselect("div#newscont")[0]
        content = lxml.html.tostring(contentdiv)
        content = content.replace("</a><a", "</a>&nbsp; <a ")
        return (True, content)
    except: pass
    return (False, None)


def fetchZippedHtml(url):
    f = urllib2.urlopen(url)
    html = f.read()
    if f.info().get('Content-Encoding'):
        data = StringIO.StringIO(html)
        gz = gzip.GzipFile(fileobj=data)
        html = gz.read()
        gz.close()
    return html


def parseChnTime(cntime):
    now = datetime.datetime.now() + datetime.timedelta(days=40)
    time = re.sub(r"\D", "", cntime)
    month = int(time[:2])
    year = now.year
    if month>now.month: year-=1
    return str(parser.parse(str(year)+time))


def initDatabase():
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `swdata` (`url` text PRIMARY KEY, `time`, `fails`, `updated`, `title`, `content`)')
    scraperwiki.sqlite.commit()


##########
main()

import scraperwiki
import lxml.html
import os, re, ast
import urllib2, gzip, StringIO
import datetime
from dateutil import parser


def main():
    fetchAndSaveNews()
    



def fetchAndSaveNews():
    url = "http://news.mtime.com/movie/2/"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    urls = []
    for li in root.cssselect("ul.news_lists li"):
        link = li.cssselect("a")[0]
        item = {
            "time": parseChnTime(li.cssselect("span")[0].text),
            "url": link.attrib["href"],
            "title": link.text,
            "updated": False,
        }
        urls.append(item["url"])
        if not needSave(item): continue
        print item["title"]
        (success, content) = fetchNewsContent(item["url"])
        item["fails"] = not success
        if success:
            item["content"] = content
        if success or not item["updated"]:
            scraperwiki.sqlite.save(["url"], item)
    scraperwiki.sqlite.save(["name"], {"name":"urls", "value":urls}, "conf")



def needSave(item):
    dataset = scraperwiki.sqlite.select("time, fails, title from swdata where url=?", item["url"])
    if not dataset: return True
    data = dataset[0]
    item["updated"] = True
    if data["title"] != item["title"]: return True
    if data["time"] != item["time"]: return True
    if bool(data["fails"]): return True
    return False


def fetchNewsContent(url):
    try:
        html = fetchZippedHtml(url)
        root = lxml.html.fromstring(html)
        contentdiv = root.cssselect("div#newscont")[0]
        content = lxml.html.tostring(contentdiv)
        content = content.replace("</a><a", "</a>&nbsp; <a ")
        return (True, content)
    except: pass
    return (False, None)


def fetchZippedHtml(url):
    f = urllib2.urlopen(url)
    html = f.read()
    if f.info().get('Content-Encoding'):
        data = StringIO.StringIO(html)
        gz = gzip.GzipFile(fileobj=data)
        html = gz.read()
        gz.close()
    return html


def parseChnTime(cntime):
    now = datetime.datetime.now() + datetime.timedelta(days=40)
    time = re.sub(r"\D", "", cntime)
    month = int(time[:2])
    year = now.year
    if month>now.month: year-=1
    return str(parser.parse(str(year)+time))


def initDatabase():
    scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS `swdata` (`url` text PRIMARY KEY, `time`, `fails`, `updated`, `title`, `content`)')
    scraperwiki.sqlite.commit()


##########
main()

