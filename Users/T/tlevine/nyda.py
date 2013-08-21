from urllib2 import urlopen
from lxml.html import fromstring
from time import time
from scraperwiki import swimport
from scraperwiki.sqlite import save
keyify = swimport('keyify').keyify
import re

DATE = time()
MENU = "http://www.nyda.gov.za/index.php?option=com_content&view=category&id=54&Itemid=166"
DOMAIN= "http://www.nyda.gov.za"

def main():
    provinces = menu()
    locations = []
    for provinceurl in [p['url'] for p in provinces]:
        locations.extend(doprovince(provinceurl))

    addstuff(provinces)
    addstuff(locations)
    save([], provinces, 'provinces')
    save([], locations, 'locations')

def addstuff(d):
    for row in d:
      row['date_scraped'] = DATE
      if row.has_key('Postal_Address'):
        codes = re.findall(r'[0-9]{4}', row['Postal_Address'])
        if len(codes) > 0:
          row['postal-code'] = codes[-1]

def menu():
    p = urlopen(MENU).read()
    html = fromstring(p)
    a_nodes = html.xpath('//form[@name="adminForm"]/descendant::a')
    return [{"url": DOMAIN + a.attrib['href'], "province": a.text.strip()} for a in a_nodes]

def doprovince(url):
    html = fromstring(urlopen(url).read().replace('<','\n<'))
    headers = html.xpath('//span[style="color: #ff0000;"]')
    for header in headers:
        html.remove(header)

    lines = html.get_element_by_id('page').text_content().split('\n')

    keys = set(['Telephone', 'Physical Address', 'Branch Manager', 'Postal Address', 'Fax'])

    d = [{}]
    key = None
    for line in lines:
        line = line.replace(':', '').strip()

        if line == '':
            continue

        elif line in keys:
            key = keyify(line)

        elif key != None:
            if key in d[-1]:
                d.append({
                    key: line,
                    'locationName': location_name,
                    'provinceUrl': url
                })

            else:
                d[-1][key] = line

            key = None

        elif line != '':
            location_name = line

    return d

main()