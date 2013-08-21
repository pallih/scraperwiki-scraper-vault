import scraperwiki

# Blank Python

import lxml.html

datas = scraperwiki.scrape("http://thonegger.com/dir/journalsidtitle.csv")
import csv           
URLs= csv.reader(datas.splitlines())

for urli in URLs:
    url = urli[1]
    try:
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
        data = lxml.html.parse(url)
        root.make_links_absolute(url)
        if (url != data.docinfo.URL):
            url = data.docinfo.URL
        for el in root.cssselect("a"):           
            if (lxml.html.tostring(el).find("rss")>=0):
                feed=el.attrib['href']
                if (feed.find("http")>=0):
                    rss=feed
                else:
                    if (feed.find("/")==0 and url.endswith("/")):
                        rss=url+feed.lstrip("/")
                    else:
                        rss=url+feed
        data = {
            'id' : urli[0],
            'url': url,
            'rss': rss,
        }
        scraperwiki.sqlite.save(unique_keys=['id'],data = data)

    except:

        pass
