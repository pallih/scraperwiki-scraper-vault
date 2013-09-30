# Blank Python
import urllib
import BeautifulSoup
import scraperwiki
import re
import sys
import json
import string

#*******************************************************CIDADES***********************************************************************

#baixa o json com as cidades do outro scraper e cria uma nova tabela com esses dados transformados
def processaCidades():
    url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=anp-fuelscraper-br_2&query=select%20*%20from%20%27cities%27";
    cidades = urllib.urlopen(url)
    cidades = json.load(cidades)

    print "Pegando dados de cidades"
    print cidades
    for cidade in cidades:
        cod_municipio = cidade['id']
        data = {}
        data['id'] = int(cod_municipio.split('*')[0])
        data['nome'] = fromCodigoToNome(cod_municipio)
        data['cod_municipio'] = cod_municipio
        data['cod_estado'] = cidade['state']
        data['estado'] = fromCodigoToNome(cidade['state'])
        data['qntPostos'] = int(cidade['postos'])
        scraperwiki.sqlite.save(["id"], data, table_name='cities')
        print data['nome']
    print "Busca das cidades concluída"

#metodo auxiliar de processaCidades
def fromCodigoToNome(codigo):
    nome = codigo.split('*')[1].replace('@',' ')
    nome = string.capwords(nome)
    return nome

#*******************************************************AUXILIARES***********************************************************************

#não funciona, pois o google não permite tantas requisições
def geocode(address, city, state):
    fuel_address = address + ',' + city + ',' + state
    url = 'http://maps.google.com/maps/api/geocode/json?sensor=false&region=br&address='+fuel_address
    results = urllib.urlopen(url)
    results = json.load(results)
    lat = results['geometry']['location']['lat']
    lng = results['geometry']['location']['lng']
    return results

#metodo para registrar os scrapes que deram errado
def registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error):
        error = {}
        error['id'] = cod_municipio + '-' + cod_combustivel + '-' + cod_semana
        error['cod_municipio'] = cod_municipio
        error['cod_combustivel'] = cod_combustivel
        error['cod_semana'] = cod_semana
        error['msg'] = scrape_error
        scraperwiki.sqlite.save(["id"], error, table_name='failed_scrapes')

#monta a url para buscar os precos de combustivel ou os dados dos postos
def urlPreco(cod_semana, cod_combustivel, cod_municipio):
    post_arg = "cod_semana=" + str(cod_semana)
    post_arg += "&desc_semana=" + desc_semana #De+03%2F06%2F2012+a+09%2F06%2F2012
    post_arg += "&cod_combustivel=" + str(cod_combustivel)
    post_arg += "&desc_combustivel=+-+Gasolina+R%24%2Fl"
    post_arg += "&selMunicipio=" + cod_municipio
    post_arg += "&tipo=1"
    return post_arg

#*******************************************************POSTOS DE GASOLINA***********************************************************************

#pega as informacoes sobre os postos de cities_list
#considera só as informações de gasolina, pois a maioria dos postos tem gasolina
#os que não fornecem gasolina são processados posteriormente, quando for adicionar os precos dos outros combustiveis
def processaPostos(cities_list, cod_semana):
    fuel_list = {487 : 'Gasolina'}
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Posto.asp"
    for city in cities_list['data']:
        for tipo in fuel_list:
            print 'Pegando dados dos postos de gasolina de ' + city[2]
            post_args = urlPreco(cod_semana, tipo, city[1])
            html = urllib.urlopen(base_url, post_args)
            soup = BeautifulSoup.BeautifulSoup(html)
            getPostos(soup)
        
#adiciona os postos que estão no soup
def getPostos(soup):
    cod_municipio = soup.find("input", { 'name' : 'municipio' })['value']
    cod_combustivel = soup.find("input", { 'name' : 'Cod_Combustivel' })['value']
    cod_semana = soup.find("input", { 'name' : 'cod_semana' })['value']
    cidade = soup.find("input", { 'name' : 'desc_municipio' })['value']
    id = 0
    rows = soup.table.findAll("tr")
    header_rows = rows.pop(0)
    try:
        for row in rows:
            cell = row.findAll("td")
            adicionarPosto(id, cod_municipio, cod_combustivel, cell, cidade)
            id += 1
    except:
        scrape_error = str(sys.exc_info()[1])
        print scrape_error
        registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error)
        return 0

