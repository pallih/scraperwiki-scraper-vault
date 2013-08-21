# -*- encoding: utf-8 -*-
import scraperwiki
import re
import time
import lxml.html

BASE_URL = 'http://www.buergerdienste-saar.de'

PATH = '/zfinder-saar-web/'

START = 'welcome'


def get_base_menu():
    html = scraperwiki.scrape(BASE_URL + PATH + START)
    root = lxml.html.fromstring(html)
    links = []
    for link in root.cssselect(".wegweiser li a"):
        links.append({'url': link.attrib['href'], 'category': link.text_content()})
    return links


def get_topic(name):
    name = name.lower()
    mapping = {
        'gericht': 'justiz',
        'polizei': 'inneres',
        'schul': 'bildung-und-forschung',
        'rechnungs': 'finanzen',
        'staatsanwaltschaft': 'justiz',
        'liegenschaftsbetrieb': 'verkehr-und-bau',
        'hrungshilfe': 'justiz',
        'finanzamt': 'finanzen',
        'hrungsaufsichtsstelle': 'justiz',
        'landwirtschaftskammer': 'landwirtschaft-und-verbraucherschutz',
        'jugendarrestanstalt': 'justiz',
        'justiz': 'justiz',
        'umwelt': 'umwelt',
        u'straßenbau': 'verkehr-und-bau',
        'wald': 'umwelt',
        'kriminal': 'inneres',
        u'prüfungsamt': 'bildung-und-forschung'
    }
    for k, v in mapping.items():
        if k in name:
            return v
    return ''


def get_classification(name):
    classifications = name.split()
    mapping = {
        'amt': 'Amt',
        'ministerium': 'Ministerium',
        'landkreis': 'Landkreis',
        'wesen': 'Amt'
    }
    for k, v in mapping.items():
        if k in name.lower():
            return v
    if classifications[0] == 'Der':
        classification = classifications[1]
    elif classifications[0].startswith('Staatl'):
        classification = u"Staatliches %s" % classifications[1]
    elif classifications[0].endswith('-'):
        classification = ' '.join(classifications[:3])
    else:
        classification = classifications[0]
    return classification


def scrape_public_body(root, url):

    url = re.sub(';jsessionid=[^\?]+\?', '?', url)
    url = re.sub('&menuitemid=\d+', '', url)
    kv = {}
    better_url = None
    box = root.cssselect('#box-1-1')
    if box:
        box = box[0]

        for h4 in box.cssselect('div.kontaktbox > h4'):
            h4_text = h4.text_content().strip()
            if h4_text == 'Hausanschrift' or h4_text == 'Postanschrift':
                div = h4.getnext()
                address_text = []
                while div is not None:
                    t = div.text_content().strip()
                    t = ' '.join([k.strip() for k in t.split() if k.strip()])
                    address_text.append(t)
                    div = div.getnext()
                kv[h4_text] = '\n'.join(address_text)

        for label, text in zip(box.cssselect('div > span.labeldescription'), box.cssselect('div > span.labeltext')):
            if text.cssselect('a[href^="http"]'):
                better_url = text.cssselect('a[href^="http"]')[0].attrib['href']
            label = label.text_content().replace(':', '').strip()
            if label in kv:
                continue
            kv[label] = '\n'.join([k.strip() for k in text.text_content().strip().splitlines()])

    contact = []
    if 'Telefon' in kv:
        contact.append(u'Tel.: %s' % kv['Telefon'])
    if 'Fax' in kv:
        contact.append(u'Fax: %s' % kv['Fax'])
    contact = '\n'.join(contact)

    if better_url is not None:
        url = better_url
    print url
    print kv
    name = root.cssselect('.content-area-prolog h1')[0].text_content().strip()
    email_elem = root.cssselect('.labeltext a[href^="mailto"]')
    email = ''
    if email_elem:
        email = email_elem[0].attrib['href'][len('mailto:'):]
    return {
        'name': name,
        'email': email,
        'url': url,
        "jurisdiction__slug": "saarland",
        "address": kv.get('Postanschrift', kv.get('Hausanschrift', '')),
        "contact": contact,
        "classification": get_classification(name),
        "other_names": "",
        "request_note": "",
        "website_dump": "",
        "description": '',
        "parent__name": "",
        "topic__slug": get_topic(name),
    }


def recursive_scrape(url, data):
    if url.startswith('/'):
        url = BASE_URL + url
    else:
        url = BASE_URL + PATH + url

    tries = 0
    while True:
        html = scraperwiki.scrape(url)
        if not 'Internal Error!' in html:
            break
        tries += 1
        print "Sleeping %d" % tries ** 2
        time.sleep(tries ** 2)
    root = lxml.html.fromstring(html)

    if 'authorityread' in url:
        print url
        try:
            elem = scrape_public_body(root, url)
            print elem
            if elem is not None:
                scraperwiki.sqlite.save(unique_keys=['name'], data=[elem])
        except Exception:
            print html
            raise
    else:
        for link in root.cssselect('.thema_leftside ul li a'):
            print link.attrib['href']
            recursive_scrape(link.attrib['href'], data)
        for link in root.cssselect('.thema_rightside ul li a'):
            print link.attrib['href']
            recursive_scrape(link.attrib['href'], data)


def main():
    menu_links = get_base_menu()
    data = []
    for menu_link in reversed(menu_links):
        recursive_scrape(menu_link['url'], data)


main()
