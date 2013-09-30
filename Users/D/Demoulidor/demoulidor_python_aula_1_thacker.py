import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

ps = parse("http://oglobo.globo.com/pais/noblat/posts/2011/06/28/hacker-mesmo-outra-coisa-389024.asp").getroot()

data = {}

data['titulo'] = ps.cssselect('#content h4')[0].text_content()

print data['titulo']

data['autor'] = ps.cssselect('#content p strong')[0].text_content()

print data['autor']

data['texto'] = ''

for paragrafo in ps.cssselect('#content p'):
    data['texto'] = data['texto'] + paragrafo.text_content()

data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()

print data['editoria']

data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

print data['editoria_link']

scraperwiki.sqlite.save(['titulo'], data)


import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

ps = parse("http://oglobo.globo.com/pais/noblat/posts/2011/06/28/hacker-mesmo-outra-coisa-389024.asp").getroot()

data = {}

data['titulo'] = ps.cssselect('#content h4')[0].text_content()

print data['titulo']

data['autor'] = ps.cssselect('#content p strong')[0].text_content()

print data['autor']

data['texto'] = ''

for paragrafo in ps.cssselect('#content p'):
    data['texto'] = data['texto'] + paragrafo.text_content()

data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()

print data['editoria']

data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

print data['editoria_link']

scraperwiki.sqlite.save(['titulo'], data)


