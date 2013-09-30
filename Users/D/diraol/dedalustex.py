import scraperwiki
import re
from BeautifulSoup import BeautifulSoup



class bibtex:

    tipo = ""
    titulo = ""
    editora = ""
    ano = ""
    editores = ""
    autores = ""
    volume = ""
    numero = ""
    paginas = ""
    serie = ""
    endereco = ""
    edicao = ""
    mes = ""
    DOI = ""
    ISBN = ""
    palavras_chave = ""







#COMO MONTAR AS URLS??....

#BUSCAR O HTML
url_livro = "http://dedalus.usp.br/F/?func=full-set-set&set_number=140840&set_entry=000001&format=999"

#PARSEAR O HTML
html_livro = scraperwiki.scrape(url_livro) #pegando o html da página
livroSoup = BeautifulSoup(html_livro)
tabelas = livroSoup.findAll("table")


#ENCONTRAR A TABELA QUE CONTEM OS DADOS
tabela_queremos = tabelas[6]


#OBJETIFICAR OS DADOS
publicacao_dict={}
for linha in tabela_queremos.findAll("tr"):
    coluna=linha.findAll("td")
    if coluna[0].text != "&nbsp;":
        chave = coluna[0].text.replace("&nbsp;", " ").strip()
    if chave in publicacao_dict:
        publicacao_dict[chave].append(coluna[1].text.replace("&nbsp;", " ").strip())
    else:
        publicacao_dict[chave]=[coluna[1].text.replace("&nbsp;", " ").strip()]



#print livro_dict
    

#TRANSFORMAR DADOS EM BIBTEX

bibtex_saida = bibtex()
for chave in publicacao_dict.keys():
    print chave





#html_cgs = scraperwiki.scrape(cgs_url) #pegando o html da página
    #cgsSoup = BeautifulSoup(html_cgs) #transformando num objeto do BeautifulSoup
#cgs = cgsSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"} ) #usar o BeautifulSoup para pegar a lista de cgs e seus códigos
import scraperwiki
import re
from BeautifulSoup import BeautifulSoup



class bibtex:

    tipo = ""
    titulo = ""
    editora = ""
    ano = ""
    editores = ""
    autores = ""
    volume = ""
    numero = ""
    paginas = ""
    serie = ""
    endereco = ""
    edicao = ""
    mes = ""
    DOI = ""
    ISBN = ""
    palavras_chave = ""







#COMO MONTAR AS URLS??....

#BUSCAR O HTML
url_livro = "http://dedalus.usp.br/F/?func=full-set-set&set_number=140840&set_entry=000001&format=999"

#PARSEAR O HTML
html_livro = scraperwiki.scrape(url_livro) #pegando o html da página
livroSoup = BeautifulSoup(html_livro)
tabelas = livroSoup.findAll("table")


#ENCONTRAR A TABELA QUE CONTEM OS DADOS
tabela_queremos = tabelas[6]


#OBJETIFICAR OS DADOS
publicacao_dict={}
for linha in tabela_queremos.findAll("tr"):
    coluna=linha.findAll("td")
    if coluna[0].text != "&nbsp;":
        chave = coluna[0].text.replace("&nbsp;", " ").strip()
    if chave in publicacao_dict:
        publicacao_dict[chave].append(coluna[1].text.replace("&nbsp;", " ").strip())
    else:
        publicacao_dict[chave]=[coluna[1].text.replace("&nbsp;", " ").strip()]



#print livro_dict
    

#TRANSFORMAR DADOS EM BIBTEX

bibtex_saida = bibtex()
for chave in publicacao_dict.keys():
    print chave





#html_cgs = scraperwiki.scrape(cgs_url) #pegando o html da página
    #cgsSoup = BeautifulSoup(html_cgs) #transformando num objeto do BeautifulSoup
#cgs = cgsSoup.findAll( "span", {"class" : "txt_arial_8pt_gray"} ) #usar o BeautifulSoup para pegar a lista de cgs e seus códigos
