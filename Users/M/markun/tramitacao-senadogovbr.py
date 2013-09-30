###############################################################################
# Basic scraper
###############################################################################
import scraperwiki
import urllib
import re
#from BeautifulSoup import BeautifulSoup


# retrieve a page
materia = '96674'
starting_url = 'http://www.senado.gov.br/atividade/materia/detalhes.asp?p_cod_mate=' + materia + '&p_sort=DESC&p_sort2=D&cmd=sort'
html = urllib.urlopen(starting_url).read()


#print html
print type(html)
soup = BeautifulSoup(html)
print soup
#usar o BeautifulSoup para pegar o numero do projeto
proj_name = soup.find("div", "titulocaixa_abas" )

# usar o BeautifulSoup para pegar a tramitacao do projeto
tramitacao = soup.find("div", { "id" : "DIV_TRAMITACAO" }) 
tramite = tramitacao.findAll("div", { "style" : "clear:left; width:100%; padding-top:10px; display:block;"})
for div in tramite:

    data = {}
    data['id'] = div.find("div", { "style" : "clear:both; width:100%;"})['id']
    data['date'] = div.find("div", "label").text
    data['where'] = div.find("div", { "style" : "float:left; width:62%; padding-left:10px;" }).text
#POG barato porque não consegui verificar acentos.
    if (div.find("div",text=re.compile("Situa*."))) :
        data['status'] = div.find("div", { "style" : "float:left; width:81%; padding-left:10px;" }).text
    else :
        data['status'] = "-"
    data['action'] = div.find("span", "textoAcao").text
    data['proj_name'] = proj_name.text

#milestone
#    if (re.search(re.compile("Recebido nest*."), data['action'])) :
#        data['milestone'] = 1  


#   salva links para diario e textos
    links = re.findall(r'<a(.+?)href="(.+?)"(.+?)>', str(div))
    for link in links:
        full_link = "http://www.senado.gov.br/atividade/materia/%s" % link[1]
        if link[1].startswith('getTexto'):
            data['link_texto'] = full_link
        elif link[1].startswith('verDiario'):
            data['link_diario'] = full_link 

    
    scraperwiki.datastore.save(['id'], data) # save the records one by one

#falta ainda os textos e os links###############################################################################
# Basic scraper
###############################################################################
import scraperwiki
import urllib
import re
#from BeautifulSoup import BeautifulSoup


# retrieve a page
materia = '96674'
starting_url = 'http://www.senado.gov.br/atividade/materia/detalhes.asp?p_cod_mate=' + materia + '&p_sort=DESC&p_sort2=D&cmd=sort'
html = urllib.urlopen(starting_url).read()


#print html
print type(html)
soup = BeautifulSoup(html)
print soup
#usar o BeautifulSoup para pegar o numero do projeto
proj_name = soup.find("div", "titulocaixa_abas" )

# usar o BeautifulSoup para pegar a tramitacao do projeto
tramitacao = soup.find("div", { "id" : "DIV_TRAMITACAO" }) 
tramite = tramitacao.findAll("div", { "style" : "clear:left; width:100%; padding-top:10px; display:block;"})
for div in tramite:

    data = {}
    data['id'] = div.find("div", { "style" : "clear:both; width:100%;"})['id']
    data['date'] = div.find("div", "label").text
    data['where'] = div.find("div", { "style" : "float:left; width:62%; padding-left:10px;" }).text
#POG barato porque não consegui verificar acentos.
    if (div.find("div",text=re.compile("Situa*."))) :
        data['status'] = div.find("div", { "style" : "float:left; width:81%; padding-left:10px;" }).text
    else :
        data['status'] = "-"
    data['action'] = div.find("span", "textoAcao").text
    data['proj_name'] = proj_name.text

#milestone
#    if (re.search(re.compile("Recebido nest*."), data['action'])) :
#        data['milestone'] = 1  


#   salva links para diario e textos
    links = re.findall(r'<a(.+?)href="(.+?)"(.+?)>', str(div))
    for link in links:
        full_link = "http://www.senado.gov.br/atividade/materia/%s" % link[1]
        if link[1].startswith('getTexto'):
            data['link_texto'] = full_link
        elif link[1].startswith('verDiario'):
            data['link_diario'] = full_link 

    
    scraperwiki.datastore.save(['id'], data) # save the records one by one

#falta ainda os textos e os links