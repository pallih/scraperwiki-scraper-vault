import scraperwiki
from lxml.html import parse

# Blank Python

def penitencia(numero):
    soup = parse('http://www.deap.sc.gov.br/deap/unidade_prisional.jsp?id=' + str(numero)).getroot()
    
    table_root = soup.cssselect('table[width="500"]')[0]
    
    data = {}
    data['p_id'] = numero
    data['name'] = table_root.cssselect('th.fb14rd')[1].text_content().strip()
    body = table_root.cssselect('td.fn14gn table tr')
    for field in body:
        fieldname = field.cssselect('td.fn12gn')[0].text_content().strip(':').lower()
        if fieldname == 'imagem':
            data[fieldname] = 'http://www.deap.sc.gov.br/deap/' + field.cssselect('td.fn12rd a')[0].get('href')
        else:
            data[fieldname] = field.cssselect('td.fn12rd')[0].text_content().strip()
    return data

for a in range(17,100):
    try:
        data = penitencia(a)
        if data['name']:
            scraperwiki.sqlite.save(['p_id'], data)
    except:
        print 'http://www.deap.sc.gov.br/deap/unidade_prisional.jsp?id=' + str(a)
import scraperwiki
from lxml.html import parse

# Blank Python

def penitencia(numero):
    soup = parse('http://www.deap.sc.gov.br/deap/unidade_prisional.jsp?id=' + str(numero)).getroot()
    
    table_root = soup.cssselect('table[width="500"]')[0]
    
    data = {}
    data['p_id'] = numero
    data['name'] = table_root.cssselect('th.fb14rd')[1].text_content().strip()
    body = table_root.cssselect('td.fn14gn table tr')
    for field in body:
        fieldname = field.cssselect('td.fn12gn')[0].text_content().strip(':').lower()
        if fieldname == 'imagem':
            data[fieldname] = 'http://www.deap.sc.gov.br/deap/' + field.cssselect('td.fn12rd a')[0].get('href')
        else:
            data[fieldname] = field.cssselect('td.fn12rd')[0].text_content().strip()
    return data

for a in range(17,100):
    try:
        data = penitencia(a)
        if data['name']:
            scraperwiki.sqlite.save(['p_id'], data)
    except:
        print 'http://www.deap.sc.gov.br/deap/unidade_prisional.jsp?id=' + str(a)
