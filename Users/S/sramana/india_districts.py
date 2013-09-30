"""List of districts in India
"""

import scraperwiki
import lxml.html

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['state', 'district']
base_url = 'http://india.gov.in/knowindia/'


def get_states():
    url = base_url + 'districts.php'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    assert 'stateid' in html
    links = root.cssselect('a[href*=stateid]') # States have stateid in href
    return [base_url + link.get('href') for link in links]


@utils.cache
def get_districts(state):
    html = scraperwiki.scrape(state)
    root = lxml.html.fromstring(html)
    state_name = root.cssselect('h1')[0].text_content()
    rows = root.cssselect('table.districts tr')
    del rows[0] # Header
    for row in rows:
        rec = dict()
        for elem in row.cssselect('span.hidethis'):
            elem.getparent().remove(elem)
        cells = [td.text_content() for td in row.cssselect('td')]

        rec['state'] = state_name
        rec['district'] = cells[1].replace('*', '')
        rec['area_in_sqkm'] = cells[2].replace(',', '')
        rec['population'] = cells[3].replace(',', '')
        rec['headquarters'] = cells[4]

        if row.cssselect('a'):
            rec['official_website'] = row.cssselect('a')[0].get('href').split('id=')[-1]

        utils.save(rec)



@utils.clear_cache
def main():
    states = get_states()
    for state in states:
        get_districts(state)


main()
"""List of districts in India
"""

import scraperwiki
import lxml.html

utils = scraperwiki.utils.swimport("utils")
utils.save.unique_keys = ['state', 'district']
base_url = 'http://india.gov.in/knowindia/'


def get_states():
    url = base_url + 'districts.php'
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    assert 'stateid' in html
    links = root.cssselect('a[href*=stateid]') # States have stateid in href
    return [base_url + link.get('href') for link in links]


@utils.cache
def get_districts(state):
    html = scraperwiki.scrape(state)
    root = lxml.html.fromstring(html)
    state_name = root.cssselect('h1')[0].text_content()
    rows = root.cssselect('table.districts tr')
    del rows[0] # Header
    for row in rows:
        rec = dict()
        for elem in row.cssselect('span.hidethis'):
            elem.getparent().remove(elem)
        cells = [td.text_content() for td in row.cssselect('td')]

        rec['state'] = state_name
        rec['district'] = cells[1].replace('*', '')
        rec['area_in_sqkm'] = cells[2].replace(',', '')
        rec['population'] = cells[3].replace(',', '')
        rec['headquarters'] = cells[4]

        if row.cssselect('a'):
            rec['official_website'] = row.cssselect('a')[0].get('href').split('id=')[-1]

        utils.save(rec)



@utils.clear_cache
def main():
    states = get_states()
    for state in states:
        get_districts(state)


main()
