import scraperwiki
import lxml.html           
from dateutil import parser

html = scraperwiki.scrape("http://confreaks.net/videos")
root = lxml.html.fromstring(html)
for div in root.cssselect("div.search_result"):
    title = div.cssselect("div.title a")[0].text_content() + ' (from ' + div.cssselect("div.conference a")[0].text_content() + ')'
    url = "http://confreaks.net" + div.cssselect("div.title a")[0].attrib['href']
    posted = parser.parse(div.cssselect("div.post-date strong")[0].text_content())
    scraperwiki.sqlite.save(unique_keys=['url'], data={'title': title, 'url': url, 'posted': posted})
import scraperwiki
import lxml.html           
from dateutil import parser

html = scraperwiki.scrape("http://confreaks.net/videos")
root = lxml.html.fromstring(html)
for div in root.cssselect("div.search_result"):
    title = div.cssselect("div.title a")[0].text_content() + ' (from ' + div.cssselect("div.conference a")[0].text_content() + ')'
    url = "http://confreaks.net" + div.cssselect("div.title a")[0].attrib['href']
    posted = parser.parse(div.cssselect("div.post-date strong")[0].text_content())
    scraperwiki.sqlite.save(unique_keys=['url'], data={'title': title, 'url': url, 'posted': posted})
