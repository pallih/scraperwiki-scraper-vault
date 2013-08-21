import scraperwiki
import lxml.html

root = scraperwiki.scrape('http://onethingwell.org/')

content = lxml.html.etree.HTML(root)

linkage = content.xpath("/html/body/div/article/h2/a/@href")

for links in linkage:
    record = { "link" : links }
    scraperwiki.datastore.save(["link"], record)
