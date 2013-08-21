import scraperwiki, urllib
from lxml.html import parse


url_original = "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente=2312886"

dicionario = { 'chave' : 'valor', 'chave2' : 'valor2', 'chave3' : 10 }
dicionario = { 'nome' : 'pedro' }
lista = ['pedro', 'joao', 'rodrigo']
lista = [1,2,3,4,5]
lista = [1,'pedro',4,3.9]

data_original = {
    'titulo' : 'AI 553939 - AGRAVO DE INSTRUMENTO  (Processo físico)',
    'origem' : 'SP - SÃO PAULO',
    'relator': 'MIN. DIAS TOFFOLI',
    'agtes' : 'LUIZ ALBERTO GREGORIN E OUTRO(A/S)',
    'agtes_advs' : 'HIROKO HASHIMOTO VIANA E OUTRO(A/S)',
    'agdos' : 'MASSA FALIDA DE SELECTA COMÉRCIO E INDÚSTRIA S.A.',
    'agdos_advs' : 'WILLIAM LIMA CABRAL E OUTRO(A/S)',
    'procedencia_orgao' : 'TRIBUNAL DE JUSTIÇA ESTADUAL',
    'procedencia_estado' : 'SÃO PAULO',
    'andamentos' : [
        { 'data' : '02/09/2010', 'andamento' : 'Baixa definitiva dos autos, Guia nº', 'orgao_julgador' : '', 'obs' : 'Guia 6776 - TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO', 'documento' : '' },      
        { 'data' : '23/08/2010', 'andamento' : 'Transitado(a) em julgado', 'orgao_julgador' : '', 'obs' : 'em 17/08/2010. ', 'documento' : '' }
    ],
    'data_de_entrada' : '01/04/1996',
    'procedencia_numero' : 'AG 23174010'
}

base_url = "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente="
no_incidente = "2312886"

url = base_url+str(no_incidente)
html = urllib.urlopen(url)

soup = parse(html).getroot()

data = {}

data['titulo'] = soup.cssselect('#detalheProcesso h3 strong')[0].text
data['tipo_de_processo'] = data['titulo'].split('-')[1]


numero_do_processo_com_iniciais = data['titulo'].split('-')[0] #'AI 553939'
numero_do_processo_sem_iniciais = numero_do_processo_com_iniciais.split()[1] #553939
data['numero_de_processo'] = numero_do_processo_sem_iniciais

data['origem'] = soup.cssselect('.comum tr')[0].cssselect('td')[1].text_content()

data['relator'] = soup.cssselect('.comum td')[3].text_content()

data['agtes'] = soup.cssselect('.comum strong')[2].text

data['agtes_advs'] = soup.cssselect('.comum strong')[3].text
data['agdos'] = soup.cssselect('.comum strong')[4].text
data['agdos_advs'] = soup.cssselect('.comum strong')[5].text

data['andamentos'] = []

linhas_de_andamento = soup.cssselect(".resultadoAndamentoProcesso tr")

for linha in linhas_de_andamento[1:]:
    
    
    colunas = linha.cssselect('td')

    
    andamento = {
        'data' : colunas[0].text_content().strip(),
        'andamento' : colunas[1].text_content().strip(),
        'orgao_julgador' : colunas[2].text_content().strip(),
        'obs' : colunas[3].text_content().strip(),
        'documento' : colunas[4].text_content().strip() }

    data['andamentos'].append(andamento)

data['url'] = url



pagina_de_detalhes = urllib.urlopen("http://www.stf.jus.br/portal/processo/verProcessoDetalhe.asp?incidente=" + str(no_incidente))


soup_da_pagina_de_detalhes = parse(pagina_de_detalhes).getroot()

x = soup_da_pagina_de_detalhes
tabela_de_procedencias = x.cssselect("#abaAcompanhamentoConteudoResposta .comum")[0]
conteudo_da_tabela = tabela_de_procedencias.cssselect("b")

data['procedencia_numero'] = conteudo_da_tabela[1].text
data['procedencia_orgao'] = conteudo_da_tabela[2].text
data['procedencia_estado'] = conteudo_da_tabela[3].text
print data['procedencia_orgao']
print data['procedencia_estado']
print data['procedencia_numero']

scraperwiki.sqlite.save(["titulo"], data)

