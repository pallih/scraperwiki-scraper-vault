import scraperwiki #permite que a gente salve os nossos resultados
from lxml.html import parse
import re

links_todos = ['http://oglobo.globo.com/rio/mat/2011/07/13/pm-anuncia-prisao-do-maior-hacker-do-rio-de-janeiro-924898599.asp','http://oglobo.globo.com/tecnologia/mat/2011/07/15/meu-amigo-foi-atacado-por-um-hacker-sistema-da-microsoft-tenta-evitar-roubo-de-senhas-no-hotmail-924914313.asp', 'http://oglobo.globo.com/pais/noblat/posts/2011/06/28/hacker-mesmo-outra-coisa-389024.asp', 'http://oglobo.globo.com/pais/mat/2011/06/30/policia-federal-abre-inquerito-para-investigar-invasao-de-hacker-ao-mail-da-presidente-dilma-durante-eleicao-924804515.asp']

links = ['http://oglobo.globo.com/pais/noblat/posts/2011/06/28/hacker-mesmo-outra-coisa-389024.asp']

for url in links:
    if re.match('.*/mat/.*', url):
        ps = parse(url).getroot()
        
        data = {}
        data['titulo'] = ps.cssselect('#ltintb h3')[0].text_content()
        data['autor'] = ps.cssselect('#ltintb cite')[0].text_content()
        data['texto'] = ''
        for paragrafo in ps.cssselect('#ltintb p'):
            data['texto'] = data['texto'] + paragrafo.text_content()
            
        data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()
        data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')

        scraperwiki.sqlite.save(['titulo'], data)
    elif re.match('.*/noblat/.*', url):
        ps = parse(url).getroot()
        
        data = {}
        data['titulo'] = ps.cssselect('.tituloPost')[0].text_content().strip()
        data['autor'] = ps.cssselect('.IdentificadorPost b')[0].text_content().strip('Enviado por ')
        data['texto'] = ''
        lista_de_paragrafos = ps.cssselect('.corpoPost p')[:-4]
        for paragrafo in lista_de_paragrafos:
            data['texto'] = data['texto'] + ' ' + paragrafo.text_content()
            
        data['editoria'] = ps.cssselect('.corpoPost h6')[0].text_content()
        data['editoria_link'] = ''

        scraperwiki.sqlite.save(['titulo'], data)
        

    else:
        print 'essa url nao eh noticia ' + url
