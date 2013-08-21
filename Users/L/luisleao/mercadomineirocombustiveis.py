# -*- coding: utf-8 -*-  

import scraperwiki
import json
import urllib

cidades = {} #com regiao
combustiveis = {}
postos = {}


###############################################################################
# Funcoes
###############################################################################


def unicode2utf8(value):
    u = unicode(value, "ISO-8859-1")
    return u.encode("UTF-8")

def carregaCombustivel():
    url = 'http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=3'
    html = scraperwiki.scrape(url)
    lista = html.split("|")
    for sItem in lista:
        item = sItem.split("^")
        combustivel = {"codigo": item[0], "nome": unicode2utf8(item[1])}
        combustiveis[item[0]] = combustivel
        #print combustivel
    #print html


def carregaCidade():
    url = 'http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=4'
    html = scraperwiki.scrape(url)
    lista = html.split("|")
    for sItem in lista:
        item = sItem.split("^")
        codigo_cidade = item[0]
        cidade = {"codigo": item[0], "nome": unicode2utf8(item[1]), "regioes": []}
        cidades[codigo_cidade] = cidade
        #print "{%s: %s}" % (cidade['codigo'], cidade['nome'])
        #carregar Regioes da cidade
        carregaRegiao(cidade)

def carregaRegiao(cidade):
    url = 'http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=6;%s' % cidade['codigo']
    html = scraperwiki.scrape(url)
    lista = html.split("|")
    for sItem in lista:
        item = sItem.split("^")
        codigo_regiao = item[0]
        nome_regiao = item[1]
        regiao = {"codigo": codigo_regiao, "nome": unicode2utf8(nome_regiao), "postos": []}
        cidade['regioes'].append(regiao)

def carregaDados(combustivel, cidade, regiao):
    url = 'http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=8;%s;%s;;%s;;' % (combustivel['codigo'], cidade['codigo'], regiao['codigo'])
    html = scraperwiki.scrape(url)
    if len(html) == 0:
        return
    lista = html.split("|")
    for sItem in lista:
        #print sItem
        item = sItem.split("^")
        razao_social = item[0]

        if not postos.has_key(razao_social):
            #carregar GEO e inserir dados
            posto = {
                "razao_social": unicode2utf8(item[0]), 
                "endereco": unicode2utf8(item[1]), 
                "telefone": unicode2utf8(item[2]), 
                "bairro": unicode2utf8(item[3]), 
                "cidade": cidade['nome'],
                "regiao": regiao['nome'],
                "bandeira": unicode2utf8(item[4]), 
                "marca": "http://mercadomineiro.com.br/combustivel/logo_posto/%s" % unicode2utf8(item[5]), 
                "data": unicode2utf8(item[8]),
                "combustiveis": {}
            }
            #CARREGAR GEO
            carregaGeo(posto)

            postos[razao_social] = posto
        else:
            posto = postos[razao_social]
        
        posto['combustiveis'][combustivel['nome']] = {'avista': item[6], 'aprazo': item[7], 'data': item[8]}
        

def carregaGeo(posto):
    url = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % urllib.quote_plus("%s, %s" % (posto['endereco'], posto['cidade']))

    html = urllib.urlopen(url)
    geo = json.load(html)

    if not geo:
        return
    
    if geo['status'] == "OK":
        if len(geo['results']) > 0:
            location = geo['results'][0]['geometry']['location']
            #print "%s: %s" % (posto['razao_social'], location)
            posto['latitude'] = location['lat']
            posto['longitude'] = location['lng']
        else:
            return
            #print "%s: SEM RETORNO" % posto['razao_social']
    else:
        return
        #print "%s: ERRO GEO" % posto['razao_social']






###############################################################################
# 
###############################################################################



print "carregando dados base..."
carregaCombustivel()
carregaCidade()

print "carregando dados dos combustiveis..."
for codigo_combustivel in combustiveis:
    combustivel = combustiveis[codigo_combustivel]
    #print combustivel
    for codigo_cidade in cidades:
        cidade = cidades[codigo_cidade]
        for regiao in cidade['regioes']:
            #regiao = regioes[codigo_regiao]
            carregaDados(combustivel, cidade, regiao)

print "salvando registro no banco de dados..."
for posto in postos:
    #print postos[posto]
    scraperwiki.datastore.save(['razao_social', 'endereco', 'bairro', 'cidade'], postos[posto]) # save the records one by one      




# BUSCAR COMBUSTIVEL
# http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=3
# 5^Alcool|6^Diesel|3^Gasolina|4^Gasolina Aditivada

# BUSCAR CIDADE
# http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=4

# BUSCAR BANDEIRA
# http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=7

# BUSCAR BAIRRO
# http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=5;{cidade}

# BUSCAR REGIAO
# http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=6;{cidade}
# 10^Barreiro|12^Centro|9^Leste|8^Nordeste|1^Noroeste|6^Norte|11^Oeste|7^Pampulha|13^Sul|5^Venda Nova

# BUSCAR POSTOS
# http://m.mercadomineiro.com.br/iphone/lib/broker.php?cmd=8;{tipo};{cidade};{bairro};{regiao};{bandeira};



