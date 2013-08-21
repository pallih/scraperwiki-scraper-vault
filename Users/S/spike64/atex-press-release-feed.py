import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.atex.com/news-events/press-releases")

root = lxml.html.fromstring(html)
for section in root.cssselect("ul[class='latest-news']"):
    for item in section.cssselect("li"):
        
        item = {
            'title' : item.cssselect("a")[0].text_content().strip('\t\r\n'),
            'link' : "http://www.atex.com" + item.cssselect("a")[0].get("href"),
            'description' : item.cssselect("p")[0].text_content(),
            'pubDate' : item.cssselect("time")[0].get("datetime")
        }
        
        print item
        
        scraperwiki.sqlite.save(unique_keys=["link"], data = item)
