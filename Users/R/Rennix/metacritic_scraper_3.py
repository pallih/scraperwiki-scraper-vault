# Metacritic Scraper
import scraperwiki
import lxml.html
import re

types = ['0']
for type in types:
    url = "http://www.metacritic.com/browse/games/release-date/available/ps3/name?hardware=all&view=detailed&page=%s" % type
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

        product_image = product.xpath("div/div[@class='product_basics product_image small_image']/a/img[@class='product_image small_image']/a/@href")
        if len(product_image) != 1:
            data['image'] = -1
        else:
            data['image'] = str(product_image[0])        

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

        product_score = product.xpath("div/div/div/div/div/div[@class='std_score']/div[@class='score_wrap']/span[2]/text()")
        if len(product_score) != 1 or product_score[0] == 'tbd':
            data['score'] = -3
        else:
            data['score'] = int(product_score[0])

        product_userscore = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat product_avguserscore']/span[2]/text()")
        if len(product_userscore) != 1:
            data['user_score'] = -1
        else:
            data['user_score'] = str(product_userscore[0])

        data['type'] = type
        scraperwiki.sqlite.save(unique_keys=['title','image','url','rating','release','genre','publisher',], data=data)

        
        
        