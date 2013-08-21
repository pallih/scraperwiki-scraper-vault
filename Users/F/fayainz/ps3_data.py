# Metacritic PS3 Game Scraper
import scraperwiki
import lxml.html
import re

for page in range(0,12):
    url = "http://www.metacritic.com/browse/games/release-date/available/ps3/name?view=detailed&page=%s" % page
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    products = root.xpath("//ol[@class='list_products list_product_summaries']/li")
    for product in products:
        data = {}
        data['title'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/text()")[0])
        data['url'] = str(product.xpath("div/div/div/div[@class='main_stats']/div[@class='basic_stat product_title']/h3[@class='product_title']/a/@href")[0])

        product_release = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat release_date']/span[@class='data']/text()")
        if len(product_release) != 1:
            data['release'] = -1
        else:
            data['release'] = str(product_release[0])

        rating_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat maturity_rating']/span[@class='data']/text()")
        if len(rating_score) != 1:
            data['rating'] = -1
        else:
            data['rating'] = str(rating_score[0])

        genre_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat genre']/span[@class='data']/text()")
        if len(genre_score) != 1:
            data['genre'] = -1
        else:
            data['genre'] = str(genre_score[0])


        product_publisher = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat publisher']/span[@class='data']/text()")
        if len(product_publisher) != 1:
            data['publisher'] = -1
        else:
            data['publisher'] = str(product_publisher[0])

        scraperwiki.sqlite.save(unique_keys=['title','url','rating','release','genre','publisher'], data=data)