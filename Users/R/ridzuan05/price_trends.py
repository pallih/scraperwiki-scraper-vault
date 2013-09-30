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
item_list = scraperwiki.sqlite.select("* from pricewatch_barang.swdata")
area_list = scraperwiki.sqlite.select("* from pricewatch_kawasan.swdata")

headers = {
    'Referer': base_url,
}

random_seconds = [1, 5, 10, 12, 11, 15]

for item in item_list[4:]:
    for area in area_list:
        data = {
            'KodBrg': item['kod_barang'],
            'negeri': area['kod_negeri'],
            'KodKawasan': area['kod_kawasan'],
        }
        url = base_url + 'index.php?pg=mysearch/result_search#content'

        try:
            resp = requests.post(url, data, headers=headers)
        except Exception as e:
            print e
            continue

        html = resp.content
        page = lxml.html.fromstring(html)
        table = page.cssselect('#content table')[0]
        product = {}
        product['kod_barang'] = item['kod_barang']
        product['kod_negeri'] = area['kod_negeri']
        product['kod_kawasan'] = area['kod_kawasan']
        for count, tr in enumerate(table.getchildren()):
            if count == 0:
                product['tarikh'] = tr.getchildren()[0].text.split(':')[-1].strip()
                continue
            if count == 1:
                product['nama'] = tr.getchildren()[0].text.split(':')[-1].strip()
                continue
            if count == 2:
                continue
            
            try:
                cat_img = tr.getchildren()[1].cssselect('img')[0].items()[0][1]
                cat = cat_img.split('/')[-1]
                premise = tr.getchildren()[2].text
                price = tr.getchildren()[4].text
                product['kategori'] = cat
                product['premis'] = premise
                product['harga'] = price
            except Exception as e:
                print e
                continue

            scraperwiki.sqlite.save(unique_keys=['kod_barang', 'kod_negeri', 'kod_kawasan', 'premis', 'tarikh'], data=product)
            print product
            second = random.choice(random_seconds)
            print 'Sleep %ds' % second
            #time.sleep(second)import scraperwiki

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
item_list = scraperwiki.sqlite.select("* from pricewatch_barang.swdata")
area_list = scraperwiki.sqlite.select("* from pricewatch_kawasan.swdata")

headers = {
    'Referer': base_url,
}

random_seconds = [1, 5, 10, 12, 11, 15]

for item in item_list[4:]:
    for area in area_list:
        data = {
            'KodBrg': item['kod_barang'],
            'negeri': area['kod_negeri'],
            'KodKawasan': area['kod_kawasan'],
        }
        url = base_url + 'index.php?pg=mysearch/result_search#content'

        try:
            resp = requests.post(url, data, headers=headers)
        except Exception as e:
            print e
            continue

        html = resp.content
        page = lxml.html.fromstring(html)
        table = page.cssselect('#content table')[0]
        product = {}
        product['kod_barang'] = item['kod_barang']
        product['kod_negeri'] = area['kod_negeri']
        product['kod_kawasan'] = area['kod_kawasan']
        for count, tr in enumerate(table.getchildren()):
            if count == 0:
                product['tarikh'] = tr.getchildren()[0].text.split(':')[-1].strip()
                continue
            if count == 1:
                product['nama'] = tr.getchildren()[0].text.split(':')[-1].strip()
                continue
            if count == 2:
                continue
            
            try:
                cat_img = tr.getchildren()[1].cssselect('img')[0].items()[0][1]
                cat = cat_img.split('/')[-1]
                premise = tr.getchildren()[2].text
                price = tr.getchildren()[4].text
                product['kategori'] = cat
                product['premis'] = premise
                product['harga'] = price
            except Exception as e:
                print e
                continue

            scraperwiki.sqlite.save(unique_keys=['kod_barang', 'kod_negeri', 'kod_kawasan', 'premis', 'tarikh'], data=product)
            print product
            second = random.choice(random_seconds)
            print 'Sleep %ds' % second
            #time.sleep(second)