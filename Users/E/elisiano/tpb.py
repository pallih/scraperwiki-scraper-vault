import scraperwiki
import lxml.html
import re
import urllib, urllib2, urlparse, lxml, lxml.html
from pprint import pprint as pp
import datetime, time

host="https://thepiratebay.se"
category = { "Highres TV Show": 208, "Highres Movies": 207,}
sorting = { "Uploaded DESC": 3, "Uploaded ASC": 4}
page=0

url = "%s/browse/%d/%d/%d" % (host, category['Highres TV Show'], page, sorting['Uploaded DESC'])
#print url


class TPBTorrent(object):
        def __init__(self, link, title='', guid='', seeders=0, leechers=0, pubDate=time.localtime(), category="undefined"):
                self.torrent = {        "link": link,
                                        "title" : title,
                                        "guid" : guid,
                                        "seeders": seeders,
                                        "leechers": leechers,
                                        "pubDate": pubDate,
                                        "category": category,
                                }
        def __str__(self):
            return "<TPBTorrent %s >" % self.torrent['guid']

            #return "<TPBTorrent %s (s:%s l:%s) >" % ( self.torrent["title"], 
            #                                          self.torrent['seeders'],
            #                                          self.torrent['leechers'])
                                                        
        def __repr__(self):
                return self.__str__()


class TPBPage(object):
        def __init__(self, url, category):
                self.url = url
                #self.html = urllib2.urlopen(url).read()
                self.html = scraperwiki.scrape(url)
                self.root = lxml.html.fromstring(self.html)
                self.torrents = []
                up = urlparse.urlparse(url)
                for tr in self.root.cssselect("div#main-content tr"):
                    tds = tr.cssselect("td[class!='vertTh']")
                    if len(tds)==3:
                        links = tds[0].cssselect("a")

                        title = links[0].text
                        guid = "%s://%s%s" % (up.scheme, up.hostname, links[0].get("href"))
                        link = links[1].get("href")
                        seeders = tds[1].text
                        leechers = tds[2].text
                        if title and link:
                            self.torrents.append(TPBTorrent(link,title=title,guid=guid,seeders=seeders,leechers=leechers,category=category))

class TPBCategoryScraper(object):
    def __init__(self, category, max_recent_pages=5, sorting = sorting['Uploaded DESC']):
        self.url_template = r"""https://thepiratebay.se/browse/%s/%s/%s"""
        self.max_recent_pages=max_recent_pages
        self.current_page=0
        self.category=category
        self.sorting=sorting
        
    def getPage(self, page=0):
        p = TPBPage(self.url_template % (self.category, page, self.sorting), self.category)
        return p

    def getPages(self):
        pages=[]
        while self.current_page < self.max_recent_pages:
            pages.append(self.getPage(self.current_page))
            self.current_page+=1
        return pages

    def scrape(self):
        for p in self.getPages():
            for t in p.torrents:
                scraperwiki.sqlite.save(unique_keys=['guid'], data=t.torrent)


for cat in category.itervalues():
    cs = TPBCategoryScraper(cat)
    cs.scrape()
import scraperwiki
import lxml.html
import re
import urllib, urllib2, urlparse, lxml, lxml.html
from pprint import pprint as pp
import datetime, time

host="https://thepiratebay.se"
category = { "Highres TV Show": 208, "Highres Movies": 207,}
sorting = { "Uploaded DESC": 3, "Uploaded ASC": 4}
page=0

url = "%s/browse/%d/%d/%d" % (host, category['Highres TV Show'], page, sorting['Uploaded DESC'])
#print url


class TPBTorrent(object):
        def __init__(self, link, title='', guid='', seeders=0, leechers=0, pubDate=time.localtime(), category="undefined"):
                self.torrent = {        "link": link,
                                        "title" : title,
                                        "guid" : guid,
                                        "seeders": seeders,
                                        "leechers": leechers,
                                        "pubDate": pubDate,
                                        "category": category,
                                }
        def __str__(self):
            return "<TPBTorrent %s >" % self.torrent['guid']

            #return "<TPBTorrent %s (s:%s l:%s) >" % ( self.torrent["title"], 
            #                                          self.torrent['seeders'],
            #                                          self.torrent['leechers'])
                                                        
        def __repr__(self):
                return self.__str__()


class TPBPage(object):
        def __init__(self, url, category):
                self.url = url
                #self.html = urllib2.urlopen(url).read()
                self.html = scraperwiki.scrape(url)
                self.root = lxml.html.fromstring(self.html)
                self.torrents = []
                up = urlparse.urlparse(url)
                for tr in self.root.cssselect("div#main-content tr"):
                    tds = tr.cssselect("td[class!='vertTh']")
                    if len(tds)==3:
                        links = tds[0].cssselect("a")

                        title = links[0].text
                        guid = "%s://%s%s" % (up.scheme, up.hostname, links[0].get("href"))
                        link = links[1].get("href")
                        seeders = tds[1].text
                        leechers = tds[2].text
                        if title and link:
                            self.torrents.append(TPBTorrent(link,title=title,guid=guid,seeders=seeders,leechers=leechers,category=category))

class TPBCategoryScraper(object):
    def __init__(self, category, max_recent_pages=5, sorting = sorting['Uploaded DESC']):
        self.url_template = r"""https://thepiratebay.se/browse/%s/%s/%s"""
        self.max_recent_pages=max_recent_pages
        self.current_page=0
        self.category=category
        self.sorting=sorting
        
    def getPage(self, page=0):
        p = TPBPage(self.url_template % (self.category, page, self.sorting), self.category)
        return p

    def getPages(self):
        pages=[]
        while self.current_page < self.max_recent_pages:
            pages.append(self.getPage(self.current_page))
            self.current_page+=1
        return pages

    def scrape(self):
        for p in self.getPages():
            for t in p.torrents:
                scraperwiki.sqlite.save(unique_keys=['guid'], data=t.torrent)


for cat in category.itervalues():
    cs = TPBCategoryScraper(cat)
    cs.scrape()
