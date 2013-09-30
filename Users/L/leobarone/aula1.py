import scraperwiki #permite salvar resultados - é um conjunto de coisas prontas para se utilizar
from lxml.html import parse # funcao parse é a que scrapeia

url = 'http://oglobo.globo.com/rio/mat/2011/07/13/pm-anuncia-prisao-do-maior-hacker-do-rio-de-janeiro-924898599.asp'

ps = parse(url).getroot() #coloca cod html definido no ps ps=paginascrapeada

data = {}

data['titulo']= ps.cssselect('#ltintb h3')[0].text_content() #campos precisa ser guardados numa lista ... ps é do url .. cssselect é para selecionar 
data['autor']= ps.cssselect('#ltintb cite')[0].text_content()
data['data'] = ps.cssselect('#ltintb p')[0].text_content()
data['texto']= ''
for paragrafo in ps.cssselect('#ltintb p'):
    data['texto'] = data['texto'] + paragrafo.text_content()
    print data['texto']

data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()
data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

print data

scraperwiki.sqlite.save(['titulo'], data)

#data('corpo')=ps.cssselect('#ltintb ')[0].textcontent()
#data('')
import scraperwiki #permite salvar resultados - é um conjunto de coisas prontas para se utilizar
from lxml.html import parse # funcao parse é a que scrapeia

url = 'http://oglobo.globo.com/rio/mat/2011/07/13/pm-anuncia-prisao-do-maior-hacker-do-rio-de-janeiro-924898599.asp'

ps = parse(url).getroot() #coloca cod html definido no ps ps=paginascrapeada

data = {}

data['titulo']= ps.cssselect('#ltintb h3')[0].text_content() #campos precisa ser guardados numa lista ... ps é do url .. cssselect é para selecionar 
data['autor']= ps.cssselect('#ltintb cite')[0].text_content()
data['data'] = ps.cssselect('#ltintb p')[0].text_content()
data['texto']= ''
for paragrafo in ps.cssselect('#ltintb p'):
    data['texto'] = data['texto'] + paragrafo.text_content()
    print data['texto']

data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()
data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

print data

scraperwiki.sqlite.save(['titulo'], data)

#data('corpo')=ps.cssselect('#ltintb ')[0].textcontent()
#data('')
