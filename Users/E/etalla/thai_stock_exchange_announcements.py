# Retrieves news announcements from selected companies (listed in the symbols list) of the Thai Stock Exchange. 
import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
from dateutil import parser
import urllib, urlparse
import lxml.etree, lxml.html
import re
import json

sourcescraper = 'thai_stock_listed_companies'
scraperwiki.sqlite.attach(sourcescraper)
 
keys =  scraperwiki.sqlite.execute('select * from `thai_stock_listed_companies`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `thai_stock_listed_companies`.swdata')

symbols = ['ASIAN','CFRESH','CPF','TUF','TRS','CHOTI','LEE','OISHI','PPC','SORKON','SSF','TC']

def get_news(symbol,name):
    news = {}
    url = 'http://www.set.or.th/set/companynews.do?symbol=%s&language=en&country=US' %(symbol)
    root = scraperwiki.scrape(url)
    root = lxml.html.fromstring(root)
    section = root.cssselect("a[name]")[0].getnext()
    section = section[1].cssselect("a")
    counter = 0
    for i in section:
        core = i.getparent().getprevious().getprevious().getprevious().getprevious().getparent()
        news['date'] = core.cssselect("td[align=nowrap]")[0].text_content()
        news['date']= str(parser.parse(news['date']))[:-9]
        if int(news['date'][:4]) > 2012:
            news['title'] = core.cssselect("td[align=left]")[0].text_content().strip()
            core = core.cssselect("a")
            for links in core:
                news['link'] = links.get("href").strip()
                if news['link'][0:4]!="http":
                    news['link'] = "http://www.set.or.th" + news['link']
            news['company']=(name.replace("TRADING FROZEN FOOD","")
                                 .replace("PUBLIC CO., LTD.","")
                                 .replace("PUBLIC COMPANY LIMITED","").strip())
            news['symbol']=symbol
            news['key'] = (str(symbol) +" -- " + str(news['title']) +" -- " +str(news['date']))
            scraperwiki.sqlite.save(['key'],news)


for row in data:
    if row.get('symbol') in symbols:
        name = row.get('name')
        symbol  = row.get('symbol')
        get_news(symbol,name)
