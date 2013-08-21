# Metacritic Scraper
import scraperwiki
import lxml.html
import re

platforms = ['pc','ps3','xbox360']
types = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
for platform in platforms:
    for type in types:
        url = "http://www.metacritic.com/browse/games/score/metascore/all/{0}?view=detailed&page={1}".format( platform, type )
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

            data['page'] = type
            data['platform'] = platform
        
        #product_score = product.xpath("div/div/div/a[@class='basic_stat product_score']/div[@class='std_score']/div[@class='score_wrap']/span[@class='data metascore score_mixed']/text()")
        #product_score = product.xpath("div/div/div/div/a[@class='basic_stat product_score']/div[@class='std_score']/div[@class='score_wrap']/span[@class='data metascore score_outstanding']/text()")
        #data['score'] = product_score

            scraperwiki.sqlite.save(unique_keys=['title','release','publisher','score','page'], data=data)