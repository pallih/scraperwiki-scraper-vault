import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://eidosmedia.com/EN/Page/Uuid/e0bf4372-af33-11de-9d72-8e8f18867204/news.dwp")

root = lxml.html.fromstring(html)
for item in root.cssselect("div[class='newsitem']"):
    item = {
        'title' : item .cssselect("a")[0].text.strip('\r\n\t'),
        'link' : item .cssselect("a")[0].get("href"),
        'description' : item.cssselect("div[class='title']")[0].xpath("./text()"),
        'shortDate' : item.cssselect("span[class='ShortDate']")[0].text.strip('\r\n\t').replace(u'\xa0', u'')
    }
    
    print item
    
    scraperwiki.sqlite.save(unique_keys=["link"], data = item)
import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://eidosmedia.com/EN/Page/Uuid/e0bf4372-af33-11de-9d72-8e8f18867204/news.dwp")

root = lxml.html.fromstring(html)
for item in root.cssselect("div[class='newsitem']"):
    item = {
        'title' : item .cssselect("a")[0].text.strip('\r\n\t'),
        'link' : item .cssselect("a")[0].get("href"),
        'description' : item.cssselect("div[class='title']")[0].xpath("./text()"),
        'shortDate' : item.cssselect("span[class='ShortDate']")[0].text.strip('\r\n\t').replace(u'\xa0', u'')
    }
    
    print item
    
    scraperwiki.sqlite.save(unique_keys=["link"], data = item)
