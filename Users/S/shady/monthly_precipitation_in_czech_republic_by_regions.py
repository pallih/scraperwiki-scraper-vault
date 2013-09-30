import scraperwiki
import urllib, lxml.html, re

id = 1
region = ""
entity = ""
years = range(61, 100)
years2 = range(0, 14)
years.extend(years2)

for year in years:
    if len(str(year)) == 1:
        year = "0"+str(year)
    url = 'http://portal.chmi.cz/files/portal/docs/meteo/ok/uzs'+str(year)+'_cs.html'

    if int(year) < 61:
        year = "20"+str(year)
    else:
        year = "19"+str(year)

    f = urllib.urlopen(url)
    html = f.read()
    f.close()

    root = lxml.html.fromstring(html)
    tabulka = root.cssselect('table')[0]
    trs = tabulka.cssselect('tr')
    for tr in trs:
        i = 0
        tds = tr.cssselect('td')
        if len(tds) > 13:
            if re.sub('^(\s)+', '', tds[1].text_content()) == 'S':
                entity = "precipitation"
                region = tds[0].text_content()
                i = 1
            if tds[0].text_content() == 'N':
                entity = "normal"
            if tds[0].text_content() == '%':
                entity = "anomaly"
            data = {
                'id' : id,
                'region' : region,
                'year' : year,
                'entity' : entity,
                'january' : tds[1+i].text_content(),
                'february' : tds[2+i].text_content(),
                'march' :  tds[3+i].text_content(),
                'april' : tds[4+i].text_content(),
                'may' : tds[5+i].text_content(),
                'june' : tds[6+i].text_content(),
                'july' :  tds[7+i].text_content(),
                'august' : tds[8+i].text_content(),
                'september' : tds[9+i].text_content(),
                'october' : tds[10+i].text_content(),
                'november' :  tds[11+i].text_content(),
                'december' : tds[12+i].text_content()
            }
            scraperwiki.sqlite.save(unique_keys=["id"], data=data, table_name="swdata") 
            id = id + 1
import scraperwiki
import urllib, lxml.html, re

id = 1
region = ""
entity = ""
years = range(61, 100)
years2 = range(0, 14)
years.extend(years2)

for year in years:
    if len(str(year)) == 1:
        year = "0"+str(year)
    url = 'http://portal.chmi.cz/files/portal/docs/meteo/ok/uzs'+str(year)+'_cs.html'

    if int(year) < 61:
        year = "20"+str(year)
    else:
        year = "19"+str(year)

    f = urllib.urlopen(url)
    html = f.read()
    f.close()

    root = lxml.html.fromstring(html)
    tabulka = root.cssselect('table')[0]
    trs = tabulka.cssselect('tr')
    for tr in trs:
        i = 0
        tds = tr.cssselect('td')
        if len(tds) > 13:
            if re.sub('^(\s)+', '', tds[1].text_content()) == 'S':
                entity = "precipitation"
                region = tds[0].text_content()
                i = 1
            if tds[0].text_content() == 'N':
                entity = "normal"
            if tds[0].text_content() == '%':
                entity = "anomaly"
            data = {
                'id' : id,
                'region' : region,
                'year' : year,
                'entity' : entity,
                'january' : tds[1+i].text_content(),
                'february' : tds[2+i].text_content(),
                'march' :  tds[3+i].text_content(),
                'april' : tds[4+i].text_content(),
                'may' : tds[5+i].text_content(),
                'june' : tds[6+i].text_content(),
                'july' :  tds[7+i].text_content(),
                'august' : tds[8+i].text_content(),
                'september' : tds[9+i].text_content(),
                'october' : tds[10+i].text_content(),
                'november' :  tds[11+i].text_content(),
                'december' : tds[12+i].text_content()
            }
            scraperwiki.sqlite.save(unique_keys=["id"], data=data, table_name="swdata") 
            id = id + 1
