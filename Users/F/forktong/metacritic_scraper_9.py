# Metacritic Scraper
import scraperwiki
import lxml.html
import re

types = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14']
for type in types:
    url = "http://www.metacritic.com/browse/games/score/metascore/all/xbox360?view=detailed&page=%s" % type
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    products = root.xpath("//ol[@class='list_products list_product_summaries']/li")
    for product in products:
        data = {}
        data['title'] = str(product.xpath("div/div/div/div/div/h3[@class='product_title']/a/text()")[0])

        product_release = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat release_date']/span[@class='data']/text()")
        if len(product_release) != 1:
            data['release'] = -1
        else:
            data['release'] = str(product_release[0])

        user_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat product_avguserscore']/span[@class='data textscore textscore_mixed']/text()")
        if len(user_score) != 1 or user_score[0] == 'tbd':
            user_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat product_avguserscore']/span[@class='data textscore textscore_favorable']/text()")
            if len(user_score) != 1 or user_score[0] == 'tbd':
                user_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat product_avguserscore']/span[@class='data textscore textscore_outstanding']/text()")
                if len(user_score) != 1 or user_score[0] == 'tbd':
                    user_score = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat product_avguserscore']/span[@class='data textscore textscore_unfavorable']/text()")
                    if len(user_score) != 1 or user_score[0] == 'tbd':
                        data['userscore'] = -1
                    else:
                        data['userscore'] = str(user_score[0])
                else:
                    data['userscore'] = str(user_score[0])
            else:
                data['userscore'] = str(user_score[0])
        else:
            data['userscore'] = str(user_score[0])

        product_publisher = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat publisher']/span[@class='data']/text()")
        if len(product_publisher) != 1:
            data['publisher'] = -1
        else:
            data['publisher'] = str(product_publisher[0])

        product_score = product.xpath("/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[2]/div[2]/ol/li/div/div/div/div[2]/ul/li[5]/span[2]/text()")
        if len(product_score) != 1 or product_score[0] == 'tbd':
            data['score'] = -1
        else:
            data['score'] = int(product_score[0])

        data['type'] = type
        scraperwiki.datastore.save(unique_keys=['title','release','publisher','userscore','score'], data=data)
