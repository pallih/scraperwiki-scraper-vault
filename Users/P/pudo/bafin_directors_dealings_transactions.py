import scraperwiki
import requests
import csv

MAPS = {
    '\xe4': 'ae',
    '\xfc': 'ue',
    '\xf6': 'oe',
    '-': '_',
    '/': '_',
    '.': '_'
    }

URL = "http://ww2.bafin.de/database/DealingsInfo/transaktionListe.do?d-8275856-e=1&6578706f7274=1&cmd=loadTransaktionenAction"
res = requests.get(URL)
reader = csv.DictReader(res.content.splitlines(), delimiter=';')     

for row in reader:
    out = {}
    for k, v in row.items():
        for ulk, ulv in MAPS.items():
            k = k.replace(ulk, ulv)
        k = k.strip('_')
        out[k] = v #.decode('utf-8')
    #print out
    scraperwiki.sqlite.save(unique_keys=['Meldungsnr', 'BaFin_ID'], data=out)
