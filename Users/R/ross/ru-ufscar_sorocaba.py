import scraperwiki
import lxml.html
from pprint import pprint


html = scraperwiki.scrape("http://www.sorocaba.ufscar.br/ufscar/index.php?pg_id=39")
tree = lxml.html.fromstring(html)


menu = []
for div in tree.cssselect('div[class=noticia]'):
    for table in div.getiterator('table'):
        titulo = (table[0][0].text_content().split('-')[1].strip('\r\n')).encode('utf-8')
        datas = [el.text_content().strip('\r\n').encode('utf-8') for el in table[0][2]]

        for i, td in enumerate(table[0][3].getiterator('td')):
            ps = td.findall('p')
            tipos = ["`" + e.text_content().encode('utf-8') + "`"  for e in ps[::3]]
            pratos = [e.text_content().encode('utf-8') for e in ps[1::3]]
            norm = dict(zip(tipos, pratos))
            dados = {
               'periodo' : titulo,
               'data' : datas[i],
               'tipo': 'normal'
            }
            dados.update(norm)
            menu.append(dados)
            scraperwiki.sqlite.save(unique_keys=['periodo', 'data', 'tipo'],
                                    data=dados)

        for i, td in enumerate(table[0][5].cssselect('td')):
            ps = td.findall('p')
            tipos = ['Arroz']
            pratos = [ps[0].text_content().encode('utf-8')]
            tipos += ['`' + e.text_content().encode('utf-8') + '`' 
                      for e in ps[2::3]
                      if not e.text_content().startswith(u'\xa0')]
            pratos += [e.text_content().encode('utf-8')
                       for e in ps[3::3]
                       if not e.text_content().startswith(u'\xa0')]
            veg = dict(zip(tipos, pratos))
            dados = {
               'periodo' : titulo,
               'data' : datas[i],
               'tipo': 'vegetariano'
            }
            menu.append(dados)
            dados.update(veg)
            scraperwiki.sqlite.save(unique_keys=['periodo', 'data', 'tipo'], data=dados)

pprint(sorted(menu, key=lambda x:x['data']))
