import json
import lxml.html
import HTMLParser
import re
import scraperwiki
import urllib2

INTERNATIONAL_PAT = re.compile(r'<dt>International: </dt><dd>(.*?)</dd>')
WHITESPACE_PAT = re.compile(r'\s+')
PRIMARY_DATA_KEYS = [ # uncomment keys to include
    'Fax',
    'Id',
    'Intro',
    'Name',
    'PostCode',
    'Staff',
    'StreetName',
    'Telephone',
    'Town',
    'Url',
    #'Established',
    #'RewrittenUrl',
    #'District',
    #'IsAffiliated',
    #'ImageOffice',
    #'Latitude',
    #'IsBuildingShare',
    #'ParentAgencyName',
    #'Vacancies',
    #'Joined',
    #'Longitude',
    #'ImageLogo',
    #'Letter',
    #'Offices',
    #'AddressSummary',
    #'BuildingShareCode',
    #'IsBranch',
]


def fetch(url):
    page = urllib2.urlopen(url).read()
    page = page.decode('utf-8')
    page = page.encode('ascii', 'ignore')
    return page


def cleanup_values(data):
    for k,v in data.items():
        data[k] = re.sub(WHITESPACE_PAT, ' ', v)
    return data


def get_primary_data():
    url = 'http://www.ipa.co.uk/Agencies/'
    page = fetch(url)
    doc = lxml.html.fromstring(page)
    data = doc.cssselect('div#divAgencyMap > input')[0].get('value')
    data = HTMLParser.HTMLParser().unescape(data)
    return json.loads(data)


def get_agency_data(agency):
    data = {}
    for key in PRIMARY_DATA_KEYS:
        data[key] = agency[key]
    page = fetch('http://www.ipa.co.uk%s' % agency['Url'])
    internat = INTERNATIONAL_PAT.findall(page)
    if internat:
        data['international'] = internat[0].strip()
    doc = lxml.html.fromstring(page)
    a = doc.cssselect('div.agency_contact_info a')
    if a:
        data['Web'] = a[0].get('href')
    ul = doc.cssselect('ul#majorClientsList')
    if ul:
        clients = ul[0].text_content().split('||')
        if len(clients) == 1:
            clients = clients[0].split('\n')
        data['clients'] = ';'.join([i.strip() for i in clients if i.strip()])
    data = cleanup_values(data)
    people = []
    for i,figure in enumerate(doc.cssselect('div.agency_detail_people figure'), start=1):
        figure_data = {}
        img = figure.cssselect('img')
        if img:
            figure_data['image'] = img[0].get('src').strip()
        name = figure.cssselect('div.figcaption h2')
        if name:
            figure_data['name'] = name[0].text_content().strip()
        info = figure.cssselect('div.figcaption p')
        if info:
            figure_data['info'] = info[0].text_content().strip()
        #people.append(cleanup_values(figure_data))
        for k,v in cleanup_values(figure_data).items():
            data['person_%s_%s' % (i, k)] = v
    #data['people'] = people
    return data


def main():
    agencies = []
    for agency in get_primary_data()['agencies']:
        agencies.append(get_agency_data(agency))
    scraperwiki.sqlite.save(unique_keys=['Id'], data=agencies)


main()import json
import lxml.html
import HTMLParser
import re
import scraperwiki
import urllib2

INTERNATIONAL_PAT = re.compile(r'<dt>International: </dt><dd>(.*?)</dd>')
WHITESPACE_PAT = re.compile(r'\s+')
PRIMARY_DATA_KEYS = [ # uncomment keys to include
    'Fax',
    'Id',
    'Intro',
    'Name',
    'PostCode',
    'Staff',
    'StreetName',
    'Telephone',
    'Town',
    'Url',
    #'Established',
    #'RewrittenUrl',
    #'District',
    #'IsAffiliated',
    #'ImageOffice',
    #'Latitude',
    #'IsBuildingShare',
    #'ParentAgencyName',
    #'Vacancies',
    #'Joined',
    #'Longitude',
    #'ImageLogo',
    #'Letter',
    #'Offices',
    #'AddressSummary',
    #'BuildingShareCode',
    #'IsBranch',
]


def fetch(url):
    page = urllib2.urlopen(url).read()
    page = page.decode('utf-8')
    page = page.encode('ascii', 'ignore')
    return page


def cleanup_values(data):
    for k,v in data.items():
        data[k] = re.sub(WHITESPACE_PAT, ' ', v)
    return data


def get_primary_data():
    url = 'http://www.ipa.co.uk/Agencies/'
    page = fetch(url)
    doc = lxml.html.fromstring(page)
    data = doc.cssselect('div#divAgencyMap > input')[0].get('value')
    data = HTMLParser.HTMLParser().unescape(data)
    return json.loads(data)


def get_agency_data(agency):
    data = {}
    for key in PRIMARY_DATA_KEYS:
        data[key] = agency[key]
    page = fetch('http://www.ipa.co.uk%s' % agency['Url'])
    internat = INTERNATIONAL_PAT.findall(page)
    if internat:
        data['international'] = internat[0].strip()
    doc = lxml.html.fromstring(page)
    a = doc.cssselect('div.agency_contact_info a')
    if a:
        data['Web'] = a[0].get('href')
    ul = doc.cssselect('ul#majorClientsList')
    if ul:
        clients = ul[0].text_content().split('||')
        if len(clients) == 1:
            clients = clients[0].split('\n')
        data['clients'] = ';'.join([i.strip() for i in clients if i.strip()])
    data = cleanup_values(data)
    people = []
    for i,figure in enumerate(doc.cssselect('div.agency_detail_people figure'), start=1):
        figure_data = {}
        img = figure.cssselect('img')
        if img:
            figure_data['image'] = img[0].get('src').strip()
        name = figure.cssselect('div.figcaption h2')
        if name:
            figure_data['name'] = name[0].text_content().strip()
        info = figure.cssselect('div.figcaption p')
        if info:
            figure_data['info'] = info[0].text_content().strip()
        #people.append(cleanup_values(figure_data))
        for k,v in cleanup_values(figure_data).items():
            data['person_%s_%s' % (i, k)] = v
    #data['people'] = people
    return data


def main():
    agencies = []
    for agency in get_primary_data()['agencies']:
        agencies.append(get_agency_data(agency))
    scraperwiki.sqlite.save(unique_keys=['Id'], data=agencies)


main()