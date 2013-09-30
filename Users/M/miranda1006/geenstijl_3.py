from lxml import html
import scraperwiki

# Blank Python
site = "http://geenstijl.nl/"
page = scraperwiki.scrape(site)
page = html.fromstring(page)

for article in page.cssselect("article.artikel"):
    link = article.cssselect ("footer a")[0].get ("href")
    print link
    article_page = html.fromstring(scraperwiki.scrape(link))
    title = article_page.cssselect("article.artikel h1")[0].text_content()
    text = article_page.cssselect("article.artikel p") [0].text_content()
    data = {"url":link, "title":title, "text":text}
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)from lxml import html
import scraperwiki

# Blank Python
site = "http://geenstijl.nl/"
page = scraperwiki.scrape(site)
page = html.fromstring(page)

for article in page.cssselect("article.artikel"):
    link = article.cssselect ("footer a")[0].get ("href")
    print link
    article_page = html.fromstring(scraperwiki.scrape(link))
    title = article_page.cssselect("article.artikel h1")[0].text_content()
    text = article_page.cssselect("article.artikel p") [0].text_content()
    data = {"url":link, "title":title, "text":text}
    scraperwiki.sqlite.save(unique_keys=["url"], data=data)