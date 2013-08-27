import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
import urllib
import re
import lxml.etree
import scraperwiki
import datetime
import scraperwiki.datastore
scraperwiki.cache(True)
import urlparse

def scrapedistricts():
    url = "http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/"
    html = urllib.urlopen(url).read()

    latestnews = re.findall('<h2><a href="http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/(.*?)-echo/">Latest news from (.*?)</a></h2>', html)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for tag, district in latestnews:
        for p in xrange(1, 15):
            urldistrict = 'http://www.liverpoolecho.co.uk/liverpool-news/echo-districts/'+tag+'-echo/'+tag+'-news/p'+str(p)+'/'
            try:
                htmldistrict = urllib.urlopen(urldistrict).read()
            except:
                print "Error on page: " + urldistrict
                print "skipping to next district"
                break
            
            print tag, district, p
    
            teasers = re.findall('(?s)<div class="teasers">\s*<div class="clearfix">\s*(<span.*?</span>)?\s*<h2>\s*<a\s*href="(.*?)"\s*>\s*(.*?)</a>(.*?)</div>', htmldistrict)
            for img, link, title, rest in teasers:
                mdate = re.findall('<span class="article-date">(\w+)\s*(\d+)\s+(\d+)\s*</span>', rest)
                assert mdate, rest
                monthname, day, year = mdate[0]
                imonth = months.index(monthname)
                # , day, year, mdate
                date = datetime.date(int(year), imonth + 1, int(day))
                data = { "articledate":date, "title":title, "district":district, "url":urlparse.urljoin(urldistrict, link), 'shortname':tag }        
                scraperwiki.datastore.save(unique_keys=["url", "district"], data=data, date=date)
        
scrapedistricts()
