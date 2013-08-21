import scraperwiki
import requests
import lxml.html

data = requests.get('http://data.octo.dc.gov/feeds/cjis_juvenile/cjis_juvenile_current.xml')
xml_content = lxml.html.fromstring(data.content)

entries = xml_content.xpath('//entry')

entry_list = []

for entry in entries:
    entry_dict = {}
    entry_dict['id'] = int(entry.xpath('title')[0].text_content().replace('ArrestedJuvenile ID:', ''))
    entry_dict['chargeid'] = entry.xpath('dcst:ArrestedJuvenile',namespaces={'dcst': 'http://dc.gov/dcstat/types/1.0/'})[0].text_content()
#    entry_dict['arrestdate'
#    entry_dict['dob']
#    entry_dict['gender']
#    entry_dict['race']
#    entry_dict['ethnicity']
#    entry_dict['weaponcode']
#    entry_dict['weapondescription']

    entry_list.append(entry_dict)

print entry_list