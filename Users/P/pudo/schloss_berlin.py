import scraperwiki
import requests
from lxml import html

doc = html.parse('http://berliner-schloss.de/spenden-system/spenden-spenderliste')
for name in doc.findall('//input[@name="name_search"]'):
    page_filter = name.get('value')
    res = requests.post('http://berliner-schloss.de/spenden-system/spenden-spenderliste', 
        data={'name_search': page_filter})
    id = html.fromstring(res.content)
    for num, row in enumerate(id.findall('.//table[@id="se_spenderlisten_table"]//tr')):
        tds = row.findall('./td') 
        if len(tds) < 2:
            continue
        name, city, _ = row.findall('./td')
        pf = '%s-%s' % (page_filter, num)
        scraperwiki.sqlite.save(['id'], {
            'id': pf,
            'num': num,
            'page': page_filter,
            'name': name.text, 
            'city': city.text
            })

import scraperwiki
import requests
from lxml import html

doc = html.parse('http://berliner-schloss.de/spenden-system/spenden-spenderliste')
for name in doc.findall('//input[@name="name_search"]'):
    page_filter = name.get('value')
    res = requests.post('http://berliner-schloss.de/spenden-system/spenden-spenderliste', 
        data={'name_search': page_filter})
    id = html.fromstring(res.content)
    for num, row in enumerate(id.findall('.//table[@id="se_spenderlisten_table"]//tr')):
        tds = row.findall('./td') 
        if len(tds) < 2:
            continue
        name, city, _ = row.findall('./td')
        pf = '%s-%s' % (page_filter, num)
        scraperwiki.sqlite.save(['id'], {
            'id': pf,
            'num': num,
            'page': page_filter,
            'name': name.text, 
            'city': city.text
            })

