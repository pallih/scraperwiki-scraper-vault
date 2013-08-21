import scraperwiki

from datetime import datetime, timedelta
from pprint import pprint

from lxml.html import parse
import lxml.etree as etree

tree = parse("http://www2.ufscar.br/servicos/cardapio.php").getroot()

menu = []
skip = True
table = tree.cssselect('table.style3')[0]

for tr in table.cssselect('tr')[2]:
    for tab in tr.cssselect('table'):
        print etree.tostring(tab)

    '''
    if "Card" in tds[0].text_content():
        if skip:
            skip = False
            #continue

        titulo = tds[0].text_content().split('-')[1].strip()
        datas = [el.text_content().strip() for el in trs[2]]

        for i, td in enumerate(trs[3].cssselect('td')):
            ps = td.findall('p')
            tipos = [e.text_content().encode('utf-8').replace('ç', 'c').replace('ã', 'a') for e in ps[::3]]
            pratos = [e.text_content() for e in ps[1::3]]
            norm = dict(zip(tipos, pratos))
            dados = {
               'periodo' : titulo,
               'data' : datas[i],
            }
            dados.update(norm)
            menu.append(dados)

        for i, td in enumerate(trs[5].cssselect('td')):
            ps = td.findall('p')
            tipos = ['Arroz']
            pratos = [ps[0].text_content()]
            tipos += [e.text_content().encode('utf-8').replace('ç', 'c').replace('ã', 'a') + ' vegetariano'
                      for e in ps[2::3]]
            pratos += [e.text_content() for e in ps[3::3]]
            veg = dict(zip(tipos, pratos))
            dados = next(dado for dado in menu if dado['periodo'] == titulo and dado['data'] == datas[i])
            dados.update(veg)
    '''

#for dados in menu:
#    scraperwiki.sqlite.save(unique_keys=['periodo', 'data'], data=dados)

pprint(sorted(menu, key=lambda x:x['data']))
