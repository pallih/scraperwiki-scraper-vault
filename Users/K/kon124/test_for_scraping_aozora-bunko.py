import scraperwiki
import lxml.html


html = scraperwiki.scrape("http://www.aozora.gr.jp/cards/000020/files/2569_28291.html")
root = lxml.html.fromstring(html)

for el in root.cssselect("h2"):
    print el.text
