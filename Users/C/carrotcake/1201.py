import scraperwiki           
import lxml.html

html = scraperwiki.scrape("http://foodiebooty.tumblr.com/page/5")
root = lxml.html.fromstring(html)

e1 = root.cssselect("div.post img")
e2 = root.cssselect("div.caption a")

for x in e1:
    scraperwiki.sqlite.save(unique_keys=["src"], data = {"src":x.attrib['src']})

for y in e1:
    scraperwiki.sqlite.save(unique_keys=["alt"], data = {"alt":y.attrib['alt']})

for z in e2:
    scraperwiki.sqlite.save(unique_keys=["href"], data = {"href":z.attrib['href']})