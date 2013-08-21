import scraperwiki
import lxml.html
import re
import json


SITE_ROOT = 'http://www.camera.it/'

LEGISLATION = 'leg17/28'

NBSP = '\xc2\xa0'


def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2) + 1):
        yield chr(c)


def scrape_deputee_details(deputee_page_url):
    deputee_page_html = scraperwiki.scrape(deputee_page_url)
    deputee_page_dom = lxml.html.fromstring(deputee_page_html)
    bio = deputee_page_dom.cssselect('div[class="datibiografici"]')[0].text_content().strip().encode('utf-8')
    bio = map(lambda x: x.strip().replace(NBSP, ''), bio.split('\n'))
    elective_data = deputee_page_dom.cssselect('div[class="datielettoriali"]')[0].text_content().strip().encode('utf-8')
    image = deputee_page_dom.cssselect('img[class="fotoDep"]')[0].get('src')
    return {'bio' : json.dumps(bio), 'elective_data' : elective_data, 'image' : image}


def scrape_deputees_by_letter(letter):
    list_url = SITE_ROOT + LEGISLATION + '?lettera=%s' % letter
    list_html = scraperwiki.scrape(list_url)
    list_dom = lxml.html.fromstring(list_html)
    list_elems = list_dom.cssselect('li[class="list_wrapper"]')
    for list_elem in list_elems:
        name_node = list_elem.cssselect('div[class="fn"] a')[0]
        deputee_details_page_url = name_node.get('href')
        deputee_id = re.match('.*&idPersona=([\d]+)', deputee_details_page_url).groups()[0]
        deputee_fullname = name_node.text_content().strip().encode('utf-8')
        deputee_surname, deputee_name = deputee_fullname.split(NBSP) 
        deputee_email = None
        try: 
            deputee_email = list_elem.cssselect('div[class="email"] a')[0].get('href').split('&email=')[-1]
        except: pass
        
        deputee_details = scrape_deputee_details(deputee_details_page_url)
        record = { 'id' : deputee_id, 'name' : deputee_name, 'surname' : deputee_surname, 'url' : deputee_details_page_url, 'email' : deputee_email }
        record.update(deputee_details)
        print repr(record)
        scraperwiki.sqlite.save(table_name='data', unique_keys=['url'], data=record)


def scrape_deputees():
    for letter in char_range('A', 'Z'):
        scrape_deputees_by_letter(letter)


scrape_deputees()