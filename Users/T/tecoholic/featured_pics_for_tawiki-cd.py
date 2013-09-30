import scraperwiki
import lxml.html
# Blank Python

html = scraperwiki.scrape("http://tawp.in/r/2gxd")

doc = lxml.html.fromstring(html)
ans = doc.cssselect("h2.title-blog a")
for an in ans:
    print an.text_content()
import scraperwiki
import lxml.html
# Blank Python

html = scraperwiki.scrape("http://tawp.in/r/2gxd")

doc = lxml.html.fromstring(html)
ans = doc.cssselect("h2.title-blog a")
for an in ans:
    print an.text_content()
