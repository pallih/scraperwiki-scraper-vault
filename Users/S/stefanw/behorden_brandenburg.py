import scraperwiki
import lxml.html as lh
import urllib


BASE_URL = u'http://service.brandenburg.de'
LIST_URL = u'http://service.brandenburg.de/lis/list.php?page=behoerdenverzeichnis_art&sv[adr_art]=lb_*&_grid=Landesbeh%C3%B6rden'

content = scraperwiki.scrape(LIST_URL)
content = content.decode('utf-8')
doc = lh.fromstring(content)

publicbodies = []

for link in doc.cssselect('.einruecken li a'):
    url = link.attrib['href'].strip()
    name = link.text_content().strip()
    name = unicode(name).replace('  ', ' ')
    publicbodies.append({'url': BASE_URL + url, 'name': name})

whitelist = ['E-Mail', 'Internet', 'Telefon', 'Telefax']

for pb in publicbodies:
    content = scraperwiki.scrape(pb['url'])
    content = content.decode('utf-8')
    doc = lh.fromstring(content)
    base = doc.cssselect('.einruecken')[0]
    address = u'\n'.join([t.text_content() for t in base.cssselect('p') if not 'zuletzt aktualisiert' in t.text_content()]).strip()
    infos = {'address': address, 'parent': None}
    for li in base.cssselect('ul li'):
        t = li.text_content()
        if ':' not in t:
            continue
        parts = [x.strip() for x in t.split(':', 1)]
        if parts[0] not in whitelist:
            continue
        infos[parts[0]] = parts[1]
    h4s = base.cssselect('h4')
    if len(h4s) > 1 and h4s[1].text_content().strip() == u'\xfcbergeordnet:':
        parent = base.cssselect('ul')[-1]
        parent = parent.cssselect('li a')[0].attrib['href']
        infos['parent'] = BASE_URL + parent.strip()
    pb.update(infos)
    print pb
    scraperwiki.sqlite.save(['url'], pb, table_name='brandenburg_publicbody')
    