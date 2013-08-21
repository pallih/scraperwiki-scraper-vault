import scraperwiki
import requests
import lxml.html
import re

letters = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqr', 'stu', 'vwx', 'yz', '0-9']


URL = 'http://www.thueringenweb.de/site/start'

def get_addresses(root):
    uebers = root.cssselect('.adressenueber')
    contents = root.cssselect('.adressencontent')
    addresses = {}
    for ueber, content in zip(uebers, contents):
        name = ueber.text_content().strip()
        data = {
            'name': name,
            'jurisdiction__slug': 'thueringen'
        }
        for line in content.cssselect('.adressenzeile'):
            divs = line.cssselect('div')
            data[divs[1].text_content().strip()] = divs[2].text_content().strip()
        addresses[name] = data
    return addresses

def scrape(letter, topic=''):
    paging = {
        'next': 20,
        'page': 1,
        'char': '',
        'searchlog': 'no',
        'reiter': '',
        'reitername': '',
        'aktion_bewerten':''
    }
    data = {'ridtb': "224", 'il': '1', 'pid': '11', 'httppostvars': '------------------', 'letters': 'ghi', 'ortsauswahl': '', 'textsuchen': ''}
    data.update({'letters': letter, 'textsuchen': topic})
    response = requests.post(URL, data=data)
    match = re.search('Seite \d+ von (\d+)', response.content)
    max_pages = int(match.group(1))
    root = lxml.html.fromstring(response.content)
    topics = []
    elems = root.cssselect('#textsuchen option')
    for elem in elems:
        topics.append(elem.attrib['value'])
    addresses = get_addresses(root)
    data.update(paging)
    for page in range(1, max_pages):
        data.update({'page': page, 'next': 20 * page})
        response = requests.post(URL, data=data)
        root = lxml.html.fromstring(response.content)
        adrs = get_addresses(root)
        addresses.update(adrs)
    return topics, addresses

def main():
    addresses = {}
    for letter in letters:
        topics, adrs = scrape(letter, topic='')
        addresses.update(adrs)
        for topic in topics:
            _, adrs = scrape(letter, topic=topic)
            print topic, len(adrs)
        addresses.update(adrs)
    scraperwiki.sqlite.save(unique_keys=['name'], data=addresses.values())
    

main()