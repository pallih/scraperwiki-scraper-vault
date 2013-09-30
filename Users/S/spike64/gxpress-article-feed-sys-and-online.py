import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.gxpress.net/section/systems-online")

root = lxml.html.fromstring(html)
for table in root.cssselect("table[class='bw_news_detail_article']"):
    if len(table.cssselect("p")) > 0 :
        description = [ table.cssselect("p")[0].text_content() ]
    else :
        d = table.cssselect("td")[0].xpath("./text()")
        if len(d) > 0 :
            description = d[0]
        else :
            description = table.cssselect("td")[0].text_content()

    item = {
        'title' : table.cssselect("a")[0].text_content(),
        'link' : table.cssselect("a")[0].get("href"),
        'description' : description
    }

    print item
    
    scraperwiki.sqlite.save(unique_keys=["link"], data = item)
import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.gxpress.net/section/systems-online")

root = lxml.html.fromstring(html)
for table in root.cssselect("table[class='bw_news_detail_article']"):
    if len(table.cssselect("p")) > 0 :
        description = [ table.cssselect("p")[0].text_content() ]
    else :
        d = table.cssselect("td")[0].xpath("./text()")
        if len(d) > 0 :
            description = d[0]
        else :
            description = table.cssselect("td")[0].text_content()

    item = {
        'title' : table.cssselect("a")[0].text_content(),
        'link' : table.cssselect("a")[0].get("href"),
        'description' : description
    }

    print item
    
    scraperwiki.sqlite.save(unique_keys=["link"], data = item)