#adiciona no banco um novo posto de gasolina
def adicionarPosto(id, cod_municipio, cod_combustivel, cell, cidade):
    data = {}
    id_posto = cod_municipio + '-' + str(id)
    data['id'] = id_posto
    data['id_cidade'] = int(cod_municipio)
    data['razao_social'] = cell[0].text
    data['endereco'] = cell[1].text
    data['bairro'] = cell[2].a.text
    print 'Pegando dados do posto ' + str(id) + " da cidade " + cidade
    if cod_combustivel == '462': #GLP
        data['bandeira'] = '-'
        scraperwiki.sqlite.save(["id"], data, table_name='gas_station')
    else:           
        data['bandeira'] = cell[3].text
        scraperwiki.sqlite.save(["id"], data, table_name='gas_station')
    return id_posto

#*******************************************************PREÇOS DE COMBUSTÍVEIS***********************************************************************

#adiciona no banco os precos dos combustiveis de fuel_list, das cidades cities_list e na semana cod_semana
def processaPrecos(cities_list, fuel_list, cod_semana):
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Posto.asp"
    i = 1
    size = len(cities_list['data'])
    for city in cities_list['data']:
        print '**** Cidade {0} - {1} de {2} ****'.format(city[2], i, size)
        for tipo in fuel_list:
            print 'Pegando dados de ' + fuel_list[tipo] + ' dos postos de ' + city[2]
            post_args = urlPreco(cod_semana, tipo, city[1])
            html = urllib.urlopen(base_url, post_args)
            soup = BeautifulSoup.BeautifulSoup(html)
            getPrecos(soup, fuel_list)

#adiciona no banco os precos dos combustiveis de fuel_list retornados em soup
def getPrecos(soup, fuel_list):  
    cod_municipio = soup.find("input", { 'name' : 'municipio' })['value']
    cod_combustivel = soup.find("input", { 'name' : 'Cod_Combustivel' })['value']
    cod_semana = soup.find("input", { 'name' : 'cod_semana' })['value']
    cidade = soup.find("input", { 'name' : 'desc_municipio' })['value']
    id = 0
    rows = soup.table.findAll("tr")
    header_rows = rows.pop(0)

    try:
        if len(rows) == 0:
            print '****Entrou aqui pegou nada ****'
            return
        rows.pop(0)
        for row in rows:
            cell = row.findAll("td")
            razao_social = cell[0].text
            endereco = cell[1].text
            bairro = cell[2].a.text
            id_posto = getPostoId(razao_social, endereco, bairro, cod_municipio, cod_combustivel, cell, cidade)
            adicionarPreco(id_posto, cod_combustivel, cod_semana, fuel_list, cell)
    except:
        scrape_error = str(sys.exc_info()[1])
        print scrape_error
        registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error)
        return 0

#adiciona no banco um registro de preco de combustivel com os dados passados
def adicionarPreco(id_posto, cod_combustivel, cod_semana, fuel_list, cell):
    combustivel = fuel_list[int(cod_combustivel)]

    data = {}
    data['id'] = id_posto + '-' + cod_combustivel + '-' + cod_semana
    data['id_posto'] = id_posto
    data['combustivel'] = combustivel
    data['cod_combustivel'] = int(cod_combustivel)
    data['preco_venda'] = precoToFloat(cell[4].text)
    data['preco_compra'] = precoToFloat(cell[5].text)
    data['modalidade_de_compra'] = cell[6].text
    print combustivel + ' - Posto ' + id_posto

    if cod_combustivel == '462': #GLP
        data['distribuidora'] = cell[3].text
        data['fornecedor'] = ''
        data['data_coleta'] = cell[7].text
    else:           
        data['distribuidora'] = '-'
        data['fornecedor'] = cell[7].text
        data['data_coleta'] = cell[8].text
    scraperwiki.sqlite.save(["id"], data, table_name='gas_price')
    print "salvou " + str(data['id'])

