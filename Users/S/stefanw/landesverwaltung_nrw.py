import scraperwiki
import lxml.html as lh
import urllib


BASE_URL = u'http://www.service.nrw.de/Behoerdenverzeichnis/'
LIST_URL = BASE_URL + u'csvlesen.php?param=%s'

letters = '''A  B  C  D  E  F  G  H  I  J  K  L  M  
O  P  Q  R  S  T  U  V  W  X  Y  Z'''.split()


publicbodies = []

for letter in letters:
    content = scraperwiki.scrape(LIST_URL % letter)
    content = content.decode('utf-8')
    doc = lh.fromstring(content)
    for link in doc.cssselect('ul li a[href*="behoerdedetail.php"]'):
        url = link.attrib['href']
        url = url.encode('utf-8')
        url = urllib.quote(url, '?=/&')
        print repr(link.text_content())
        name = link.text_content().strip()
        publicbodies.append({'url': BASE_URL + url, 'name': unicode(name) })

for pb in publicbodies:
    pb['web'] = None
    pb['email'] = None
    pb['kontakt'] = None
    pb['address'] = None
    print pb['name'], pb['url']
    content = scraperwiki.scrape(pb['url'])
    content = content.decode('utf-8')
    doc = lh.fromstring(content)
    kontakt = doc.cssselect('.kontaktdaten')
    if not kontakt:
        print "!!!Skipping %s" % pb['name']
        continue
    kontakt = kontakt[0]
    anschrift = kontakt.cssselect('.anschrift')
    if anschrift:
        pb['address'] = u'\n'.join([a.tail.strip() for a in anschrift[0] if a.tail is not None])
    kontakt = kontakt.cssselect('.kontakt')
    if kontakt:
        kontakt = kontakt[0]
        pb['kontakt'] = u'\n'.join([a.tail.strip() for a in kontakt if a.tail is not None and not a.tail.strip() in ('E-Mail:', 'Internet:')])
        email = kontakt.cssselect('a[href*="mailto"]')
        if email:
            pb['email'] = email[0].attrib['href'][len('mailto:'):]
        web = kontakt.cssselect('a[href*="http"]')
        if web:
            pb['web'] = web[0].attrib['href']
    print "saving", pb
    scraperwiki.sqlite.save(['url'], pb, table_name='nrw_publicbody')