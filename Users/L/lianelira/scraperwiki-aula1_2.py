import scraperwiki #importa biblioteca que permite que a gente salve os nossos resultados
from lxml.html import parse #biblioteca do python - html parse é um método que torna isso navegável,#parse transforma um documento html em um doc q o python consegue entender e manipular. A variável ps (nome escolhido livremente).
import re #regular expressions

url_busca = "http://busca.globo.com/Busca/oglobo/?query=hacker"

ps_busca = parse(url_busca).getroot()
print ps_busca 
#isso acabou não sendo usado


links = ['http://oglobo.globo.com/rio/mat/2011/07/13/pm-anuncia-prisao-do-maior-hacker-do-rio-de-janeiro-924898599.asp','http://oglobo.globo.com/tecnologia/mat/2011/07/15/meu-amigo-foi-atacado-por-um-hacker-sistema-da-microsoft-tenta-evitar-roubo-de-senhas-no-hotmail-924914313.asp', 'http://oglobo.globo.com/pais/noblat/posts/2011/06/28/hacker-mesmo-outra-coisa-389024.asp', 'http://oglobo.globo.com/pais/mat/2011/06/30/policia-federal-abre-inquerito-para-investigar-invasao-de-hacker-ao-mail-da-presidente-dilma-durante-eleicao-924804515.asp']

lista2 = ['banana', 'maça'] #o que está entre aspas diz q é texto, se não estiver, será entendido como variável, que deve ser especificado antes. Exemplo abaixo:

banana = 'banana'
lista3 = [banana]

#isto abaixo é um loopi(?) ou laço
for url in links:
    if re.match('.*/mat/.*', url): #match = 
        ps = parse(url).getroot() #get pega os atributos dessa indicação. Usou o parse, use o getroot!

#parse transforma um documento html em um doc q o python consegue entender e manipular. A variável é um nome escolhido livremente).
#[] é lista
#{} é dicionário ex: {'fruta' : 'banana', 'cor': 'amarela'}. É bom começar com {} vazias e ligando a uma variável, por exemplo, "data".
        
        data = {}
        
        data['titulo'] = ps.cssselect('#ltintb h3')[0].text_content() #conteúdo de texto que estiver dentro do colchete, que sempre é uma lista, ainda q com um elemento só. Aqui disse: pegue o 0 e me retorne o conteúdo do texto
        data['autor'] = ps.cssselect('#ltintb cite')[0].text_content()
        data['texto'] = '' #variável vazia - como aqui são vários parágrafos (p'), tem q dizer: para cada parágrafo nessa lista, faça com q o texto se some ao texto dos parágrafos anteriores, soma tudo dentro da mesma variável, é uma variável aberta que vai sendo preenchida
        for paragrafo in ps.cssselect('#ltintb p'): 
            data['texto'] = data['texto'] + paragrafo.text_content()

#len á uma forma de ver qto parágrafos tem, dando para escolher quais eu quero. Vai sempre retornar um número.
#a função string (str) transforma um número em um texto. 
#Ex: numero = 13, se ponho: numero + 1, retorna 14
#Ex" numero = '13', se ponho: numero + 1, dá erro, mas se ponho: numero + '1', retorna '131'
        
        data['editoria'] = ps.cssselect('#vrsedt a')[0].text_content()

        data['editoria_link'] = 'http://oglobo.globo.com' + ps.cssselect('#vrsedt a')[0].get('href')
        
        scraperwiki.sqlite.save(['titulo'], data) #identificador único (importante): dá identidade para as informações colhidas, faz com que duas coisas iguais não se repitam e, principalmente, com q coisas diferentes não se sobreescrevam. Ele salva uma entrada (uma linha na tabela) para cada item desejado. É sempre uma chave dentro do dicionário, já definido. o dicionário usado é cologado depois do item desejado - (['titulo'], DATA). Ao escolher, deve ser uma informação q realmente distingua um dado do outro.
    else:
        print 'essa url nao eh noticia ' + url
