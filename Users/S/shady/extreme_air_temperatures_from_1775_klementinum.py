import scraperwiki
import urllib, lxml.html

id = 1

months = range(1, 13)

for month in months:
    if len(str(month)) == 1:
        month = "0"+str(month)

    url = 'http://portal.chmi.cz/files/portal/docs/meteo/ok/extrklem'+str(month)+'_cs.html'

    f = urllib.urlopen(url)
    html = f.read()
    f.close()

    root = lxml.html.fromstring(html)
    tabulka = root.cssselect('table')[0]
    trs = tabulka.cssselect('tr')

    for tr in trs:
        tds = tr.cssselect('td')
        if len(tds) > 5:
            data = {
                'id' : id,
                'month' : month,
                'day' : tds[0].text_content(),
                'mean' : tds[1].text_content(),
                'maximum' : tds[2].text_content(),
                'maximum_year' : tds[3].text_content(),
                'minimum' : tds[4].text_content(),
                'minimum_year' : tds[5].text_content()
            }
            scraperwiki.sqlite.save(unique_keys=["id"], data=data, table_name="swdata") 
            id = id + 1
import scraperwiki
import urllib, lxml.html

id = 1

months = range(1, 13)

for month in months:
    if len(str(month)) == 1:
        month = "0"+str(month)

    url = 'http://portal.chmi.cz/files/portal/docs/meteo/ok/extrklem'+str(month)+'_cs.html'

    f = urllib.urlopen(url)
    html = f.read()
    f.close()

    root = lxml.html.fromstring(html)
    tabulka = root.cssselect('table')[0]
    trs = tabulka.cssselect('tr')

    for tr in trs:
        tds = tr.cssselect('td')
        if len(tds) > 5:
            data = {
                'id' : id,
                'month' : month,
                'day' : tds[0].text_content(),
                'mean' : tds[1].text_content(),
                'maximum' : tds[2].text_content(),
                'maximum_year' : tds[3].text_content(),
                'minimum' : tds[4].text_content(),
                'minimum_year' : tds[5].text_content()
            }
            scraperwiki.sqlite.save(unique_keys=["id"], data=data, table_name="swdata") 
            id = id + 1
