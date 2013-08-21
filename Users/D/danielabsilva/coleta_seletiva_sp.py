###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
import time

# opa! Essa função define a ordem das colunas!
scraperwiki.sqlite.save_var('data_columns', ['tipo', 'cep', 'logradouro', 'distrito', 'inicio', 'fim', 'subprefeitura', 'domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'empresa', 'periodo', 'turno', 'frequencia', 'id'])

#descomentar para 'restar o scrapper'
#actual_id = scraperwiki.metadata.save('actual_id', 1)


#tenta recomeçar o processo do último id scrappeado
last_id = 276597

# retrieve a page
#ids = [241361, 2, 223781]


base_url = "http://www3.prefeitura.sp.gov.br/limpeza_urbana/FormsPublic/LimpezaRuaDetalhe.aspx?ID="

def rockndroll(actual_id):
    count = 0
    print "Iniciando a partir do id " + str(actual_id)
    for id in range(int(actual_id), last_id): 
        count = count + 1
        if count == 10:
            scraperwiki.sqlite.save_var('actual_id', id)
            print 'Salvando progresso... id ' + str(id)
            #time.sleep(300)
            #rockndroll_allnight()
            count = 0
        
        starting_url = base_url + str(id)
        html = unicode(scraperwiki.scrape(starting_url), 'utf-8', 'ignore')
        soup = BeautifulSoup(html, fromEncoding='utf-8')
    
        if soup.find("legend",text="Coleta de lixo seletiva"): 
        
            data = {}
            data["tipo"] = "coleta_seletiva"
            data["cep"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblCep"}).text
            data["lograduoro"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLogradouro"}).text
            data["distrito"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDistrito"}).text
            data["inicio"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblInicio"}).text
            data["fim"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblFim"}).text
            data["subprefeitura"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSubprefeitura"}).text
    
            data["domingo"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelDOM"}).text
            data["segunda"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelSEG"}).text
            data["terca"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelTER"}).text
            data["quarta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelQUA"}).text
            data["quinta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelQUI"}).text
            data["sexta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelSEX"}).text
            data["sabado"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelSAB"}).text
    
            data["empresa"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblEmpresaSel"}).text
            data["periodo"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSelPeriodo"}).text
    
    #especifico varricao
            data["turno"] = ''
            data["frequencia"] = ''
    
            data["id"] = re.search("ID=([0-9]*)", starting_url).group(1)
    
            scraperwiki.datastore.save(["id"], data)
    
    
        elif soup.find("legend", text="Coleta de lixo domiciliar"):
            data = {}
            data['tipo'] = "coleta_domiciliar"
            data["cep"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblCep"}).text
            data["lograduoro"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLogradouro"}).text
            data["distrito"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDistrito"}).text
            data["inicio"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblInicio"}).text
            data["fim"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblFim"}).text
            data["subprefeitura"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSubprefeitura"}).text
    
            data["domingo"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomDOM"}).text
            data["segunda"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomSEG"}).text
            data["terca"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomTER"}).text
            data["quarta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomQUA"}).text
            data["quinta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomQUI"}).text
            data["sexta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomSEX"}).text
            data["sabado"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomSAB"}).text
    
            data["empresa"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblEmpresaDom"}).text
            data["periodo"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDomPeriodo"}).text
    
    #especifico varricao
            data["turno"] = ''
            data["frequencia"] = ''
    
            data["id"] = re.search("ID=([0-9]*)", starting_url).group(1)
    
            scraperwiki.datastore.save(["id"], data)        
    
        else:
            data = {}
            data['tipo'] = "varricao"
            data["cep"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblCep"}).text
            data["lograduoro"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLogradouro"}).text
            data["distrito"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblDistrito"}).text
            data["inicio"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblInicio"}).text
            data["fim"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblFim"}).text
            data["subprefeitura"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblSubprefeitura"}).text
    
            data["domingo"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrDOM"}).text
            data["segunda"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrSEG"}).text
            data["terca"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrTER"}).text
            data["quarta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrQUA"}).text
            data["quinta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrQUI"}).text
            data["sexta"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrSEX"}).text
            data["sabado"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrSAB"}).text
    
            data["empresa"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblEmpresaVarr"}).text
            
    #especifico coletas
            data["periodo"] = ' '
            
    
    #especifico varricao
            data["frequencia"] = soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblVarrFrequencia"}).text   
            turno_m = soup.find("span", { "id" : "ctl00_ContentPlaceHolder1_lblTurnoM"}).text
            turno_v = soup.find("span", { "id" : "ctl00_ContentPlaceHolder1_lblTurnoV"}).text
            turno_n = soup.find("span", { "id" : "ctl00_ContentPlaceHolder1_lblTurnoN"}).text
            data["turno"] = [turno_m, turno_v, turno_n]
    
            data["id"] = re.search("ID=([0-9]*)", starting_url).group(1)
    
            scraperwiki.datastore.save(["id"], data)

def rockndroll_allnight():
    start_id = scraperwiki.sqlite.get_var('actual_id', 1)
    try:
        rockndroll(start_id)
        print 'oops'
    except:
        time.sleep(900)
        rockndroll_allnight()

rockndroll_allnight()