#busca o id do posto com as informacoes passadas como parametro
#caso o posto com essas informacoes não exista, cria um novo posto
def getPostoId(razao_social, endereco, bairro, cod_municipio, cod_combustivel, cell, cidade):
    strings = formatStringToQuery([razao_social, endereco, bairro])
    query = 'select id from gas_station where razao_social="'+ strings[0] + '" and endereco="' + strings[1] + '" and bairro="' + strings[2] + '" and id_cidade=' + cod_municipio

    id_postos_list = scraperwiki.sqlite.execute(query)
    id_postos_list = id_postos_list['data']
    if(id_postos_list == []):
        id = getProximoIdGasStation(cod_municipio)
        id_posto = adicionarPosto(id, cod_municipio, cod_combustivel, cell, cidade)
        print "Criou novo posto com id " + id_posto
    else:
        id_posto = id_postos_list[0][0]
    return id_posto

#no caso de precisar criar um novo posto, essa funcao retorna a id desse posto, ou seja, o próximo id válido para um posto de determinado municipio
def getProximoIdGasStation(cod_municipio):
    query = 'select id from gas_station where id_cidade="{0}"'.format(cod_municipio)
    id_postos_list = scraperwiki.sqlite.execute(query)
    id_postos_list = id_postos_list['data']
    maxId = 0;
    for id in id_postos_list:
        id = int(id[0].split('-')[1])
        if id > maxId:
            maxId = id
    return maxId+1

def precoToFloat(preco):
    preco = preco.replace(',' , '.')
    try:
        preco = float(preco)
        return preco
    except:
        return 0

def formatStringToQuery(strings):
    retorno = []
    for str in strings:
        str = str.replace('"','""')
        retorno += [str]
    return retorno 

#*******************************************************MÉTODOS PRINCIPAIS***********************************************************************

#recria a tabela de cidades
def populaTabelaCidades():
    try:
        scraperwiki.sqlite.execute('drop table cities')
    except:
        i = 0 #nao faz nada
    processaCidades()

#retorna a lista de cidades
def listaCidades():
    try:
        cities_list = scraperwiki.sqlite.execute('select id, cod_municipio, nome from cities where estado <> "Santa Catarina" and estado <> "São Paulo" and estado <> "Minas Gerais" and estado <> "Bahia" and estado <> "Goiás" and estado <> "Paraná"')
        print cities_list 
    except:
        populaTabelaCidades()
        cities_list = scraperwiki.sqlite.execute('select id, cod_municipio, nome from cities')
    return cities_list

def listaCidadesFaltando():
    query = "select id from 'cities' where id not in (select distinct s.id_cidade from `gas_price` p, 'gas_station' s where p.id_posto = s.id)"
    cities_list = scraperwiki.sqlite.execute('select id, cod_municipio, nome from cities where  id in (2754, 4048, 2980)')
    #cities_list = cities_list[1000:]
    return cities_list

#recria a tabela dos postos de gasolina
def populaTabelaPostosGasolina():
    #try:
        #scraperwiki.sqlite.execute('drop table gas_station')
    #except:
       # i = 0 #nao faz nada
    cities_list = listaCidades()
    semana = cod_semana
    processaPostos(cities_list, semana)

#adiciona os precos de cod_semana 
def populaTabelaPrecoCombustivel(cod_semana):
    fuel_list = {487 : 'Gasolina', 643 : 'Etanol', 476 : 'GNV', 532 : 'Diesel', 462 : 'GLP'}
    cities_list = listaCidadesFaltando()
    processaPrecos(cities_list, fuel_list, cod_semana)

#codigo da semana
base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Index.asp"
html = urllib.urlopen(base_url)
soup = BeautifulSoup.BeautifulSoup(html)
cod_semana = soup.find("input", { 'name' : 'cod_Semana' })['value']
desc_semana = soup.find("input", { 'name' : 'desc_Semana' })['value']

#recria a tabela de cidades
populaTabelaCidades()

#popula a tabela de gas_station, ou seja, preenche todos os postos de gasolina
populaTabelaPostosGasolina()

#popula a tabela de gas_price, ou seja, busca os preços de gasolina de uma determinada semana
#scraperwiki.sqlite.execute('drop table gas_price')
populaTabelaPrecoCombustivel(cod_semana)

#print listaCidadesFaltando()# Blank Python
import urllib
import BeautifulSoup
import scraperwiki
import re
import sys
import json
import string

