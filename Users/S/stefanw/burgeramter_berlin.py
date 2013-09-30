import scraperwiki
import lxml.html
import json

BASE = 'http://service.berlin.de'
INDEX = '/standorte/'

standorte = []

html = scraperwiki.scrape(BASE + INDEX)
root = lxml.html.fromstring(html.decode('utf-8'))
for li in root.cssselect("ul.list li .row"):
    div = li.cssselect('>div')
    if len(div) > 1:
        standort = div[0].text_content().strip()
        a = div[1].cssselect('a')[0]
    else:
        standort = None
        a = div[0].cssselect('a')[0]
        
    dienstleistung = a.text_content().strip()
    url = a.attrib['href']
    data = {
        'name': standort,
        'dienstleistung': dienstleistung,
        'url': url
    }
    standorte.append(data)

def get_text(root, selector):
    el = root.cssselect(selector)
    if not el:
        return
    return el[0].text_content().strip()

for standort in standorte:
    url = BASE + standort['url']
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html.decode('utf-8'))
    standort['street'] = get_text(root, '.strasse')
    standort['postcode'] = get_text(root, '.ort')
    services = []
    for li in root.cssselect('.link_dienstleistung'):
        a = li.cssselect('a')[0]
        services.append({
            'name': a.text_content().strip(),
            'url': a.attrib['href'],
            'note': get_text(li, '.zhinweise')
        })
    standort['services'] = json.dumps(services)
    scraperwiki.sqlite.save(unique_keys=['url'], data=standort)

import scraperwiki
import lxml.html
import json

BASE = 'http://service.berlin.de'
INDEX = '/standorte/'

standorte = []

html = scraperwiki.scrape(BASE + INDEX)
root = lxml.html.fromstring(html.decode('utf-8'))
for li in root.cssselect("ul.list li .row"):
    div = li.cssselect('>div')
    if len(div) > 1:
        standort = div[0].text_content().strip()
        a = div[1].cssselect('a')[0]
    else:
        standort = None
        a = div[0].cssselect('a')[0]
        
    dienstleistung = a.text_content().strip()
    url = a.attrib['href']
    data = {
        'name': standort,
        'dienstleistung': dienstleistung,
        'url': url
    }
    standorte.append(data)

def get_text(root, selector):
    el = root.cssselect(selector)
    if not el:
        return
    return el[0].text_content().strip()

for standort in standorte:
    url = BASE + standort['url']
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html.decode('utf-8'))
    standort['street'] = get_text(root, '.strasse')
    standort['postcode'] = get_text(root, '.ort')
    services = []
    for li in root.cssselect('.link_dienstleistung'):
        a = li.cssselect('a')[0]
        services.append({
            'name': a.text_content().strip(),
            'url': a.attrib['href'],
            'note': get_text(li, '.zhinweise')
        })
    standort['services'] = json.dumps(services)
    scraperwiki.sqlite.save(unique_keys=['url'], data=standort)

