# Real-time scrape a ScrapeWiki tag page and show a montage of all the images

import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://scraperwiki.com/tags/alphagov")
#print html

root = lxml.html.fromstring(html)
items = root.cssselect('.code_object_line h3 img')
for ss in items:
    img_url = ss.attrib["src"]
    # A deleted one
    if img_url == "http://media.scraperwiki.com/screenshots/small/directgov_local_services_a-z.png":
        continue

    print '''<img src="%s" style="padding: 1px">''' % img_url

print '<p>Number of scrapers:', len(items)

items = [ i.attrib["href"] for i in root.cssselect('.code_object_line h3 a[href^="/profiles/"]') ]
print '<p>Number of users:', len(set(items))

