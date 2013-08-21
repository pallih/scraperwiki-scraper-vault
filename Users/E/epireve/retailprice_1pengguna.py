import scraperwiki

import time
import json
import random
import lxml.html
import requests

scraperwiki.sqlite.attach("pricewatch_kawasan")
scraperwiki.sqlite.attach("pricewatch_barang")

base_url = 'http://www.1pengguna.com/11pengguna/'

#item_list = json.loads(open('pricewatch_barang.json').read())
#area_list = json.loads(open('pricewatch_kawasan.json').read())
item_list = scraperwiki.sqlite.select("* from pricewatch_barang.swdata order by random() limit 50")
area_list = scraperwiki.sqlite.select("* from pricewatch_kawasan.swdata order by random() limit 50")

headers = {
    'Referer': base_url,
}

random_seconds = [1, 5, 10, 12, 11, 15]

for item in item_list[4:]:
    for area in area_list:
        data = {
            'KodBrg': item['item_code'],
            'negeri': area['state_code'],
            'KodKawasan': area['area_code'],
        }
        url = base_url + 'index.php?pg=mysearch/result_search#content'

        try:
            resp = requests.post(url, data, headers=headers)
        except Exception as e:
            print e
            continue

        html = resp.content
        page = lxml.html.fromstring(html)
        table = page.cssselect('#content > table')[0]
        product = {}
        product['item_code'] = item['kod_barang']
        product['state_code'] = area['kod_negeri']
        product['area_code'] = area['kod_kawasan']
        for count, tr in enumerate(table.getchildren()):
            if count == 0:
                product['date'] = tr.getchildren()[0].text.split(':')[-1].strip()
                continue
            if count == 1:
                product['name'] = tr.getchildren()[0].text.split(':')[-1].strip()
                continue
            if count == 2:
                continue
            
            try:
                cat_img = tr.getchildren()[1].cssselect('img')[0].items()[0][1]
                cat = cat_img.split('/')[-1]
                premise = tr.getchildren()[2].text
                price = tr.getchildren()[4].text
                product['kategori'] = cat
                product['premise'] = premise
                product['price'] = price
            except Exception as e:
                print e
                continue

            scraperwiki.sqlite.save(unique_keys=['item_code', 'state_code', 'area_code', 'premise', 'date'], data=product)
            print product
            second = random.choice(random_seconds)
            print 'Sleep %ds' % second
            #time.sleep(second)