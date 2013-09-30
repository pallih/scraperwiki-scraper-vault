import scraperwiki, urllib
from lxml.html import parse

base_url = "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente=" 
no_incidente = 2312886

html = urllib.urlopen(base_url+str(no_incidente))
soup = parse(html).getroot()

data = {}

data['titulo'] = soup.cssselect('#detalheProcesso h3 strong')[0].text

data['origem'] = soup.cssselect('.comum strong')[0].text
data['relator'] = soup.cssselect('.comum strong')[1].text
data['agtes'] = soup.cssselect('.comum strong')[2].text
data['agtes_advs'] = soup.cssselect('.comum strong')[3].text
data['agdos'] = soup.cssselect('.comum strong')[4].text
data['agdos_advs'] = soup.cssselect('.comum strong')[5].text
data['andamentos'] = []

for linha in soup.cssselect(".resultadoAndamentoProcesso tr")[1:]:
    colunas = linha.cssselect('td')
    data['andamentos'].append({ 
    'data' : colunas[0].text_content().strip(),
    'andamento' : colunas[1].text_content().strip(),
    'orgao_julgador' : colunas[2].text_content().strip(),
    'obs' : colunas[3].text_content().strip(),
    'documento' : colunas[4].text_content().strip() })

scraperwiki.sqlite.save(["titulo"], data)
import scraperwiki, urllib
from lxml.html import parse

base_url = "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente=" 
no_incidente = 2312886

html = urllib.urlopen(base_url+str(no_incidente))
soup = parse(html).getroot()

data = {}

data['titulo'] = soup.cssselect('#detalheProcesso h3 strong')[0].text

data['origem'] = soup.cssselect('.comum strong')[0].text
data['relator'] = soup.cssselect('.comum strong')[1].text
data['agtes'] = soup.cssselect('.comum strong')[2].text
data['agtes_advs'] = soup.cssselect('.comum strong')[3].text
data['agdos'] = soup.cssselect('.comum strong')[4].text
data['agdos_advs'] = soup.cssselect('.comum strong')[5].text
data['andamentos'] = []

for linha in soup.cssselect(".resultadoAndamentoProcesso tr")[1:]:
    colunas = linha.cssselect('td')
    data['andamentos'].append({ 
    'data' : colunas[0].text_content().strip(),
    'andamento' : colunas[1].text_content().strip(),
    'orgao_julgador' : colunas[2].text_content().strip(),
    'obs' : colunas[3].text_content().strip(),
    'documento' : colunas[4].text_content().strip() })

scraperwiki.sqlite.save(["titulo"], data)
