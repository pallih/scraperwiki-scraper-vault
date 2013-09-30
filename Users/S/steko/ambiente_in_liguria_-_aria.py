import requests
from lxml.html import fromstring
import scraperwiki

# Retrieve air pollution data from Regione Liguria
#
# The steps are as follows
# 1. choose a year
# 2. get a list of all polluting agents available for that year
# 3. get a list of all monitoring stations for each polluting agent (sensors)
# 4. retrieve data for all combinations of sensors and stations
# 5. parse data (a very simple tabular format)
# 6. store data

# This is the only endpoint to query for all:
# - list of monitoring stations
# - list of sensors available at each station (varies from year to year)
# - actual data


def query_sensors(year):

    table = []

    url0 = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAria11.asp?Tipo=CinqueAnni'
    s = requests.session()
    r = s.get(url0)

    url1 = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAria13.asp'
    payload1 = {
        'Anno': year,
        'Anni': year,
        'TipoTema': 'SENSORI',
        'CodTema': 'SENSORI',
        'Tipo': 'CinqueAnni',
        'TipoRete': 'T',
    }

    r = s.post(url1, data=payload1, headers={'Referer':url0})
    root = fromstring(r.text)
    select = root.find(".//select[@name='Param']")
    sensors = {}
    for o in select:
        code = o.get('value')
        desc = o.text_content()
        sensors[code] = desc
    request_id = root.find(".//input[@name='Id_Richiesta']").get('value')

    def sensor_payload(sensor_code, sensor_desc, request_id):
        payload2 = {
            'Anno': year,
            'CodParam': sensor_code,
            'SiglaParam': sensor_desc,
            'Azione': 'LISTA_STAZIONI',
            'CodTema': 'SENSORI',
            'Id_Richiesta': request_id,
        }
        return payload2

    url2 = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAria131.asp'

    for code, desc in sensors.items():
        # repeat insanely again to obtain a "fresh" request id
        r = s.post(url1, data=payload1, headers={'Referer':url0})
        root = fromstring(r.text)
        request_id = root.find(".//input[@name='Id_Richiesta']").get('value')
        # request id obtained, go on like a sane person would do
        r = s.get(url2, params=sensor_payload(code, desc, request_id), headers={'Referer': url1})
        root = fromstring(r.text)
        for tr in root.cssselect("table tr"):
            tds = tr.cssselect("td")
            if len(tds)==5:
                data = {
                    'postazione' : tds[0].text_content(),
                    'indirizzo' : tds[1].text_content(), # there is a <br> tag in the middle
                    'tipo_zona': tds[2].text_content(),
                    'tipo_stazione': tds[3].text_content(),
                    'sensor_desc': tds[4].text_content(),
                    'year': year,
                    'sensor_name': desc,
                    }
                ahref = tds[4].cssselect("a")
                if len(ahref)==1:
                    href = ahref[0].get('href')
                    hrefparams = href.split(",'")
                    data['postazione_code'] = hrefparams[1].strip("'")
                    data['sensor_code'] = hrefparams[3].strip("'")
                    data['azione'] = hrefparams[5].strip("';)")
                    table.append(data)
    scraperwiki.sqlite.save(["sensor_code", "year", "postazione_code"], table)


for y in range(2008,2013):
    query_sensors(y)import requests
from lxml.html import fromstring
import scraperwiki

# Retrieve air pollution data from Regione Liguria
#
# The steps are as follows
# 1. choose a year
# 2. get a list of all polluting agents available for that year
# 3. get a list of all monitoring stations for each polluting agent (sensors)
# 4. retrieve data for all combinations of sensors and stations
# 5. parse data (a very simple tabular format)
# 6. store data

# This is the only endpoint to query for all:
# - list of monitoring stations
# - list of sensors available at each station (varies from year to year)
# - actual data


def query_sensors(year):

    table = []

    url0 = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAria11.asp?Tipo=CinqueAnni'
    s = requests.session()
    r = s.get(url0)

    url1 = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAria13.asp'
    payload1 = {
        'Anno': year,
        'Anni': year,
        'TipoTema': 'SENSORI',
        'CodTema': 'SENSORI',
        'Tipo': 'CinqueAnni',
        'TipoRete': 'T',
    }

    r = s.post(url1, data=payload1, headers={'Referer':url0})
    root = fromstring(r.text)
    select = root.find(".//select[@name='Param']")
    sensors = {}
    for o in select:
        code = o.get('value')
        desc = o.text_content()
        sensors[code] = desc
    request_id = root.find(".//input[@name='Id_Richiesta']").get('value')

    def sensor_payload(sensor_code, sensor_desc, request_id):
        payload2 = {
            'Anno': year,
            'CodParam': sensor_code,
            'SiglaParam': sensor_desc,
            'Azione': 'LISTA_STAZIONI',
            'CodTema': 'SENSORI',
            'Id_Richiesta': request_id,
        }
        return payload2

    url2 = 'http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub2AccessoDatiAria131.asp'

    for code, desc in sensors.items():
        # repeat insanely again to obtain a "fresh" request id
        r = s.post(url1, data=payload1, headers={'Referer':url0})
        root = fromstring(r.text)
        request_id = root.find(".//input[@name='Id_Richiesta']").get('value')
        # request id obtained, go on like a sane person would do
        r = s.get(url2, params=sensor_payload(code, desc, request_id), headers={'Referer': url1})
        root = fromstring(r.text)
        for tr in root.cssselect("table tr"):
            tds = tr.cssselect("td")
            if len(tds)==5:
                data = {
                    'postazione' : tds[0].text_content(),
                    'indirizzo' : tds[1].text_content(), # there is a <br> tag in the middle
                    'tipo_zona': tds[2].text_content(),
                    'tipo_stazione': tds[3].text_content(),
                    'sensor_desc': tds[4].text_content(),
                    'year': year,
                    'sensor_name': desc,
                    }
                ahref = tds[4].cssselect("a")
                if len(ahref)==1:
                    href = ahref[0].get('href')
                    hrefparams = href.split(",'")
                    data['postazione_code'] = hrefparams[1].strip("'")
                    data['sensor_code'] = hrefparams[3].strip("'")
                    data['azione'] = hrefparams[5].strip("';)")
                    table.append(data)
    scraperwiki.sqlite.save(["sensor_code", "year", "postazione_code"], table)


for y in range(2008,2013):
    query_sensors(y)