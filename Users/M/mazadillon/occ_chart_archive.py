import scraperwiki
import lxml.html
import time

def scrapeyear(url,chart):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    weeks = root.xpath('//table[@class="chart nonseq archive purple"]/tr/td/a/@href')
    for week in weeks:
        print week
        scrapechart('http://www.officialcharts.com'+week,chart)
        time.sleep(1)

def scrapechart(url,chart):
    data = dict()
    data['date'] = url[-11:-1]
    data['chart'] = chart
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    titles = root.xpath('//table/tr[@class="entry"]/td[@class="info"]/div/h3')
    artists = root.xpath('//table/tr[@class="entry"]/td[@class="info"]/div/h4')
    positions = root.xpath('//table/tr[@class="entry"]/td[@class="currentposition"]')
    for position in positions:
        data['position'] = position.text_content()
        id = int(data['position']) - 1
        data['artist'] = artists[id].text_content()
        data['title'] = titles[id].text_content()
        scraperwiki.sqlite.save(['date','position','chart'],data)

for x in range(2008, 2013):
    scrapeyear('http://www.officialcharts.com/archive-chart/_/1/'+str(x)+'/',1)

import scraperwiki
import lxml.html
import time

def scrapeyear(url,chart):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    weeks = root.xpath('//table[@class="chart nonseq archive purple"]/tr/td/a/@href')
    for week in weeks:
        print week
        scrapechart('http://www.officialcharts.com'+week,chart)
        time.sleep(1)

def scrapechart(url,chart):
    data = dict()
    data['date'] = url[-11:-1]
    data['chart'] = chart
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    titles = root.xpath('//table/tr[@class="entry"]/td[@class="info"]/div/h3')
    artists = root.xpath('//table/tr[@class="entry"]/td[@class="info"]/div/h4')
    positions = root.xpath('//table/tr[@class="entry"]/td[@class="currentposition"]')
    for position in positions:
        data['position'] = position.text_content()
        id = int(data['position']) - 1
        data['artist'] = artists[id].text_content()
        data['title'] = titles[id].text_content()
        scraperwiki.sqlite.save(['date','position','chart'],data)

for x in range(2008, 2013):
    scrapeyear('http://www.officialcharts.com/archive-chart/_/1/'+str(x)+'/',1)

