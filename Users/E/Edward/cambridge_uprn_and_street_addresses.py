import scraperwiki
import re
from lxml import html
from time import sleep

start = 'http://www.cambridge.gov.uk/ccm/content/environment-and-recycling/rubbish-waste-and-recycling/bins/bin-collections.en'
re_last = re.compile('page=(\d+)')

def get_all():
    url = 'http://cambridge.jdi-consult.net/bins/bins.php?postcode=%25'
    root = html.parse(url).getroot()
    last = root.cssselect("a[title='last']")[0]
    last_page = int(re_last.search(last.get('href')).group(1))

    for page in range(1, last_page+1):
        sleep(1)
        root = html.parse(url + '&page={}'.format(page)).getroot()
        address_list = root.cssselect("table[id='bins_search_address_list']")[0]
        for row in address_list[1:]:
            a = row[0][0]
            href = a.get('href')
            assert href.startswith('/bins/bins.php?uprn=')
            uprn = href[href.find('=')+1:]
            data = {'uprn': uprn, 'address': a.text}
            scraperwiki.sqlite.save(unique_keys=['uprn'], data=data)

get_all()