#*******************************************************CIDADES***********************************************************************

#baixa o json com as cidades do outro scraper e cria uma nova tabela com esses dados transformados
def processaCidades():
    url = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=anp-fuelscraper-br_2&query=select%20*%20from%20%27cities%27";
    cidades = urllib.urlopen(url)
    cidades = json.load(cidades)

    print "Pegando dados de cidades"
    print cidades
    for cidade in cidades:
        cod_municipio = cidade['id']
        data = {}
        data['id'] = int(cod_municipio.split('*')[0])
        data['nome'] = fromCodigoToNome(cod_municipio)
        data['cod_municipio'] = cod_municipio
        data['cod_estado'] = cidade['state']
        data['estado'] = fromCodigoToNome(cidade['state'])
        data['qntPostos'] = int(cidade['postos'])
        scraperwiki.sqlite.save(["id"], data, table_name='cities')
        print data['nome']
    print "Busca das cidades concluída"

#metodo auxiliar de processaCidades
def fromCodigoToNome(codigo):
    nome = codigo.split('*')[1].replace('@',' ')
    nome = string.capwords(nome)
    return nome

#*******************************************************AUXILIARES***********************************************************************

#não funciona, pois o google não permite tantas requisições
def geocode(address, city, state):
    fuel_address = address + ',' + city + ',' + state
    url = 'http://maps.google.com/maps/api/geocode/json?sensor=false&region=br&address='+fuel_address
    results = urllib.urlopen(url)
    results = json.load(results)
    lat = results['geometry']['location']['lat']
    lng = results['geometry']['location']['lng']
    return results

#metodo para registrar os scrapes que deram errado
def registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error):
        error = {}
        error['id'] = cod_municipio + '-' + cod_combustivel + '-' + cod_semana
        error['cod_municipio'] = cod_municipio
        error['cod_combustivel'] = cod_combustivel
        error['cod_semana'] = cod_semana
        error['msg'] = scrape_error
        scraperwiki.sqlite.save(["id"], error, table_name='failed_scrapes')

#monta a url para buscar os precos de combustivel ou os dados dos postos
def urlPreco(cod_semana, cod_combustivel, cod_municipio):
    post_arg = "cod_semana=" + str(cod_semana)
    post_arg += "&desc_semana=" + desc_semana #De+03%2F06%2F2012+a+09%2F06%2F2012
    post_arg += "&cod_combustivel=" + str(cod_combustivel)
    post_arg += "&desc_combustivel=+-+Gasolina+R%24%2Fl"
    post_arg += "&selMunicipio=" + cod_municipio
    post_arg += "&tipo=1"
    return post_arg

#*******************************************************POSTOS DE GASOLINA***********************************************************************

#pega as informacoes sobre os postos de cities_list
#considera só as informações de gasolina, pois a maioria dos postos tem gasolina
#os que não fornecem gasolina são processados posteriormente, quando for adicionar os precos dos outros combustiveis
def processaPostos(cities_list, cod_semana):
    fuel_list = {487 : 'Gasolina'}
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Posto.asp"
    for city in cities_list['data']:
        for tipo in fuel_list:
            print 'Pegando dados dos postos de gasolina de ' + city[2]
            post_args = urlPreco(cod_semana, tipo, city[1])
            html = urllib.urlopen(base_url, post_args)
            soup = BeautifulSoup.BeautifulSoup(html)
            getPostos(soup)
        
#adiciona os postos que estão no soup
def getPostos(soup):
    cod_municipio = soup.find("input", { 'name' : 'municipio' })['value']
    cod_combustivel = soup.find("input", { 'name' : 'Cod_Combustivel' })['value']
    cod_semana = soup.find("input", { 'name' : 'cod_semana' })['value']
    cidade = soup.find("input", { 'name' : 'desc_municipio' })['value']
    id = 0
    rows = soup.table.findAll("tr")
    header_rows = rows.pop(0)
    try:
        for row in rows:
            cell = row.findAll("td")
            adicionarPosto(id, cod_municipio, cod_combustivel, cell, cidade)
            id += 1
    except:
        scrape_error = str(sys.exc_info()[1])
        print scrape_error
        registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error)
        return 0

