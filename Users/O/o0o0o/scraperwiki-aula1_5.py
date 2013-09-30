import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

es=[]
for i in xrange(130):
    try:
        ps = parse("http://www1.camara.sp.gov.br/vereador.asp?vereador="+str(i+1)).getroot()
        links=ps.cssselect('a')
        for link in links:
            l=link.text_content()
            if "@" in l:
                es.append(l)
    except:
        pass
    



#data['autor'] = ps.cssselect('#ltintb cite')[0].text_content()
#data['texto'] = ''
#for paragrafo in ps.cssselect('#ltintb p'):
#    data['texto'] = data['texto'] + paragrafo.text_content()

#data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()
#data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

#scraperwiki.sqlite.save(['titulo'], data)import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

es=[]
for i in xrange(130):
    try:
        ps = parse("http://www1.camara.sp.gov.br/vereador.asp?vereador="+str(i+1)).getroot()
        links=ps.cssselect('a')
        for link in links:
            l=link.text_content()
            if "@" in l:
                es.append(l)
    except:
        pass
    



#data['autor'] = ps.cssselect('#ltintb cite')[0].text_content()
#data['texto'] = ''
#for paragrafo in ps.cssselect('#ltintb p'):
#    data['texto'] = data['texto'] + paragrafo.text_content()

#data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()
#data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

#scraperwiki.sqlite.save(['titulo'], data)