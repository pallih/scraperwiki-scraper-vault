import json
import requests
import lxml.html

import scraperwiki

base_url = 'http://www.1pengguna.com/11pengguna/'

def get_options(page, cssid):
    select_options = page.cssselect(cssid)
    options = []
    for count, option in enumerate(select_options):
        if count == 0:
            continue
        options.append([option.values()[0], option.text_content()])

    return options

def get_kawasan(kod_negeri):
    params = "neg=" + kod_negeri
    url = base_url + 'index.php?pg=mysearch/ajax_kawasan&hd=0&' + params
    #print "\t", url
    resp = requests.get(url)
    page = lxml.html.fromstring(resp.content)
    kawasan_options = get_options(page, '#KodKawasan > option')
    kawasan = []
    for option in kawasan_options:
        kawasan.append([option[0], option[1]])
    return kawasan

html = requests.get(base_url).content
page = lxml.html.fromstring(html)

select_options = get_options(page, '#negeri > option')
for count, option in enumerate(select_options):
    kod_negeri = option[0]
    nama_negeri = option[1]
    kawasan = get_kawasan(kod_negeri)

    for kaw in kawasan:
        data = {
            'kod_negeri': kod_negeri,
            'nama_negeri': nama_negeri,
            'kod_kawasan': kaw[0],
            'nama_kawasan': kaw[1],
        }
        scraperwiki.sqlite.save(unique_keys=['kod_negeri', 'kod_kawasan'], data=data)