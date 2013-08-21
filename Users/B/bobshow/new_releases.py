# Metacritic Scraper
import scraperwiki
import lxml.html
import re

platforms = ['pc','ps3','xbox360']
types = ['0','1']

for platform in platforms:
    for type in types:
        url = "http://www.metacritic.com/browse/games/release-date/coming-soon/{0}/date?hardware=all&view=detailed&page={1}".format( platform, type )
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

            product_publisher = product.xpath("div/div/div/div[@class='more_stats extended_stats']/ul[@class='more_stats']/li[@class='stat publisher']/span[@class='data']/text()")
            if len(product_publisher) != 1:
                data['publisher'] = -1
            else:
                data['publisher'] = str(product_publisher[0])

            product_score = product.xpath("div/div/div/div/a[@class='basic_stat product_score']/div[@class='std_score']/div[@class='score_wrap']/span[@class='data metascore score_mixed']/text()")
            if len(product_score ) != 1 or product_score [0] == 'tbd':
                product_score = product.xpath("div/div/div/div/a[@class='basic_stat product_score']/div[@class='std_score']/div[@class='score_wrap']/span[@class='data metascore score_favorable']/text()")
                if len(product_score ) != 1 or product_score [0] == 'tbd':
                    product_score = product.xpath("div/div/div/div/a[@class='basic_stat product_score']/div[@class='std_score']/div[@class='score_wrap']/span[@class='data metascore score_outstanding']/text()")
                    if len(product_score ) != 1 or product_score [0] == 'tbd':
                        product_score = product.xpath("div/div/div/div/a[@class='basic_stat product_score']/div[@class='std_score']/div[@class='score_wrap']/span[@class='data metascore score_unfavorable']/text()")
                        if len(product_score ) != 1 or product_score [0] == 'tbd':
                            data['score'] = -1
                        else:
                            data['score'] = str(product_score [0])
                    else:
                        data['score'] = str(product_score [0])
                else:
                    data['score'] = str(product_score [0])
            else:
                data['score'] = str(product_score [0])

            data['platform'] = platform

            scraperwiki.sqlite.save(unique_keys=['title','release','publisher','score'], data=data)

