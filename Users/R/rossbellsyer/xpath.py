import scraperwiki
import lxml.html


# Pull restaurant reviews from menus.co.nz

url = "http://www.menus.co.nz/?f=New+Zealand"

html = scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)
root = lxml.html.etree.HTML(html)

#restaurants = root.xpath("//div[@class='listing']//a//text()")
restaurants = root.xpath("//ul[@class='categories']/text()")
print restaurants

#for restaurant in restaurants:
         
        #name = restaurant.xpath("//a[@class='bizname_link']/text()")
        #print name

        #adr = restaurant.xpath("//div[@class='adr'])/text()")
        #print adr.tail

        #product_score = restaurants.xpath("div/div/div/div/div/div[@class='std_score']/div[@class='score_wrap']/span[2]/text()")
        #if len(product_score) != 1 or product_score[0] == 'tbd':
        #    data['score'] = -1
        #    print product_score
        #else:
        #    data['score'] = int(product_score[0])
        #    print product_score

        #data['type'] = type

        #data = {"name": name}

        #scraperwiki.sqlite.save(unique_keys=['name'], data=data)
        #scraperwiki.sqlite.save(["name"], data)


