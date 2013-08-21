import scraperwiki

import requests
import lxml.html

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_company(elm):
    modal = None
    try:
        for key, value in elm.cssselect('img')[-1].items():
            if key == 'onclick':
                modal = value
    except Exception:
        pass

    try:
        if modal:
            url = modal[len("openModal('"):]
            return url.split(',')[0]
    except Exception:
        pass

    return 'N/A'

url = "http://www.halal.gov.my/ehalal/directory_standalone.php?type=P&cari=a"
html = requests.get(url).content
root = lxml.html.fromstring(html)
outer_table = root.cssselect("table")[1]
found = False
for tr in outer_table.cssselect("tr"):
    for td in tr.cssselect("td"):
        if td.text_content().strip() == 'SENARAI PRODUK':
            found = True
            break
    if found:
        data_row_counter = 0
        for td in tr.cssselect("tr"):
            data_row_counter += 1
            row_data = strip_tags(td.text_content()).strip()
            row_data_part = row_data.split('\n')

            try:
                bil = row_data_part[0].strip()
                product = row_data_part[2].strip().replace("\t", '')
                expired = row_data_part[5].strip()
            except Exception:
                continue

            import pdb;pdb.set_trace()
            print bil, product, expired, get_company(td)
            if data_row_counter == 3:
                print "\n"
                data_row_counter = 0