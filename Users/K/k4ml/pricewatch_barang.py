import scraperwiki

import json
import requests
import lxml.html

base_url = 'http://www.1pengguna.com/11pengguna/'

def get_options(page, cssid):
    select_options = page.cssselect(cssid)
    options = []
    for count, option in enumerate(select_options):
        if count == 0:
            continue
        options.append([option.values()[0], option.text_content()])

    return options

html = requests.get(base_url).content
#html = open('result.html').read()
page = lxml.html.fromstring(html)

select_options = get_options(page, '#KodBrg > option')
for count, option in enumerate(select_options):
    kod_barang = option[0]
    nama_barang = option[1]

    data = {
        'kod_barang': kod_barang,
        'nama_barang': nama_barang,
    }
    scraperwiki.sqlite.save(unique_keys=['kod_barang'], data=data)