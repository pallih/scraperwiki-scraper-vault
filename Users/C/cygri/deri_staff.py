import scraperwiki
import lxml.html
import re

def get_memberpages(url):
    root = lxml.html.fromstring(scraperwiki.scrape(url))
    root.make_links_absolute(url)
    memberpages = []
    for link in root.cssselect(".memberitemrightsmall a"):
        memberpages.append(link.get("href"))
    return memberpages

def get_positions(div):
    position = div.text.strip()
    i = 0
    while div[i].tag == 'br':
        if div[i].tail:
            position += ' ' + div[i].tail
        i += 1
    return position.strip().rsplit(' & ')

def get_details(url):
    root = lxml.html.fromstring(scraperwiki.scrape(url))
    root.make_links_absolute(url)
    details = {}
    details['url'] = url
    details['id'] = re.search('([^/]*)/$', url).group(1)
    details['given'] = root.cssselect('span[property="foaf:givenname"]')[0].text_content()
    details['family'] = root.cssselect("span[property='foaf:familyName']")[0].text_content()
    details['title'] = root.cssselect("span[property='foaf:title']")[0].text_content() or None
    details['name'] = details['given'] + ' ' + details['family']
    details['image'] = root.cssselect('#memberitemleft img')[0].get('src')
    if details['image'].endswith('nophoto.jpg'):
        details['image'] = None
    div = root.cssselect('#memberitemright')[0]
    positions = get_positions(div)
    details['position1'] = positions[0] if len(positions) > 0 else None
    details['position2'] = positions[1] if len(positions) > 1 else None
    details['position3'] = positions[2] if len(positions) > 2 else None
    try:
        details['phone'] = div.cssselect('acronym[title="Phone"]')[0].tail.strip().replace(' ', '-')
    except IndexError:
        details['phone'] = None
    try:
        details['fax'] = div.cssselect('acronym[title="Fax"]')[0].tail.strip().replace(' ', '-')
    except IndexError:
        details['fax'] = None
    try:
        details['email'] = div.cssselect('a')[0].text + '@deri.org'
    except IndexError:
        details['email'] = None
    try:
        details['homepage'] = div.cssselect('a')[1].get('href')
    except IndexError:
        details['homepage'] = None
    try:
        unit = re.match('(.*) \((.*)\)', root.cssselect('.memberclusters a')[0].text_content().replace('  ', ' '))
        details['unit'] = unit.group(1)
        details['unit_code'] = unit.group(2)
    except IndexError:
        details['unit'] = None
        details['unit_code'] = None
    return details

#print get_details('http://www.deri.ie/about/team/member/manfred_hauswirth/')

url = 'http://www.deri.ie/about/team/'
memberpages = get_memberpages(url)
for page in memberpages:
    details = get_details(page)
    scraperwiki.sqlite.save(['id'], details, 'team')
