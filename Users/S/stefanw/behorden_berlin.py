import scraperwiki
import lxml.html

BASE_URL = 'http://www.berlin.de/verwaltungsfuehrer/behoerde/all/'

html = scraperwiki.scrape(BASE_URL)
root = lxml.html.fromstring(html)

pbs = []

for li in root.cssselect("#bomain_content ul li"):
    pb = {'name': li.text_content().strip()}
    a = li.cssselect('a')
    if a:
        pb['href'] = a[0].attrib['href']
    pbs.append(pb)


def scrape_contact_form(pb, root):
    for a in root.cssselect('#containerbereich .container a'):
        if a.text_content().strip() == 'Kontaktformular':
            url = a.attrib['href']
            if url.startswith('/'):
                url = 'http://www.berlin.de' + url
            url = url.replace('rechtshinweis.html', 'kontaktformular.php') 
            html = scraperwiki.scrape(url)
            kontakt = lxml.html.fromstring(html)
            input = kontakt.cssselect('form.land_form input[name="form[recipient]"]')
            if input:
                pb['email'] = input[0].attrib['value']
            break
    return pb

    

def scrape_berlin(pb):
    html = scraperwiki.scrape(pb['href'])
    root = lxml.html.fromstring(html)
    for a in root.cssselect('#containerbereich .container a'):
        if not 'email' in pb and a.attrib['href'].startswith('mailto:'):
            pb['email'] = a.attrib['href'].split(':', 1)[1]
    if not 'email' in pb:
        pb = scrape_contact_form(pb, root)
    return pb

for pb in pbs:
    if 'href' in pb:
        if pb['href'].startswith('http://www.berlin.de/'):
            pb = scrape_berlin(pb)
    if 'email' in pb and pb['email'].startswith('%20'):
        pb['email'] = pb['email'].replace('%20', '')
    scraperwiki.sqlite.save(unique_keys=['name'], data=pb)
import scraperwiki
import lxml.html

BASE_URL = 'http://www.berlin.de/verwaltungsfuehrer/behoerde/all/'

html = scraperwiki.scrape(BASE_URL)
root = lxml.html.fromstring(html)

pbs = []

for li in root.cssselect("#bomain_content ul li"):
    pb = {'name': li.text_content().strip()}
    a = li.cssselect('a')
    if a:
        pb['href'] = a[0].attrib['href']
    pbs.append(pb)


def scrape_contact_form(pb, root):
    for a in root.cssselect('#containerbereich .container a'):
        if a.text_content().strip() == 'Kontaktformular':
            url = a.attrib['href']
            if url.startswith('/'):
                url = 'http://www.berlin.de' + url
            url = url.replace('rechtshinweis.html', 'kontaktformular.php') 
            html = scraperwiki.scrape(url)
            kontakt = lxml.html.fromstring(html)
            input = kontakt.cssselect('form.land_form input[name="form[recipient]"]')
            if input:
                pb['email'] = input[0].attrib['value']
            break
    return pb

    

def scrape_berlin(pb):
    html = scraperwiki.scrape(pb['href'])
    root = lxml.html.fromstring(html)
    for a in root.cssselect('#containerbereich .container a'):
        if not 'email' in pb and a.attrib['href'].startswith('mailto:'):
            pb['email'] = a.attrib['href'].split(':', 1)[1]
    if not 'email' in pb:
        pb = scrape_contact_form(pb, root)
    return pb

for pb in pbs:
    if 'href' in pb:
        if pb['href'].startswith('http://www.berlin.de/'):
            pb = scrape_berlin(pb)
    if 'email' in pb and pb['email'].startswith('%20'):
        pb['email'] = pb['email'].replace('%20', '')
    scraperwiki.sqlite.save(unique_keys=['name'], data=pb)
