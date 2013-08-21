import re
import scraperwiki
import lxml.html
from urllib2 import HTTPError

BASE_URL = "http://www.cityofchicago.org"
DEPARTMENTS_URL = "/city/en/depts.html"
FOIA_CONTACTS_URL = "/content/city/en/narr/foia/foia_contacts.html"
DEPARTMENTS_MAP = {
    'administrative hearings': 'Chicago Department of Administrative Hearings',
    'buildings': 'Chicago Department of Buildings',
    'police': 'Chicago Police Department',
    'procurement services': 'Chicago Department of Procurement Services',
    'ethics': 'Chicago Board of Ethics',
    'board of ethics': 'Chicago Board of Ethics',
    'fire': 'Chicago Fire Department',
    'water management': 'Chicago Department of Water Management',
    'human resources': 'Chicago Department of Human Resources',
    'human&nbsp; resources': 'Chicago Department of Human Resources',
    'revenue': 'Chicago Department of Revenue',
    'streets and sanitation': 'Chicago Department of Streets and Sanitation',
    'animal care and control': 'Chicago Animal Care and Control',
    'inspector general\'s office': 'Chicago Inspector General\'s Office',
    'office of the mayor': 'Chicago Office of the Mayor',
    'mayor\'s office': 'Chicago Office of the Mayor',
    'emergency management and communication': 'Chicago Office of Emergency Management and Communications',
    'emergency management and communications': 'Chicago Office of Emergency Management and Communications',
    'oemc': 'Chicago Office of Emergency Management and Communications',
    'zoning and land use planning': 'Chicago Department of Housing and Economic Development',
    'transportation': 'Chicago Department of Transportation',
    'business affairs and consumer protection': 'Chicago Department of Business Affairs and Consumer Protection',
    '311 city services': 'Chicago 311 City Services',
    '311': 'Chicago 311 City Services',
    'environment': 'Chicago Department of Environment',
    'law': 'Chicago Law Department',
    'police board': 'Chicago Police Board',
    'aviation': 'Chicago Department of Aviation',
    'public health': 'Chicago Department of Public Health',
    'health': 'Chicago Department of Public Health',
    'finance': 'Chicago Comptroller\'s Office',
    'budget and management': 'Chicago Office of Budget and Management',
    'independent police review authority': 'Chicago Independent Police Review Authority',
    'community development': 'Chicago Department of Housing and Economic Development',
    'housing and economic development': 'Chicago Department of Housing and Economic Development',
    'compliance': 'Chicago Office of Compliance',
    'fleet management': 'Chicago Department of Fleet Management',
    'special events': 'Chicago Department of Cultural Affairs and Special Events',
    'general services': 'Chicago Department of General Services',
    'innovation and technology': 'Chicago Department of Innovation and Technology',
    'family and support services': 'Chicago Department of Family and Support Services',
    'cultural affairs': 'Chicago Department of Cultural Affairs and Special Events',
    'chicago public library': 'Chicago Public Library',
    'human relations': 'Chicago Commission on Human Relations',
    'mayor\'s office for people with disabilities': 'Chicago Mayor\'s Office for People with Disabilities',
    'license appeal commission': 'Chicago License Appeal Commission',
    'graphics and reproduction center': 'Chicago Bureau of Graphic Services',
    'cultural affairs and special events': 'Chicago Department of Cultural Affairs and Special Events',
    'city clerk': 'Chicago City Clerk',
    'chicago treasurer\'s office': 'Chicago Office of the City Treasurer'
}

def get_from_list(value, index, default = ''):
    try:
        return value[index]
    except:
        return default

def get_department(name):
    return DEPARTMENTS_MAP.get(name.replace('&', 'and').lower(), name)

html = scraperwiki.scrape(BASE_URL + FOIA_CONTACTS_URL)
foia_contact_information_page = lxml.html.fromstring(html)
foia_records = {}
for row in foia_contact_information_page.cssselect("#content-content table tr"):
    record = {}
    record['full_name'] = get_department(row[0][0].text)
    if record['full_name'] == 'Department Name':
        continue
    record['foia_url'] = BASE_URL + row[0][0].get('href')
    record['foia_email'] = row[1][0].text

    foia_records[record['full_name']] = record

city_departments_page = lxml.html.fromstring(scraperwiki.scrape(BASE_URL + DEPARTMENTS_URL))
for heading in city_departments_page.cssselect(".department-directory-heading"):
    record = {}
    record['name'] = heading.text_content()
    if record['name'] == 'Other City, County, and State Agencies':
        continue
    
    record['full_name'] = get_department(record['name'])
    record['url'] = BASE_URL + heading.find("a").get("href")
    record['description'] = heading.getnext().text_content()#".department-description"

    department_information_html = scraperwiki.scrape(record['url'])
    department_information_page = lxml.html.fromstring(department_information_html)
    info_element = department_information_page.cssselect("#department-contactinfo-content ul li")
    contact_info_elements = filter(None, [x.strip() for x in re.split(r'(\r\n|\xa0\xa0\xa0)', info_element[0].text_content())])
    address_elements = filter(None, [x.strip() for x in re.split(r'(\r\n|\xa0\xa0\xa0)', info_element[1].text_content())])

    for contact_info_element in contact_info_elements:
        if 'Phone' in contact_info_element:
            record['phone'] = contact_info_element.replace('Phone:','').strip()
        elif 'Fax' in contact_info_element:
            record['fax'] = contact_info_element.replace('Fax:','').strip()
        elif 'TTY' in contact_info_element:
            record['tty'] = contact_info_element.replace('TTY:','').strip()

    contact_page_element = info_element[0].find("a").get("href") if info_element[0].find("a") is not None else ''

    record['address1'] = get_from_list(address_elements, 0)
    possible_address_two = get_from_list(address_elements, 1)
    if possible_address_two.find('Chicago, IL') == -1:
        record['address2'] = possible_address_two
        city_state_zip = get_from_list(address_elements, 2)
    else:
        city_state_zip = get_from_list(address_elements, 1)

    record['city'] = get_from_list(city_state_zip.split(','),0)
    record['state'] = get_from_list(city_state_zip.split(' '),1)
    record['zip'] = get_from_list(city_state_zip.split(' '),2)


    if 'leadership.html' in department_information_html:
        leadership_url = BASE_URL + re.compile(r'href="(.*leadership.html)').search(department_information_html).group(1)
        try:
            leadership_html = scraperwiki.scrape(leadership_url)
            leadership_page = lxml.html.fromstring(leadership_html)

            leader_name_and_title = leadership_page.cssselect(".leadership-padding ul li")
            record['leader_name'] = leader_name_and_title[0].text
            record['leader_title'] = leader_name_and_title[1].text
            if len(leadership_page.cssselect(".top-images img")) == 1:
                record['leader_photo'] = BASE_URL+leadership_page.cssselect(".top-images img")[0].get("src")
        except HTTPError, e:
            print 'Seriously? %s' % leadership_url

    if record['full_name'] in foia_records:
        record = dict(record.items() + foia_records[record['full_name']].items())

    scraperwiki.sqlite.save(['full_name'], record)