#adiciona no banco um novo posto de gasolina
def adicionarPosto(id, cod_municipio, cod_combustivel, cell, cidade):
    data = {}
    id_posto = cod_municipio + '-' + str(id)
    data['id'] = id_posto
    data['id_cidade'] = int(cod_municipio)
    data['razao_social'] = cell[0].text
    data['endereco'] = cell[1].text
    data['bairro'] = cell[2].a.text
    print 'Pegando dados do posto ' + str(id) + " da cidade " + cidade
    if cod_combustivel == '462': #GLP
        data['bandeira'] = '-'
        scraperwiki.sqlite.save(["id"], data, table_name='gas_station')
    else:           
        data['bandeira'] = cell[3].text
        scraperwiki.sqlite.save(["id"], data, table_name='gas_station')
    return id_posto

#*******************************************************PREÇOS DE COMBUSTÍVEIS***********************************************************************

#adiciona no banco os precos dos combustiveis de fuel_list, das cidades cities_list e na semana cod_semana
def processaPrecos(cities_list, fuel_list, cod_semana):
    base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Posto.asp"
    i = 1
    size = len(cities_list['data'])
    for city in cities_list['data']:
        print '**** Cidade {0} - {1} de {2} ****'.format(city[2], i, size)
        for tipo in fuel_list:
            print 'Pegando dados de ' + fuel_list[tipo] + ' dos postos de ' + city[2]
            post_args = urlPreco(cod_semana, tipo, city[1])
            html = urllib.urlopen(base_url, post_args)
            soup = BeautifulSoup.BeautifulSoup(html)
            getPrecos(soup, fuel_list)

#adiciona no banco os precos dos combustiveis de fuel_list retornados em soup
def getPrecos(soup, fuel_list):  
    cod_municipio = soup.find("input", { 'name' : 'municipio' })['value']
    cod_combustivel = soup.find("input", { 'name' : 'Cod_Combustivel' })['value']
    cod_semana = soup.find("input", { 'name' : 'cod_semana' })['value']
    cidade = soup.find("input", { 'name' : 'desc_municipio' })['value']
    id = 0
    rows = soup.table.findAll("tr")
    header_rows = rows.pop(0)

    try:
        if len(rows) == 0:
            print '****Entrou aqui pegou nada ****'
            return
        rows.pop(0)
        for row in rows:
            cell = row.findAll("td")
            razao_social = cell[0].text
            endereco = cell[1].text
            bairro = cell[2].a.text
            id_posto = getPostoId(razao_social, endereco, bairro, cod_municipio, cod_combustivel, cell, cidade)
            adicionarPreco(id_posto, cod_combustivel, cod_semana, fuel_list, cell)
    except:
        scrape_error = str(sys.exc_info()[1])
        print scrape_error
        registerFail(cod_semana, cod_combustivel, cod_municipio, scrape_error)
        return 0

#adiciona no banco um registro de preco de combustivel com os dados passados
def adicionarPreco(id_posto, cod_combustivel, cod_semana, fuel_list, cell):
    combustivel = fuel_list[int(cod_combustivel)]

    data = {}
    data['id'] = id_posto + '-' + cod_combustivel + '-' + cod_semana
    data['id_posto'] = id_posto
    data['combustivel'] = combustivel
    data['cod_combustivel'] = int(cod_combustivel)
    data['preco_venda'] = precoToFloat(cell[4].text)
    data['preco_compra'] = precoToFloat(cell[5].text)
    data['modalidade_de_compra'] = cell[6].text
    print combustivel + ' - Posto ' + id_posto

    if cod_combustivel == '462': #GLP
        data['distribuidora'] = cell[3].text
        data['fornecedor'] = ''
        data['data_coleta'] = cell[7].text
    else:           
        data['distribuidora'] = '-'
        data['fornecedor'] = cell[7].text
        data['data_coleta'] = cell[8].text
    scraperwiki.sqlite.save(["id"], data, table_name='gas_price')
    print "salvou " + str(data['id'])

