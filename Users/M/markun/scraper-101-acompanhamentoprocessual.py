import scraperwiki, urllib
from lxml.html import parse

# A primeira coisa a fazer eh encontrar a URL da informacao que queremos raspar
url_original = "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente=2312886"

#Vamos agora definir o modelo dos dados que queremos extrair, usando um dicionario python [1].
#A ideia eh pensar em todas as informacoes que queremos extrair e como elas vao ficar armazenadas

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
    # Os andamentos do processo sao varios e tem um formato padrao. Vamos armazenar uma variavel 'lista' do python. [2]
    'andamentos' : [
        { 'data' : '02/09/2010', 'andamento' : 'Baixa definitiva dos autos, Guia nº', 'orgao_julgador' : '', 'obs' : 'Guia 6776 - TRIBUNAL DE JUSTIÇA DO ESTADO DE SÃO PAULO', 'documento' : '' },      
        { 'data' : '23/08/2010', 'andamento' : 'Transitado(a) em julgado', 'orgao_julgador' : '', 'obs' : 'em 17/08/2010. ', 'documento' : '' }
    ],
    'data_de_entrada' : '01/04/1996',
    'procedencia_numero' : 'AG 23174010'
}


#Agora vamos de fato comecar os trabalhos
#Quebramos a URL em partes; a base da URL e o numero variavel de acordo com o processo
base_url = "http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?incidente=" 
no_incidente = "2312886"

#str(5) transforma 5 em "5"
#int("5") transforma "5" em 5
#Usamos o metodo urlopen da lib urllib para abrir uma url e salvar o resultado na variavel 'html'

url = base_url+str(no_incidente)
html = urllib.urlopen(url)

#Usamos o metodo parse da lib lxml para transformar o documento contido na variavel 'html' em um objeto python
soup = parse(html).getroot()

#Agora temos que vasculhar nosso objeto 'soup' em busca das informacoes que escolhemos la em cima.

# Vamos criar um dicionario vazio para armazenar as informacoes e ir pegando linha por linha.
data = {}

# O truque do scraping eh encontrar algo que identifique onde esta aquela determinada informacao dentro da pagina de maneira unica. Para isso existem varias tecnicas... a que utilizamos aqui sao os seletores de CSS [3] a mesma que a gente utiliza quando quer estilar um elemento em usando CSS.

#O metodo cssselect permite que a gente passe um seletor de css como argumento e retorna uma lista [2] de itens econtrados.

#Vasculhando o documento descobri que o titulo sempre esta dentro da div com id #detalheProcesso dentro de um h3, dentro de um strong
#Se a gente procurar soh pelo strong, vamos encontrar varias outras informacoes. Mesma coisa se a gente procurar soh pelo h3.
#O atributo .text retorna o texto dentro de uma tag html. No caso, o que esta dentro do <h3></h3>

data['titulo'] = soup.cssselect('#detalheProcesso h3 strong')[0].text
data['tipo_de_processo'] = data['titulo'].split('-')[1]


numero_do_processo_com_iniciais = data['titulo'].split('-')[0] #'AI 553939'
numero_do_processo_sem_iniciais = numero_do_processo_com_iniciais.split()[1] #553939
data['numero_de_processo'] = numero_do_processo_sem_iniciais

# As outras informacoes estao dentro de uma tabela com a classe .comum; vou usar varios jeitos diferentes para extrair essas informacoes.

#Pegando o primeiro 'tr' da tabela com a classe .comum e dentro desse, o segundo td, aqui eu uso o metodo text_content()
# ao inves do atributo .text pq o texto esta dentro da tag <strong> e nao direto na <td>
data['origem'] = soup.cssselect('.comum tr')[0].cssselect('td')[1].text_content()

#Pegando direto o quarto td da tabela com a classe .comum
data['relator'] = soup.cssselect('.comum td')[3].text_content()

#Pegando o terceiro negrito da tabela
data['agtes'] = soup.cssselect('.comum strong')[2].text

#Esse parece ser o jeito mais simples, vamos nele.
data['agtes_advs'] = soup.cssselect('.comum strong')[3].text
data['agdos'] = soup.cssselect('.comum strong')[4].text
data['agdos_advs'] = soup.cssselect('.comum strong')[5].text

#Agora vamos montar nossa lista com os andamentos. Primeiro montamos uma lista vazia.
data['andamentos'] = []

#Agora criamos uma lista das linhas onde estao as informacoes de andamento e armazenamos ela temporariamente na variavel 'linha_andamentos'
linhas_de_andamento = soup.cssselect(".resultadoAndamentoProcesso tr")

#Agora vamos usar o 'for' para passar por cada linha, extrair os andamentos e adicionar o dicionario final na nossa lista data['andamentos']
#Utilizamos o [1:] pq queremos pular o primeiro elemento, que no html eh o titulo das colunas

for linha in linhas_de_andamento[1:]:
    
    #vamos separar as colunas
    colunas = linha.cssselect('td')

    #criamos um dicionario para esse andamento - dessa vez vou preencher tudo de uma soh vez
    #utilizamos o .strip para remover caracteres em branco
    andamento = { 
        'data' : colunas[0].text_content().strip(),
        'andamento' : colunas[1].text_content().strip(),
        'orgao_julgador' : colunas[2].text_content().strip(),
        'obs' : colunas[3].text_content().strip(),
        'documento' : colunas[4].text_content().strip() }
    
    #agora basta adicionar nosso andamento no final da lista de andamentos
    data['andamentos'].append(andamento)

data['url'] = url

#Novos conteudos - da aba de detalhes - procedencias
#Pegando minha tabela de procedencias da nova pagina!

#Carrego a outra pagina
pagina_de_detalhes = urllib.urlopen("http://www.stf.jus.br/portal/processo/verProcessoDetalhe.asp?incidente=" + str(no_incidente))

#Uso o lxml para transformar em objeto python
soup_da_pagina_de_detalhes = parse(pagina_de_detalhes).getroot()

#Agora ja posso usar minhas funcoes na nova pagina
x = soup_da_pagina_de_detalhes 
tabela_de_procedencias = x.cssselect("#abaAcompanhamentoConteudoResposta .comum")[0]
conteudo_da_tabela = tabela_de_procedencias.cssselect("b")

data['procedencia_numero'] = conteudo_da_tabela[1].text
data['procedencia_orgao'] = conteudo_da_tabela[2].text
data['procedencia_estado'] = conteudo_da_tabela[3].text
print data['procedencia_orgao']
print data['procedencia_estado']
print data['procedencia_numero']

    #IMPORTANTE - Nao estamos pegando os links dos despachos! Mas para nao complicar, vou deixar desse jeito por enquanto.

    #Agora que ja raspamos todos os campos relevantes, basta salvar
scraperwiki.sqlite.save(["titulo"], data)

# [1] Sobre dicionarios: http://yuji.wordpress.com/2008/05/14/python-basics-of-python-dictionary-and-looping-through-them/
# [2]  Sobre listas: http://effbot.org/zone/python-list.htm
