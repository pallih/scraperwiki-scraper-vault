from urllib2 import urlopen
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring
from unidecode import unidecode

def get_area(url):
    source = urlopen(url).read()
    dec = unidecode(source)
    adec = dec.encode("ascii","ignore")
    html = fromstring(dec)
    infotable = html.cssselect('#tab_obce_1')
    table = infotable[0]
    
    
    ths = table.cssselect('tr th')
    labels = [th.text_content() for th in ths]
    print labels   
    
    tds = table.cssselect('tr td')
    data=  [td.text_content() for td in tds]
    
    area = table.xpath('//th[text()="KatastrA!lnA plocha (ha):"]/following-sibling::td/text()')[0]
    return int(area.replace('A ', ''))

#rowd = dict(zip(labels,data))
#save([],rowd)

#print get_area('http://www.risy.cz/cs/vyhledavace/obce/detail?Zuj=547441')

def ids():
    csv = urlopen('http://www.rozpocetobce.cz/bundles/publicbudgetfrontend/files/Seznam-obci-CR-EN.csv').read()
    rows = csv.split('\n')[1:-1]
    municipality_identifiers = [row.split(',')[3] for row in rows]
    return municipality_identifiers

from time import sleep
for _id in ids():
    data = {
        'url': 'http://www.risy.cz/cs/vyhledavace/obce/detail?Zuj=' + _id,
        'code': _id,
    }

    data['area'] = get_area(data['url'])
    save([], data, 'municipality')
    sleep(0.3)
from urllib2 import urlopen
from scraperwiki.sqlite import save
from lxml.html import fromstring, tostring
from unidecode import unidecode

def get_area(url):
    source = urlopen(url).read()
    dec = unidecode(source)
    adec = dec.encode("ascii","ignore")
    html = fromstring(dec)
    infotable = html.cssselect('#tab_obce_1')
    table = infotable[0]
    
    
    ths = table.cssselect('tr th')
    labels = [th.text_content() for th in ths]
    print labels   
    
    tds = table.cssselect('tr td')
    data=  [td.text_content() for td in tds]
    
    area = table.xpath('//th[text()="KatastrA!lnA plocha (ha):"]/following-sibling::td/text()')[0]
    return int(area.replace('A ', ''))

#rowd = dict(zip(labels,data))
#save([],rowd)

#print get_area('http://www.risy.cz/cs/vyhledavace/obce/detail?Zuj=547441')

def ids():
    csv = urlopen('http://www.rozpocetobce.cz/bundles/publicbudgetfrontend/files/Seznam-obci-CR-EN.csv').read()
    rows = csv.split('\n')[1:-1]
    municipality_identifiers = [row.split(',')[3] for row in rows]
    return municipality_identifiers

from time import sleep
for _id in ids():
    data = {
        'url': 'http://www.risy.cz/cs/vyhledavace/obce/detail?Zuj=' + _id,
        'code': _id,
    }

    data['area'] = get_area(data['url'])
    save([], data, 'municipality')
    sleep(0.3)
