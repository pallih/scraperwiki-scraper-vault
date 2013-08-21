import re
import datetime

import scraperwiki
import lxml.html


URL = 'http://www.verkehr-data.com/docs/artikelsuche.php?seitenzahl=1&anzahl=10000&start=0&Titel=&Datum=&Muster=&Muster2=&Jahrgang=%d&VerordnungsNr=&Seite=&Bereichsname=&DB=&Aktenzeichen='

current_year = datetime.datetime.now().year

def ctext(el):
    result = []
    if el.text:
        result.append(el.text)
    for sel in el:
        if sel.tag in ["br"]:
            result.append(ctext(sel))
            result.append('\n')
        else:
            result.append(ctext(sel))
        if sel.tail:
            result.append(sel.tail)
    return "".join(result)


price_re = re.compile('Preis: (\d+,\d+) \((\d+) Seite')
slugify_re = re.compile('[^a-z]')

def slugify(key):
    return slugify_re.sub('', key.lower())


for year in range(1947, current_year + 1):
    html = scraperwiki.scrape(URL % year)
    root = lxml.html.fromstring(html)
    print year, len(root.cssselect(".tabelle2"))
    for i, table in enumerate(root.cssselect(".tabelle2")):
        trs = table.cssselect('tr')
        header = trs[0].cssselect('td')[0].text_content().strip()
        print i, header
        genre, edition = header.split(u'\xa0 ')
        edition = edition.split(' ')[2]
        title = ctext(trs[1].cssselect('td')[0]).replace('Titel:', '').strip().splitlines()
        title = [t.strip() for t in title if t.strip()]
        title, description = title[0], '\n'.join(title[1:])
        extra = {}
        for tr in trs[2:]:
            tds = tr.cssselect('td')
            if len(tds) == 2:
                key = tds[0].text_content().replace(':', '').strip()
                value = tds[1].text_content().strip()
                extra[slugify(key)] = value
            elif len(tds) == 1:
                if tds[0].cssselect('img[src="../images/orange.gif"]'):
                    extra['link'] = tds[0].cssselect('a')[0].attrib['href']
                    extra['vid'] = extra['link'].split('=')[-1]
                    match = price_re.search(tds[0].text_content())
                    extra['price'] = float(match.group(1).replace(',', '.'))
                    extra['pages'] = int(match.group(2))
        data = dict(extra)
        data.update({
            'genre': genre,
            'edition': edition,
            'title': title,
            'description': description
        })
        scraperwiki.sqlite.save(unique_keys=['aktenzeichen'], data=data)
