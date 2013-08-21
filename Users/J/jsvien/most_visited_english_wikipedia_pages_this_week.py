import scraperwiki
import lxml.html
import re
VIEWPATTERN = re.compile(r"\(([\s\d]+) views\)")
html = scraperwiki.scrape("http://toolserver.org/~johang/wikitrends/english-most-visited-this-week.html")
root = lxml.html.fromstring(html)
items = root.cssselect("ol li")
for i in range(len(items)):
    item = items[i]
    wikipage = item.cssselect("h3 a")[0]
    href = wikipage.attrib["href"]
    title = wikipage.text
    views = VIEWPATTERN.match(item.cssselect("h3 span")[0].text).group(1).replace(" ", "")
    summary = item.cssselect(".summary")[0].text
    data = {
        "rank": i + 1,
        "title": title,
        "href": href,
        "views": views,
        "summary": summary
    }
    print data
    scraperwiki.sqlite.save(["rank"], data)