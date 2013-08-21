import scraperwiki
from lxml.html import parse, HTMLParser
from itertools import product
from urllib import urlencode

def clean_options(options):
    return [{'string': option.text_content().strip(), 'code': option.get('value')} for option in options if option.get('value') != '0']

parser = HTMLParser(encoding='utf-8')
url = 'http://www.sescsp.org.br/sesc/programa_new/busca.cfm'

start = parse(url, parser).getroot()
lastpage = start.cssselect('.pagina .paginacao').pop().text_content()
units = clean_options(start.cssselect('select[name="unidade_id"] option'))
dates = clean_options(start.cssselect('select[name="data2"] option'))
types = clean_options(start.cssselect('select[name="atividade_id"] option'))

# dates are useless, let's iterate over the units and types
for (unit, type) in product(units, types):
    print 'getting data from ' + unit['string'] + ' of type ' + type['string']
    schedule = parse(url + '?' + urlencode({'unidade_id': unit['code'], 'atividade_id': type['code']})).getroot()
    if len(schedule.cssselect('.paginacao')):
        print schedule.cssselect('.paginacao')[-1].text_content().strip()
    

#class page
#class event
