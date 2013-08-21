import scraperwiki
import lxml.html
import json
import datetime

def load_page(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

coinabul_url = "http://coinabul.com/api.php"
coinabul_data = json.loads(scraperwiki.scrape(coinabul_url))

page = lxml.html.fromstring( \
    scraperwiki.scrape('http://coinabul.com/index.php/gold-coins-bitcoin/south-african-gold-krugerrand-coins-1/south-african-gold-krugerrand.html') \
)

gold_kugerand_btc = page.xpath('//*[@id="product-price-15"]/span')[0].text_content().encode('utf-8').replace('฿', '')
gold_kugerand_avail = page.xpath('//*[@id="product_addtocart_form"]/div[2]/p[3]/span')[0].text_content().encode('utf-8')

page = lxml.html.fromstring( \
    scraperwiki.scrape('http://coinabul.com/index.php/gold-coins-bitcoin/american-gold-eagle/american-eagle-gold-bullion.html') \
)

gold_eagle_btc = page.xpath('//*[@id="product-price-23"]/span')[0].text_content().encode('utf-8').replace('฿', '')
gold_eagle_avail = page.xpath('//*[@id="product_addtocart_form"]/div[2]/p[3]/span')[0].text_content().encode('utf-8')

page = lxml.html.fromstring( \
    scraperwiki.scrape('http://coinabul.com/silver/index.php/best-value/u-s-silver-eagle-1-ounce-coin.html') \
)

silver_eagle_btc = page.xpath('//*[@id="product-price-50"]/span')[0].text_content().encode('utf-8').replace('฿', '')
silver_eagle_avail = page.xpath('//*[@id="product_addtocart_form"]/div[2]/p[2]/span')[0].text_content().encode('utf-8')

data =  {
    'captured_on' : datetime.datetime.now(),

    'gold_usd' : coinabul_data['Gold']['USD'],
    'silver_usd' : coinabul_data['Silver']['USD'],

    'gold_btc' : coinabul_data['Gold']['Ounces'],
    'silver_btc' : coinabul_data['Silver']['Ounces'],

    'gold_kugerand_btc' : gold_kugerand_btc,
    'gold_kugerand_avail' : gold_kugerand_avail,

    'gold_eagle_btc' : gold_eagle_btc,
    'gold_eagle_avail' : gold_eagle_avail,

    'silver_eagle_btc' : silver_eagle_btc,
    'silver_eagle_avail' : silver_eagle_avail,
}

scraperwiki.sqlite.save(unique_keys=['captured_on'], data=data)