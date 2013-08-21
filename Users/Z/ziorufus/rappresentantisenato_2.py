import scraperwiki
import lxml.html
import re
import json

SITE_ROOT = 'http://www.senato.it/'

LEGISLATION = 'leg/17'

NBSP = '\xc2\xa0'


def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2) + 1):
        yield chr(c)


def split_fullname(fullname):
    parts = fullname.split(' ')
    name = []
    index = -1
    for part in parts:
        if part != part.upper():
            name.append(part)
            index =+ 1
        else:
            break
    name_str = ' '.join(name)
    if len(parts) > 2: index = index + 1
    surname_str = ' '.join(parts[index:])
    return (name_str, surname_str)
        

def scrape_senator_details(page_url):
    page_html = scraperwiki.scrape(page_url)
    page_dom = lxml.html.fromstring(page_html)
    deputee_id = re.match('.*&id=([\d]+)', page_url).groups()[0]
    full_name = page_dom.cssselect('h1[class="titolo"]')[0].text_content().strip().encode('utf-8')
    bio = page_dom.cssselect('table[class="anagrafico"]')[0].text_content().strip().encode('utf-8')
    name, surname = split_fullname(full_name)
    bio = map(lambda x: x.strip(), bio.split('\n'))
    contacts = page_dom.cssselect('ul[class="composizione contatti"] a')
    contact_links = []
    for contact in contacts:
        contact_links.append(contact.get('href'))
    return { 'id' : deputee_id, 'name' : name, 'surname' : surname, 'bio' : json.dumps(bio), 'contact_links' : contact_links }


def scrape_senator_by_letter(letter):
    print 'Letter: ' + letter
    list_url = SITE_ROOT + LEGISLATION + '/BGT/Schede_v3/Attsen/Sen%s.html' % letter
    print 'URL: ' + list_url
    list_html = scraperwiki.scrape(list_url)
    print list_url + ' scraped'
    list_dom = lxml.html.fromstring(list_html)
    list_elems = list_dom.cssselect('ul[class="composizione"] li')
    for list_elem in list_elems:
        senator_details_page_url = SITE_ROOT + list_elem.cssselect('a')[0].get('href')
        senator_data = scrape_senator_details(senator_details_page_url)
        record = { 'url' : senator_details_page_url }
        record.update(senator_data)
        print repr(record)
        scraperwiki.sqlite.save(table_name='data', unique_keys=['url'], data=record)


def scrape_senators():
    for letter in char_range('a', 'z'):
        scrape_senator_by_letter(letter)


scrape_senators()