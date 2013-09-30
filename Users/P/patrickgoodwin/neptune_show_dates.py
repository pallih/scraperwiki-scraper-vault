########Scrapewiki Assignment
########Patrick Goodwin and Max Martin


import scraperwiki
html = scraperwiki.scrape("http://www.stgpresents.org/tickets/alphabetical/range.listevents/-?catids=29")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div.cRight tr"):
    tds = tr.cssselect("td")
    date = tds[0].cssselect("span")[1].text
    name = tds[0].cssselect("a")[0].text
    url = tds[0].cssselect("a")[0].attrib['href']
    slashparts = url.split('/')
    basename = '/'.join(slashparts[3:]) + '/'   
    data = {
        'date': date,
        'name': name,
        'url': 'http://stgpresents.org/jevents-crawler-sitemap/' + basename
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['date'],data=data)
########Scrapewiki Assignment
########Patrick Goodwin and Max Martin


import scraperwiki
html = scraperwiki.scrape("http://www.stgpresents.org/tickets/alphabetical/range.listevents/-?catids=29")
print html

import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("div.cRight tr"):
    tds = tr.cssselect("td")
    date = tds[0].cssselect("span")[1].text
    name = tds[0].cssselect("a")[0].text
    url = tds[0].cssselect("a")[0].attrib['href']
    slashparts = url.split('/')
    basename = '/'.join(slashparts[3:]) + '/'   
    data = {
        'date': date,
        'name': name,
        'url': 'http://stgpresents.org/jevents-crawler-sitemap/' + basename
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['date'],data=data)
