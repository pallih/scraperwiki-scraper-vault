# Blank Python
import urllib
import BeautifulSoup
import scraperwiki
import re
import sys
import json

def listEstados():
    html = urllib.urlopen('http://www.anp.gov.br/preco/prc/Resumo_Por_Estado_Index.asp')
    soup = BeautifulSoup.BeautifulSoup(html)
    soup = soup.find("select", { 'name' : 'selEstado' })
    states_list = soup.findAll("option")
    states = []
    for state in states_list:
        states.append(state['value'])
    print states

def getCidades(soup, state):
    #soup = soup.find("table", "table_padrao scrollable_table")
    rows = soup.table.findAll("tr")
    header_row = rows.pop(0)
    
    #pop top header rows
    rows.pop(0)
    rows.pop(0)
    for row in rows:
        cell = row.findAll("td")
        data = {}
        data['id'] = re.search("\('(.*)'\);", cell[0].a['href']).group(1)
        data['state'] = state
        data['postos'] = cell[1].text
        scraperwiki.sqlite.save(["id"], data, table_name='cities')

def processaCidades(states_list):
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Index.asp"
    post01 = "selSemana=656*De+08%2F01%2F2012+a+14%2F01%2F2012&desc_Semana=de+08%2F01%2F2012+a+14%2F01%2F2012"
    post02 = "&cod_Semana=656&tipo=1&Cod_Combustivel=undefined&selCombustivel=487*Gasolina"
    sel_estado = "&selEstado="

    for state in states_list:
        #post_args = post01+post02+sel_estado+state
        #print 'URL ' + base_url+"?"+post_args 
        html = urllib.urlopen(base_url)
        #print 'HTML ' + html
        soup = BeautifulSoup.BeautifulSoup(html)

        print soup.find("input", { 'name' : 'selSemana' })['value']
        print soup.find("input", { 'name' : 'desc_Semana' })['value']
        print soup.find("input", { 'name' : 'cod_Semana' })['value']

        print 'Pegando dados de ' + state
        #getCidades(soup, state)

def registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error):
        error = {}
        error['id'] = cod_municipio + '-' + cod_combustivel + '-' + cod_semana
        error['cod_municipio'] = cod_municipio
        error['cod_combustivel'] = cod_combustivel
        error['cod_semana'] = cod_semana
        error['msg'] = scrape_error
        scraperwiki.sqlite.save(["id"], error, table_name='failed_scrapes')

def urlPosto(cod_semana, cod_combustivel, cod_municipio):
    post_arg = "cod_semana=" + str(cod_semana)
    post_arg += "&desc_semana=De+08%2F01%2F2012+a+14%2F01%2F2012"
    post_arg += "&cod_combustivel=" + str(cod_combustivel)
    post_arg += "&desc_combustivel=+-+Gasolina+R%24%2Fl"
    post_arg += "&selMunicipio=" + cod_municipio
    post_arg += "&tipo=1"
    return post_arg


def processaPostos(cities_list, fuel_list):
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Posto.asp"
    for city in cities_list['data']:
        for tipo in fuel_list:
            print 'Pegando dados de ' + fuel_list[tipo] + ' dos postos de ' + city[0]
            post_args = urlPosto(618, tipo, city[0]) #primeiro registro 236?
            html = urllib.urlopen(base_url, post_args)
            soup = BeautifulSoup.BeautifulSoup(html)
            state = re.search("([A-Z][A-Z]).*", city[1]).group(1)
            getPostos(soup, state)
        
def geocode(address, city, state):
    fuel_address = address + ',' + city + ',' + state
    url = 'http://maps.google.com/maps/api/geocode/json?sensor=false&region=br&address='+fuel_address
    results = urllib.urlopen(url)
    results = json.load(results)
    return results

def getPostos(soup, state):
    cod_municipio = soup.find("input", { 'name' : 'municipio' })['value']
    cod_combustivel = soup.find("input", { 'name' : 'Cod_Combustivel' })['value']
    cod_semana = soup.find("input", { 'name' : 'cod_semana' })['value']
    cidade = soup.find("input", { 'name' : 'desc_municipio' })['value']
    id = 0
    rows = soup.table.findAll("tr")
    header_rows = rows.pop(0)
    try:
        rows.pop(0)
        for row in rows:
            cell = row.findAll("td")
            data = {}
            data['id'] = cod_municipio + '-' + cod_combustivel + '-' + cod_semana + '-' + str(id)
            data['tipo'] = fuel_list[int(cod_combustivel)]
            data['city'] = cidade
            data['state'] = state
            data['razao_social'] = cell[0].text
            data['endereco'] = cell[1].text
            data['bairro'] = cell[2].a.text
            data['latlng'] = geocode(data['endereco'],data['city'],data['state'])
            if cod_combustivel == '462': #GLP
                print 'Getting GLP:' + str(cod_combustivel)
                data['bandeira'] = '-'
                data['distribuidora'] = cell[3].text
                data['preco_venda'] = cell[4].text
                data['preco_compra'] = cell[5].text
                data['modalidade_de_compra'] = cell[6].text
                data['fornecedor'] = ''
                data['data_coleta'] = cell[7].text
                scraperwiki.sqlite.save(["id"], data, table_name='gas_price')
            else:           
                print 'Getting Other:' + str(cod_combustivel)
                data['bandeira'] = cell[3].text
                data['distribuidora'] = '-'
                data['preco_venda'] = cell[4].text
                data['preco_compra'] = cell[5].text
                data['modalidade_de_compra'] = cell[6].text
                data['fornecedor'] = cell[7].text
                data['data_coleta'] = cell[8].text
                scraperwiki.sqlite.save(["id"], data, table_name='gas_price')
            id += 1
    except:
        scrape_error = str(sys.exc_info()[1])
        print scrape_error
        registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error)
        return 0
         

