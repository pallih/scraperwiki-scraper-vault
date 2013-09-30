from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save

data={"fname":"heldlo", "lname":"edrgr"
}
COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
raw = download.read()
html=fromstring(raw)
table = html.cssselect('table')[2]
for tr in table.cssselect('tr')[1:]:
    cell_text =[td.text_content() for td in tr.cssselect('td')]
    data = dict(zip(COLUMN_NAMES, cell_text))
    data['num_workers'] = int(data['num_workers'])
    if len(data['location']) == 2:
        data['state'] = data['location']
    save([], data)from urllib2 import urlopen
from lxml.html import fromstring, tostring
from scraperwiki.sqlite import save

data={"fname":"heldlo", "lname":"edrgr"
}
COLUMN_NAMES = [
    'employer','download','location','union',
    'local', 'naics', 'num_workers', 'expiration_date'
]

download = urlopen('http://www.dol.gov/olms/regs/compliance/cba/Cba_CaCn.htm')
raw = download.read()
html=fromstring(raw)
table = html.cssselect('table')[2]
for tr in table.cssselect('tr')[1:]:
    cell_text =[td.text_content() for td in tr.cssselect('td')]
    data = dict(zip(COLUMN_NAMES, cell_text))
    data['num_workers'] = int(data['num_workers'])
    if len(data['location']) == 2:
        data['state'] = data['location']
    save([], data)