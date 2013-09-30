import lxml.html
import scraperwiki
import urllib, urlparse
from dateutil import parser

url = 'http://www.avi.co.za/investors/news'

def get_news():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    news_section = root.cssselect("div.grey_content")
    
    news = {}

    for row in news_section:
        news["title"] = row[0].text_content()
        news["summary"] = row[1].text_content()
        news["date"] = row[2].text_content()
        news["date"] = str(news["date"]).strip()[:11]
        news["date"] = parser.parse(news["date"])
        if str((row[3][0]).get("href"))[0] == "/":
            news["link"] = "http://www.avi.co.za" + str((row[3][0]).get("href"))
        else:
            news["link"] = (row[3][0]).get("href")
        scraperwiki.sqlite.save(['link'], news)

get_news()
import lxml.html
import scraperwiki
import urllib, urlparse
from dateutil import parser

url = 'http://www.avi.co.za/investors/news'

def get_news():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    news_section = root.cssselect("div.grey_content")
    
    news = {}

    for row in news_section:
        news["title"] = row[0].text_content()
        news["summary"] = row[1].text_content()
        news["date"] = row[2].text_content()
        news["date"] = str(news["date"]).strip()[:11]
        news["date"] = parser.parse(news["date"])
        if str((row[3][0]).get("href"))[0] == "/":
            news["link"] = "http://www.avi.co.za" + str((row[3][0]).get("href"))
        else:
            news["link"] = (row[3][0]).get("href")
        scraperwiki.sqlite.save(['link'], news)

get_news()
