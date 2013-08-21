import scraperwiki
import lxml.html as lh
from lxml import etree


LIST_URL = 'http://www3.chamaeleon.de/komnav/kundensuchergebnis.php?Ort=&PLZ=%s&OBGM=&Bundesland=Nordrhein-Westfalen&anfrage=imnrw'
DETAIL_URL = 'http://www3.chamaeleon.de/komnav/kundensuchedetail.php?schluessel=%s&anfrage=imnrw&PLZ=%s&Ort=&Bundesland=Nordrhein-Westfalen&OBGM=&single_search='

def plz_generator():
    for i in (3,4,5):
        for j in range(10):
            yield "%s%s" % (i, j)



kommune = []

for plz in plz_generator():
    print plz
    content = scraperwiki.scrape(LIST_URL % plz)
    content = content.decode('latin1')
    if 'Leider keinen Datensatz gefunden' in content:
        continue
    doc = lh.fromstring(content)
    for row in doc.cssselect('tr'):
        td = row.cssselect('td')
        if not td:
            continue
        kommune.append({
            'name': td[0].text_content().strip(),
            'plz': td[1].text_content().strip(),
            'head': td[3].text_content().strip(),
            'key': td[4].cssselect('a')[0].attrib['href'].split('schluessel=')[1].split('&anfrage=')[0],
            'source': td[4].cssselect('a')[0].attrib['href']
        })

wanted = {
        u'': None,
        u'Stadt-/Gemeinde-/Kreisname': None,
        u'PLZ': None,
        u'Bundesland': None,
        u'Bev\xf6lkerungsdichte Einwohner pro km\xb2': None,
        u'(Ober-)b\xfcrgermeisterin/Landr\xe4tin/Oberkreisdirektorinbzw.(Ober-)b\xfcrgermeister/Landrat/Oberkreisdirektor': None,
        u'EMail': 'email',
        u'Postanschrift': 'address',
        u'Regierungsbezirk': 'gov_area',
        u'Fax': 'fax',
        u'Telefonzentrale': 'phone',
        u'Hausanschrift (Verwaltungssitz)': 'address2',
        u'PLZ-Hausanschrift': 'plz2',
        u'Ausl\xe4nderanteil (in %)': 'immigrant_percentage',
        u'EinwohnerInnen': 'population',
        u'davon weiblich/m\xe4nnlich (in %)': 'female_male_percentage',
        u'Fl\xe4che (in km\xb2)': 'area',
        u'Anzahl Besch\xe4ftigte': 'employees',
        u'Homepage der Kommune': 'url'
}

print repr(wanted.keys())

for kom in kommune:
    for v in wanted.values():
        if v is not None:
            kom[v] = None
    content = scraperwiki.scrape(DETAIL_URL % (kom['key'], kom['plz']))
    content = content.decode('latin1')
    doc = lh.fromstring(content)
    for row in doc.cssselect('tr'):
        td = row.cssselect('td')
        if not td:
            continue
        key = td[0].text_content().split(':')[0].strip()
        if wanted.get(key, None) is not None:
            kom[wanted[key]] = td[1].text_content().strip()
        elif key not in wanted:
            print repr(key)
    print repr(kom)
    scraperwiki.sqlite.save(['key'], kom, table_name='nrw_kommune')