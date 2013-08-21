import scraperwiki
import lxml.html
import re

INDEX_URL = 'http://www.vfa.de/de/arzneimittel-forschung/datenbanken-zu-arzneimitteln/nisdb?unternehmen=-1&sucheUnternehmen=&indikation=-1&sucheIndikationen=-+Geben+Sie+die+Anfangsbuchstaben+ein+-&volltext=&volltextRadio=1&statusRadio=1&studienSuchen=Studien+suchen'

html = scraperwiki.scrape(INDEX_URL)
root = lxml.html.fromstring(html)

studies = []
found = False

for div in root.cssselect(".large-copy"):
    content = div.text_content().strip()
    if content == 'Suchergebnisse als Exceldatei exportieren':
        found = True
        continue
    if not found:
        continue
    if content == 'Einige Arzneimittelhersteller registrieren nicht-interventionelle Studien nicht in dieser, sondern in anderen Datenbanken':
        break
    studies.append({'url': div.cssselect('a')[0].attrib['href']})

def make_key(s):
    return re.sub('\W', '', s)
    
def scrape_study(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html.decode('utf-8'))
    body = root.cssselect('.large-copy')[0]
    data = {}
    key = None
    value = None
    for child in body:
        if child.tag == 'b':
            if key is not None:
                if len(value) == 1:
                    data[key] = value[0]
                else:
                    data[key] = '\n'.join(value)
            key = make_key(child.text_content().strip())
            value = []
        if child.tag == 'ul':
            value.extend([s.text_content().strip() for s in child.cssselect('li')])
        if child.tail is not None and child.tail.strip():
            content = child.tail.strip()
            content = content.replace(u'•', '')
            content = content.strip()
            value.append(content)
    if len(value) == 1:
        data[key] = value[0]
    else:
        data[key] = '\n'.join(value)
    return data


for study in studies:
    study.update(scrape_study(study['url']))
    scraperwiki.sqlite.save(unique_keys=['url'], data=study)