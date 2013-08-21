import mechanize 
import datetime
import urlparse
import scraperwiki

url = "http://www.unoosa.org/oosa/showSearch.do"

osoindexfields = ["dateoflaunchfilter text", "page integer", "html text", "scrapedate text"]
#scraperwiki.sqlite.execute("create table osoindex (%s)" % ",".join(osoindexfields))

scrapedate = datetime.datetime.now()

def Main():
    for y in reversed(range(1957, 2012)):
        print "Scraping:", y
        ScrapeIndex("%d" % y)


        # gets everything for a year and depaginates it
def ScrapeIndex(dateoflaunchfilter):
    br = mechanize.Browser()
    br.open(url)
    br.select_form('searchForm')
    br['dateOfLaunchCrit'] = dateoflaunchfilter
    response = br.submit()
    pageno = 0
    while True:
        html = response.read()
        scraperwiki.sqlite.execute("insert into osoindex values (?,?,?,?)", 
                      (dateoflaunchfilter, pageno, html, scrapedate.isoformat()))
        nextpagelinks = [ link  for link in br.links(url_regex="search.do")  if link.attrs[0] == ('title', 'next page') ]
        if not nextpagelinks:
            break
        response = br.follow_link(nextpagelinks[0])
        pageno += 1
    scraperwiki.sqlite.commit()

Main()
import mechanize 
import datetime
import urlparse
import scraperwiki

url = "http://www.unoosa.org/oosa/showSearch.do"

osoindexfields = ["dateoflaunchfilter text", "page integer", "html text", "scrapedate text"]
#scraperwiki.sqlite.execute("create table osoindex (%s)" % ",".join(osoindexfields))

scrapedate = datetime.datetime.now()

def Main():
    for y in reversed(range(1957, 2012)):
        print "Scraping:", y
        ScrapeIndex("%d" % y)


        # gets everything for a year and depaginates it
def ScrapeIndex(dateoflaunchfilter):
    br = mechanize.Browser()
    br.open(url)
    br.select_form('searchForm')
    br['dateOfLaunchCrit'] = dateoflaunchfilter
    response = br.submit()
    pageno = 0
    while True:
        html = response.read()
        scraperwiki.sqlite.execute("insert into osoindex values (?,?,?,?)", 
                      (dateoflaunchfilter, pageno, html, scrapedate.isoformat()))
        nextpagelinks = [ link  for link in br.links(url_regex="search.do")  if link.attrs[0] == ('title', 'next page') ]
        if not nextpagelinks:
            break
        response = br.follow_link(nextpagelinks[0])
        pageno += 1
    scraperwiki.sqlite.commit()

Main()
import mechanize 
import datetime
import urlparse
import scraperwiki

url = "http://www.unoosa.org/oosa/showSearch.do"

osoindexfields = ["dateoflaunchfilter text", "page integer", "html text", "scrapedate text"]
#scraperwiki.sqlite.execute("create table osoindex (%s)" % ",".join(osoindexfields))

scrapedate = datetime.datetime.now()

def Main():
    for y in reversed(range(1957, 2012)):
        print "Scraping:", y
        ScrapeIndex("%d" % y)


        # gets everything for a year and depaginates it
def ScrapeIndex(dateoflaunchfilter):
    br = mechanize.Browser()
    br.open(url)
    br.select_form('searchForm')
    br['dateOfLaunchCrit'] = dateoflaunchfilter
    response = br.submit()
    pageno = 0
    while True:
        html = response.read()
        scraperwiki.sqlite.execute("insert into osoindex values (?,?,?,?)", 
                      (dateoflaunchfilter, pageno, html, scrapedate.isoformat()))
        nextpagelinks = [ link  for link in br.links(url_regex="search.do")  if link.attrs[0] == ('title', 'next page') ]
        if not nextpagelinks:
            break
        response = br.follow_link(nextpagelinks[0])
        pageno += 1
    scraperwiki.sqlite.commit()

Main()
import mechanize 
import datetime
import urlparse
import scraperwiki

url = "http://www.unoosa.org/oosa/showSearch.do"

osoindexfields = ["dateoflaunchfilter text", "page integer", "html text", "scrapedate text"]
#scraperwiki.sqlite.execute("create table osoindex (%s)" % ",".join(osoindexfields))

scrapedate = datetime.datetime.now()

def Main():
    for y in reversed(range(1957, 2012)):
        print "Scraping:", y
        ScrapeIndex("%d" % y)


        # gets everything for a year and depaginates it
def ScrapeIndex(dateoflaunchfilter):
    br = mechanize.Browser()
    br.open(url)
    br.select_form('searchForm')
    br['dateOfLaunchCrit'] = dateoflaunchfilter
    response = br.submit()
    pageno = 0
    while True:
        html = response.read()
        scraperwiki.sqlite.execute("insert into osoindex values (?,?,?,?)", 
                      (dateoflaunchfilter, pageno, html, scrapedate.isoformat()))
        nextpagelinks = [ link  for link in br.links(url_regex="search.do")  if link.attrs[0] == ('title', 'next page') ]
        if not nextpagelinks:
            break
        response = br.follow_link(nextpagelinks[0])
        pageno += 1
    scraperwiki.sqlite.commit()

Main()
import mechanize 
import datetime
import urlparse
import scraperwiki

url = "http://www.unoosa.org/oosa/showSearch.do"

osoindexfields = ["dateoflaunchfilter text", "page integer", "html text", "scrapedate text"]
#scraperwiki.sqlite.execute("create table osoindex (%s)" % ",".join(osoindexfields))

scrapedate = datetime.datetime.now()

def Main():
    for y in reversed(range(1957, 2012)):
        print "Scraping:", y
        ScrapeIndex("%d" % y)


        # gets everything for a year and depaginates it
def ScrapeIndex(dateoflaunchfilter):
    br = mechanize.Browser()
    br.open(url)
    br.select_form('searchForm')
    br['dateOfLaunchCrit'] = dateoflaunchfilter
    response = br.submit()
    pageno = 0
    while True:
        html = response.read()
        scraperwiki.sqlite.execute("insert into osoindex values (?,?,?,?)", 
                      (dateoflaunchfilter, pageno, html, scrapedate.isoformat()))
        nextpagelinks = [ link  for link in br.links(url_regex="search.do")  if link.attrs[0] == ('title', 'next page') ]
        if not nextpagelinks:
            break
        response = br.follow_link(nextpagelinks[0])
        pageno += 1
    scraperwiki.sqlite.commit()

Main()