#busca o id do posto com as informacoes passadas como parametro
#caso o posto com essas informacoes não exista, cria um novo posto
def getPostoId(razao_social, endereco, bairro, cod_municipio, cod_combustivel, cell, cidade):
    strings = formatStringToQuery([razao_social, endereco, bairro])
    query = 'select id from gas_station where razao_social="'+ strings[0] + '" and endereco="' + strings[1] + '" and bairro="' + strings[2] + '" and id_cidade=' + cod_municipio

    id_postos_list = scraperwiki.sqlite.execute(query)
    id_postos_list = id_postos_list['data']
    if(id_postos_list == []):
        id = getProximoIdGasStation(cod_municipio)
        id_posto = adicionarPosto(id, cod_municipio, cod_combustivel, cell, cidade)
        print "Criou novo posto com id " + id_posto
    else:
        id_posto = id_postos_list[0][0]
    return id_posto

#no caso de precisar criar um novo posto, essa funcao retorna a id desse posto, ou seja, o próximo id válido para um posto de determinado municipio
def getProximoIdGasStation(cod_municipio):
    query = 'select id from gas_station where id_cidade="{0}"'.format(cod_municipio)
    id_postos_list = scraperwiki.sqlite.execute(query)
    id_postos_list = id_postos_list['data']
    maxId = 0;
    for id in id_postos_list:
        id = int(id[0].split('-')[1])
        if id > maxId:
            maxId = id
    return maxId+1

def precoToFloat(preco):
    preco = preco.replace(',' , '.')
    try:
        preco = float(preco)
        return preco
    except:
        return 0

def formatStringToQuery(strings):
    retorno = []
    for str in strings:
        str = str.replace('"','""')
        retorno += [str]
    return retorno 

#*******************************************************MÉTODOS PRINCIPAIS***********************************************************************

#recria a tabela de cidades
def populaTabelaCidades():
    try:
        scraperwiki.sqlite.execute('drop table cities')
    except:
        i = 0 #nao faz nada
    processaCidades()

#retorna a lista de cidades
def listaCidades():
    try:
        cities_list = scraperwiki.sqlite.execute('select id, cod_municipio, nome from cities where estado <> "Santa Catarina" and estado <> "São Paulo" and estado <> "Minas Gerais" and estado <> "Bahia" and estado <> "Goiás" and estado <> "Paraná"')
        print cities_list 
    except:
        populaTabelaCidades()
        cities_list = scraperwiki.sqlite.execute('select id, cod_municipio, nome from cities')
    return cities_list

def listaCidadesFaltando():
    query = "select id from 'cities' where id not in (select distinct s.id_cidade from `gas_price` p, 'gas_station' s where p.id_posto = s.id)"
    cities_list = scraperwiki.sqlite.execute('select id, cod_municipio, nome from cities where  id in (2754, 4048, 2980)')
    #cities_list = cities_list[1000:]
    return cities_list

#recria a tabela dos postos de gasolina
def populaTabelaPostosGasolina():
    #try:
        #scraperwiki.sqlite.execute('drop table gas_station')
    #except:
       # i = 0 #nao faz nada
    cities_list = listaCidades()
    semana = cod_semana
    processaPostos(cities_list, semana)

#adiciona os precos de cod_semana 
def populaTabelaPrecoCombustivel(cod_semana):
    fuel_list = {487 : 'Gasolina', 643 : 'Etanol', 476 : 'GNV', 532 : 'Diesel', 462 : 'GLP'}
    cities_list = listaCidadesFaltando()
    processaPrecos(cities_list, fuel_list, cod_semana)

#codigo da semana
base_url = "http://www.anp.gov.br/preco/prc/Resumo_Semanal_Index.asp"
html = urllib.urlopen(base_url)
soup = BeautifulSoup.BeautifulSoup(html)
cod_semana = soup.find("input", { 'name' : 'cod_Semana' })['value']
desc_semana = soup.find("input", { 'name' : 'desc_Semana' })['value']

#recria a tabela de cidades
populaTabelaCidades()

#popula a tabela de gas_station, ou seja, preenche todos os postos de gasolina
populaTabelaPostosGasolina()

#popula a tabela de gas_price, ou seja, busca os preços de gasolina de uma determinada semana
#scraperwiki.sqlite.execute('drop table gas_price')
populaTabelaPrecoCombustivel(cod_semana)

#print listaCidadesFaltando()