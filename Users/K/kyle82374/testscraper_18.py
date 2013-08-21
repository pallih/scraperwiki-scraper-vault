# Metacritic Scraper

import scraperwiki
import lxml.html
import re

types = ['movies/release-date/theaters',]

for type in types:
    url = "http://www.metacritic.com/browse/%s/date?view=detailed" % type

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    products = root.xpath("//ol[@class='list_products list_product_summaries']/li")
    
    for product in products:
        data = {}
        data['title'] = product.xpath("div/div/div/div/div/h3/a/text()")
        print data['title']
        data['url'] = str(product.xpath("div/div/div/div/div/h3/a/@href")[0])
        print data['url']
        #product_score = product.xpath("div/div/div/div/div/div[@class='std_score']/div[@class='score_wrap']/span[2]/text()")
        product_score = product.xpath("div/div/div/div/a/div/div/span[2]/text()")
        print product_score
        if len(product_score) != 1 or product_score[0] == 'tbd':
            data['score'] = -1
        else:
            data['score'] = int(product_score[0])

        data['type'] = type
        scraperwiki.sqlite.save(unique_keys=['title', 'url'], data=data)