states_list = ['AC*ACRE', 'AL*ALAGOAS', 'AP*AMAP\xc3\x81', 'AM*AMAZONAS', 'BA*BAHIA', 'CE*CEAR\xc3\x81', 'DF*DISTRITO@FEDERAL', 'ES*ESP\xc3\x8dRITO@SANTO', 'GO*GOI\xc3\x81S', 'MA*MARANH\xc3\x83O', 'MT*MATO@GROSSO', 'MS*MATO@GROSSO@DO@SUL', 'MG*MINAS@GERAIS', 'PR*PARAN\xc3\x81', 'PB*PARA\xc3\x8dBA', 'PA*PAR\xc3\x81', 'PE*PERNAMBUCO', 'PI*PIAU\xc3\x8d', 'RJ*RIO@DE@JANEIRO', 'RN*RIO@GRANDE@DO@NORTE', 'RS*RIO@GRANDE@DO@SUL', 'RO*ROND\xc3\x94NIA', 'RR*RORAIMA', 'SC*SANTA@CATARINA', 'SE*SERGIPE', 'SP*S\xc3\x83O@PAULO', 'TO*TOCANTINS']

#states_list =['SC*SANTA@CATARINA']

try:
    cities_list = scraperwiki.sqlite.execute('select id, state from cities')
    print cities_list
except:
    processaCidades(states_list)
    cities_list = scraperwiki.sqlite.execute('select id, state from cities')

fuel_list = {487 : 'Gasolina', 643 : 'Etanol', 476 : 'GNV', 532 : 'Diesel', 462 : 'GLP'}

processaPostos(cities_list, fuel_list)# Blank Python
import urllib
import BeautifulSoup
import scraperwiki
import re
import sys
import json

def listEstados():
    html = urllib.urlopen('http://www.anp.gov.br/preco/prc/Resumo_Por_Estado_Index.asp')
    soup = BeautifulSoup.BeautifulSoup(html)
    soup = soup.find("select", { 'name' : 'selEstado' })
    states_list = soup.findAll("option")
    states = []
    for state in states_list:
        states.append(state['value'])
    print states

def getCidades(soup, state):
    #soup = soup.find("table", "table_padrao scrollable_table")
    rows = soup.table.findAll("tr")
    header_row = rows.pop(0)
    
    #pop top header rows
    rows.pop(0)
    rows.pop(0)
    for row in rows:
        cell = row.findAll("td")
        data = {}
        data['id'] = re.search("\('(.*)'\);", cell[0].a['href']).group(1)
        data['state'] = state
        data['postos'] = cell[1].text
        scraperwiki.sqlite.save(["id"], data, table_name='cities')

def processaCidades(states_list):
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Index.asp"
    post01 = "selSemana=656*De+08%2F01%2F2012+a+14%2F01%2F2012&desc_Semana=de+08%2F01%2F2012+a+14%2F01%2F2012"
    post02 = "&cod_Semana=656&tipo=1&Cod_Combustivel=undefined&selCombustivel=487*Gasolina"
    sel_estado = "&selEstado="

    for state in states_list:
        #post_args = post01+post02+sel_estado+state
        #print 'URL ' + base_url+"?"+post_args 
        html = urllib.urlopen(base_url)
        #print 'HTML ' + html
        soup = BeautifulSoup.BeautifulSoup(html)

        print soup.find("input", { 'name' : 'selSemana' })['value']
        print soup.find("input", { 'name' : 'desc_Semana' })['value']
        print soup.find("input", { 'name' : 'cod_Semana' })['value']

        print 'Pegando dados de ' + state
        #getCidades(soup, state)

def registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error):
        error = {}
        error['id'] = cod_municipio + '-' + cod_combustivel + '-' + cod_semana
        error['cod_municipio'] = cod_municipio
        error['cod_combustivel'] = cod_combustivel
        error['cod_semana'] = cod_semana
        error['msg'] = scrape_error
        scraperwiki.sqlite.save(["id"], error, table_name='failed_scrapes')

