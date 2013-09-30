import scraperwiki
import lxml.html
url = "http://www.dati.trentino.it/user"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
users = root.cssselect("ul")
import scraperwiki
import lxml.html
url = "http://www.dati.trentino.it/user"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
users = root.cssselect("ul")
