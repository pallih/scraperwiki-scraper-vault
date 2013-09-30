import scraperwiki
import urllib, lxml.html

url = 'http://portal.chmi.cz/files/portal/docs/meteo/ok/mesicni_data/mdata_aktual_cs.html'

f = urllib.urlopen(url)
html = f.read()
f.close()

root = lxml.html.fromstring(html)
tabulka = root.cssselect('table')[0]

trs = tabulka.cssselect('tr')
ths = tabulka.cssselect('th')

table = ["avg_temperature", "rainfall", "sunlight"]
table_name = table[0]

for tr in trs:
    th = tr.cssselect('th')
    if len(th) > 0:
        if th[0].text == u'sr\xe1\u017eky [mm]':
            table_name = table[1]
        if th[0].text == u'trv\xe1n\xed slune\u010dn\xedho svitu [h]':
            table_name = table[2]

    tds = tr.cssselect('td')
    if ( len(tds) == 14 ):
        location = tds[0].text.rstrip()
        key = location.encode("ascii", "ignore")
        data = {
            'unique_id' : key,
            'location' : location,
            'january' : tds[1].text.rstrip(),
            'february' : tds[2].text.rstrip(),
            'march' :  tds[3].text.rstrip(),
            'april' : tds[4].text.rstrip(),
            'may' : tds[5].text.rstrip(),
            'june' : tds[6].text.rstrip(),
            'july' :  tds[7].text.rstrip(),
            'august' : tds[8].text.rstrip(),
            'september' : tds[9].text.rstrip(),
            'october' : tds[10].text.rstrip(),
            'november' :  tds[11].text.rstrip(),
            'december' : tds[12].text.rstrip()
        }
        print data
        scraperwiki.sqlite.save(unique_keys=["unique_id"], data=data, table_name=table_name)

import scraperwiki
import urllib, lxml.html

url = 'http://portal.chmi.cz/files/portal/docs/meteo/ok/mesicni_data/mdata_aktual_cs.html'

f = urllib.urlopen(url)
html = f.read()
f.close()

root = lxml.html.fromstring(html)
tabulka = root.cssselect('table')[0]

trs = tabulka.cssselect('tr')
ths = tabulka.cssselect('th')

table = ["avg_temperature", "rainfall", "sunlight"]
table_name = table[0]

for tr in trs:
    th = tr.cssselect('th')
    if len(th) > 0:
        if th[0].text == u'sr\xe1\u017eky [mm]':
            table_name = table[1]
        if th[0].text == u'trv\xe1n\xed slune\u010dn\xedho svitu [h]':
            table_name = table[2]

    tds = tr.cssselect('td')
    if ( len(tds) == 14 ):
        location = tds[0].text.rstrip()
        key = location.encode("ascii", "ignore")
        data = {
            'unique_id' : key,
            'location' : location,
            'january' : tds[1].text.rstrip(),
            'february' : tds[2].text.rstrip(),
            'march' :  tds[3].text.rstrip(),
            'april' : tds[4].text.rstrip(),
            'may' : tds[5].text.rstrip(),
            'june' : tds[6].text.rstrip(),
            'july' :  tds[7].text.rstrip(),
            'august' : tds[8].text.rstrip(),
            'september' : tds[9].text.rstrip(),
            'october' : tds[10].text.rstrip(),
            'november' :  tds[11].text.rstrip(),
            'december' : tds[12].text.rstrip()
        }
        print data
        scraperwiki.sqlite.save(unique_keys=["unique_id"], data=data, table_name=table_name)

