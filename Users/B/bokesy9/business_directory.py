# Blank Python
import scraperwiki
import lxml.html
import urllib2
import datetime
import re

urlp = 'http://www.directory.im/directory_searchresult.aspx?setpage='

#help(re)

def Scrape(number):
    url = "%s%d" % (urlp, number)
    root = lxml.html.parse(url).getroot()
    content = root.cssselect("div#mainCol")
    assert len(content) == 1, url
    tables = content[0].cssselect("div#panel twoCol")
    print len(tables)
    assert 1 <= len(tables) <= 4, (url)
    html = lxml.html.tostring(root)
    mviewstate = re.search('name="__VIEWSTATE"\s*value="([^"]*)"\s*/?>', html)
    assert mviewstate, (url, html)
    html = "%s %s" % (html[:mviewstate.start(1)], html[mviewstate.end(1):])
    moutofrange = re.search('<font color="Red">Index was out of range.', html)
    if moutofrange:
        return None

    data = {"number":number, "url":url}
    data["html"] = html

    scraperwiki.sqlite.save(unique_keys=["number", "html"], data=data, table_name="initial")

def MainScrape():
    for i in range(21, 23):
        Scrape(i)

#MainScrape()



