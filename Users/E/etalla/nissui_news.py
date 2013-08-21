import scraperwiki
import lxml.html
import urllib, urlparse
from dateutil import parser

url = "http://www.nissui.co.jp/english/whatsnew/index.html"
root = lxml.html.parse(url).getroot()

news_section = root.cssselect("table.logList")

news = {}

for row in news_section[0]:
    news['link'] = "http://www.nissui.co.jp" + row.cssselect("a")[0].get("href")
    news['date'] = parser.parse(row.cssselect("span.date")[0].text)
    print news['date']
    news['title'] = row.cssselect("span.logs")[0].text
    scraperwiki.sqlite.save(['link'],news)
