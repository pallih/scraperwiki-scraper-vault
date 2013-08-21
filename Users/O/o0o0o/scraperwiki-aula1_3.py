import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

ps = parse("http://oglobo.globo.com/tecnologia/mat/2011/06/27/hacker-mesmo-outra-coisa-924783725.asp").getroot()

data = {}

data['titulo'] = ps.cssselect('#ltintb h3')[0].text_content()
data['autor'] = ps.cssselect('#ltintb cite')[0].text_content()
data['texto'] = ''
for paragrafo in ps.cssselect('#ltintb p'):
    data['texto'] = data['texto'] + paragrafo.text_content()

data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()
data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

scraperwiki.sqlite.save(['titulo'], data)