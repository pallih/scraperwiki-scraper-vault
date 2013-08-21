import scraperwiki
# pegar o método parse da biblioteca lxml
from lxml.html import parse


# a URL é uma string, uma sequencia de caracteres, que pode a partir de agora ser referida como intro
intro = 'http://www.rollingstone.com/music/lists/500-greatest-albums-of-all-time-19691231' 

# uma lista vazia (por enquanto)
albuns = []

# interpreta (parseia) o conteúdo do endereço 'intro', depois pega a raiz do html e chama de doc :)
doc = parse(intro).getroot()
# o doc tem um método make_links_absolute que transforma links relativos (/pagina) em links absolutos (http://exemplo.com/pagina)
doc.make_links_absolute()

# usando um seletor CSS (oba!), cssselect retorna uma lista de elementos
# pra cada um deles, chamado de 'elemento', roda o código identado
for elemento in doc.cssselect('#heavyListUL .listItem'):
    # um dicionário, uma lista onde cada item tem um nome. começa vazio.
    album = {}
    # pega o conteúdo de texto do primeiro item selecionado e salva como 'posicao' dentro do dicionario
    album['posicao'] = elemento.cssselect('.sliderNo')[0].text_content()
    # usa o método get pra pegar o atributo href do primeiro link e salvo como 'link' no dicionario 'album'
    album['link'] = elemento.cssselect('a')[0].get('href')

    # hora de scrapear cada album
    paginadoalbum = parse(album['link']).getroot()
    # pegando album e artista, que estão no h3 separados por ' - '
    tituloeartista = paginadoalbum.cssselect('.listItemDescriptonDiv h3')[0].text_content()
    # abrindo uma exceção porque o site da rollingstone também erra.
    if (album['posicao'] == '262'):
        album['titulo'] = "Workingman's Dead"
        album['artista'] = 'Grateful Dead'
    # outra exceção :/
    elif (album['posicao'] == '48'):
        album['titulo'] = 'It Takes a Nation of Millions to Hold Us Back'
        album['artista'] = 'Public Enemy'
    else:
        # quebrando a string no ' - ' e pegando o primeiro pedaço
        album['titulo'] = tituloeartista.split(' - ')[0]
        # quebrando a string no ' - ' e pegando o segundo pedaço
        album['artista'] = tituloeartista.split(' - ')[1]

    # o texto do paginador avacalha a resenha :(
    paginador = paginadoalbum.cssselect('.listPagination')[0].text_content()
    # então o jeito é quebrar a string no paginador e pegar o pedaço sem o paginador
    album['resenha'] = paginadoalbum.cssselect('.listPageContentInfo')[0].text_content().partition(paginador)[2]
    # pega a url da imagem
    album['capa'] = paginadoalbum.cssselect('.listPageContentImage img')[0].get('src')
    # joga o dicionario 'album' dentro da lista 'albuns'
    albuns.append(album)

# salva no scraperwiki, o unique_keys é o valor usado pra identificar cada item no banco de dados
scraperwiki.sqlite.save(unique_keys=['posicao'], data=albuns)