def urlPosto(cod_semana, cod_combustivel, cod_municipio):
    post_arg = "cod_semana=" + str(cod_semana)
    post_arg += "&desc_semana=De+08%2F01%2F2012+a+14%2F01%2F2012"
    post_arg += "&cod_combustivel=" + str(cod_combustivel)
    post_arg += "&desc_combustivel=+-+Gasolina+R%24%2Fl"
    post_arg += "&selMunicipio=" + cod_municipio
    post_arg += "&tipo=1"
    return post_arg


def processaPostos(cities_list, fuel_list):
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Posto.asp"
    for city in cities_list['data']:
        for tipo in fuel_list:
            print 'Pegando dados de ' + fuel_list[tipo] + ' dos postos de ' + city[0]
            post_args = urlPosto(618, tipo, city[0]) #primeiro registro 236?
            html = urllib.urlopen(base_url, post_args)
            soup = BeautifulSoup.BeautifulSoup(html)
            state = re.search("([A-Z][A-Z]).*", city[1]).group(1)
            getPostos(soup, state)
        
def geocode(address, city, state):
    fuel_address = address + ',' + city + ',' + state
    url = 'http://maps.google.com/maps/api/geocode/json?sensor=false&region=br&address='+fuel_address
    results = urllib.urlopen(url)
    results = json.load(results)
    return results

def getPostos(soup, state):
    cod_municipio = soup.find("input", { 'name' : 'municipio' })['value']
    cod_combustivel = soup.find("input", { 'name' : 'Cod_Combustivel' })['value']
    cod_semana = soup.find("input", { 'name' : 'cod_semana' })['value']
    cidade = soup.find("input", { 'name' : 'desc_municipio' })['value']
    id = 0
    rows = soup.table.findAll("tr")
    header_rows = rows.pop(0)
    try:
        rows.pop(0)
        for row in rows:
            cell = row.findAll("td")
            data = {}
            data['id'] = cod_municipio + '-' + cod_combustivel + '-' + cod_semana + '-' + str(id)
            data['tipo'] = fuel_list[int(cod_combustivel)]
            data['city'] = cidade
            data['state'] = state
            data['razao_social'] = cell[0].text
            data['endereco'] = cell[1].text
            data['bairro'] = cell[2].a.text
            data['latlng'] = geocode(data['endereco'],data['city'],data['state'])
            if cod_combustivel == '462': #GLP
                print 'Getting GLP:' + str(cod_combustivel)
                data['bandeira'] = '-'
                data['distribuidora'] = cell[3].text
                data['preco_venda'] = cell[4].text
                data['preco_compra'] = cell[5].text
                data['modalidade_de_compra'] = cell[6].text
                data['fornecedor'] = ''
                data['data_coleta'] = cell[7].text
                scraperwiki.sqlite.save(["id"], data, table_name='gas_price')
            else:           
                print 'Getting Other:' + str(cod_combustivel)
                data['bandeira'] = cell[3].text
                data['distribuidora'] = '-'
                data['preco_venda'] = cell[4].text
                data['preco_compra'] = cell[5].text
                data['modalidade_de_compra'] = cell[6].text
                data['fornecedor'] = cell[7].text
                data['data_coleta'] = cell[8].text
                scraperwiki.sqlite.save(["id"], data, table_name='gas_price')
            id += 1
    except:
        scrape_error = str(sys.exc_info()[1])
        print scrape_error
        registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error)
        return 0
         

states_list = ['AC*ACRE', 'AL*ALAGOAS', 'AP*AMAP\xc3\x81', 'AM*AMAZONAS', 'BA*BAHIA', 'CE*CEAR\xc3\x81', 'DF*DISTRITO@FEDERAL', 'ES*ESP\xc3\x8dRITO@SANTO', 'GO*GOI\xc3\x81S', 'MA*MARANH\xc3\x83O', 'MT*MATO@GROSSO', 'MS*MATO@GROSSO@DO@SUL', 'MG*MINAS@GERAIS', 'PR*PARAN\xc3\x81', 'PB*PARA\xc3\x8dBA', 'PA*PAR\xc3\x81', 'PE*PERNAMBUCO', 'PI*PIAU\xc3\x8d', 'RJ*RIO@DE@JANEIRO', 'RN*RIO@GRANDE@DO@NORTE', 'RS*RIO@GRANDE@DO@SUL', 'RO*ROND\xc3\x94NIA', 'RR*RORAIMA', 'SC*SANTA@CATARINA', 'SE*SERGIPE', 'SP*S\xc3\x83O@PAULO', 'TO*TOCANTINS']

#states_list =['SC*SANTA@CATARINA']

try:
    cities_list = scraperwiki.sqlite.execute('select id, state from cities')
    print cities_list
except:
    processaCidades(states_list)
    cities_list = scraperwiki.sqlite.execute('select id, state from cities')

fuel_list = {487 : 'Gasolina', 643 : 'Etanol', 476 : 'GNV', 532 : 'Diesel', 462 : 'GLP'}

processaPostos(cities_list, fuel_list)