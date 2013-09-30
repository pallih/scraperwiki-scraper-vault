# Metacritic Scraper

import scraperwiki
import lxml.html
import re

types = [
    'games/release-date/new-releases/ps3', 'games/release-date/new-releases/xbox360', 'games/release-date/new-releases/wii',]

for type in types:
    url = "http://www.metacritic.com/browse/%s/date?view=detailed" % type

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    products = root.xpath("//ol[@class='list_products list_product_summaries']/li")

    for product in products:
        data = {}
        data['title'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/text()")[0])

        data['url'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/@href")[0])

        product_score = product.xpath("div/div/div/div/div/div[@class='std_score']/div[@class='score_wrap']/span[2]/text()")
        if len(product_score) != 1 or product_score[0] == 'tbd':
            data['score'] = -1
            print product_score
        else:
            data['score'] = int(product_score[0])
            print product_score

        data['type'] = type
        scraperwiki.sqlite.save(unique_keys=['title', 'url'], data=data)
# Metacritic Scraper

import scraperwiki
import lxml.html
import re

types = [
    'games/release-date/new-releases/ps3', 'games/release-date/new-releases/xbox360', 'games/release-date/new-releases/wii',]

for type in types:
    url = "http://www.metacritic.com/browse/%s/date?view=detailed" % type

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    products = root.xpath("//ol[@class='list_products list_product_summaries']/li")

    for product in products:
        data = {}
        data['title'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/text()")[0])

        data['url'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/@href")[0])

        product_score = product.xpath("div/div/div/div/div/div[@class='std_score']/div[@class='score_wrap']/span[2]/text()")
        if len(product_score) != 1 or product_score[0] == 'tbd':
            data['score'] = -1
            print product_score
        else:
            data['score'] = int(product_score[0])
            print product_score

        data['type'] = type
        scraperwiki.sqlite.save(unique_keys=['title', 'url'], data=data)
