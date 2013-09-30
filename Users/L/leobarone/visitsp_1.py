import scraperwiki
from lxml.html import parse

url = 'http://www.portaldatransparencia.gov.br/convenios/DetalhaConvenio.asp?CodConvenio=652760&TipoConsulta=TR-PJ3'

ps = parse(url).getroot()

for tr in ps.cssselect('#listagemConvenios'):
    
    data = {}
    
    data['convenio'] = ps.cssselect('strong')[0].text_content()
    data['situacao'] = ps.cssselect('strong')[1].text_content()
    data['numoriginal'] = ps.cssselect('strong')[2].text_content()
    data['objetoconvenio'] = ps.cssselect('strong')[3].text_content()
    data['orgaosuperior'] = ps.cssselect('strong')[4].text_content()
    data['concedente'] = ps.cssselect('strong')[5].text_content()
    data['convenente'] = ps.cssselect('strong')[6].text_content()
    data['valorconvenio'] = ps.cssselect('strong')[7].text_content()
    data['valorliberado'] = ps.cssselect('strong')[8].text_content()
    data['publicacao'] = ps.cssselect('strong')[9].text_content()
    data['iniciovigencia'] = ps.cssselect('strong')[10].text_content()
    data['fimvigencia'] = ps.cssselect('strong')[11].text_content()
    data['valorcontrapartida'] = ps.cssselect('strong')[12].text_content()
    data['dataultimaliberacao'] = ps.cssselect('strong')[13].text_content()
    data['valorultimaliberacao'] = ps.cssselect('strong')[14].text_content()

    print data
    scraperwiki.sqlite.save(['convenio'], data)import scraperwiki
from lxml.html import parse

url = 'http://www.portaldatransparencia.gov.br/convenios/DetalhaConvenio.asp?CodConvenio=652760&TipoConsulta=TR-PJ3'

ps = parse(url).getroot()

for tr in ps.cssselect('#listagemConvenios'):
    
    data = {}
    
    data['convenio'] = ps.cssselect('strong')[0].text_content()
    data['situacao'] = ps.cssselect('strong')[1].text_content()
    data['numoriginal'] = ps.cssselect('strong')[2].text_content()
    data['objetoconvenio'] = ps.cssselect('strong')[3].text_content()
    data['orgaosuperior'] = ps.cssselect('strong')[4].text_content()
    data['concedente'] = ps.cssselect('strong')[5].text_content()
    data['convenente'] = ps.cssselect('strong')[6].text_content()
    data['valorconvenio'] = ps.cssselect('strong')[7].text_content()
    data['valorliberado'] = ps.cssselect('strong')[8].text_content()
    data['publicacao'] = ps.cssselect('strong')[9].text_content()
    data['iniciovigencia'] = ps.cssselect('strong')[10].text_content()
    data['fimvigencia'] = ps.cssselect('strong')[11].text_content()
    data['valorcontrapartida'] = ps.cssselect('strong')[12].text_content()
    data['dataultimaliberacao'] = ps.cssselect('strong')[13].text_content()
    data['valorultimaliberacao'] = ps.cssselect('strong')[14].text_content()

    print data
    scraperwiki.sqlite.save(['convenio'], data)