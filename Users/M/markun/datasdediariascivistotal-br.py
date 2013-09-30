# Blank Python
import urllib
import BeautifulSoup
import scraperwiki
import re
import datetime

base_url = "http://www.portaltransparencia.gov.br/despesasdiarias/resultado?consulta=avancada&fase=PAG&codigoED=14&codigoFavorecido="

arg_os = "&codigoOS="
data_os = "24000" #Orgao Superior - MCT
arg_orgao = "&codigoOrgao="
data_orgao = "24101" #Entidade vinculada - MINC
arg_ug = "&codigoUG="
data_ug = "TOD" #Unidade Gestora - Todas

arg_what = arg_os + data_os + arg_orgao + data_orgao + arg_ug + data_ug;

arg_pagina = "&pagina="
data_pagina = 1

arg_inicio = "&periodoInicio="
arg_fim = "&periodoFim="


def getPaginas(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    last_page = soup.find("span", "paginaXdeN").text
    last_page = re.search("[0-9]* de ([0-9]+)", last_page).group(1)
    return int(last_page)

def analisaDiarias(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    descricao = soup.find("td", text=re.compile("Observa.* do Documento:")).next.next.text
    try:
        datas = re.search("PERIODO DE ([0-9 ]*) A ([0-9 ]*) ", descricao)
        data = {}
        d_ini = datas.group(1)
        d_fim = datas.group(2)
        d_ini = d_ini.strip()
        d_fim = d_fim.strip()
        data['inicio'] = datetime.datetime.strptime(d_ini, "%d %m %Y")
        data['fim'] = datetime.datetime.strptime(d_fim, "%d %m %Y")
    except:
        data['inicio'] = datetime.datetime(1,1,1) #null data
        data['fim'] = datetime.datetime(1,1,1) #null data
    data['descricao'] = descricao
    return data

def getDiarias(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    diarias = soup.find("table", "tabela")
    diarias = diarias.findAll("tr")
    diarias.pop(0)
    for row in diarias:
        cell = row.findAll("td")            
        hit = scraperwiki.sqlite.select("id from swdata where id=? limit 1", [cell[2].text])
        if hit == None:
            data = {}
            data["id"] = cell[2].text
            data['data_pgto'] = cell[0].text
            data['fase'] = cell[1].text
            data['documento'] = cell[2].text
            data['url'] = 'http://www.portaltransparencia.gov.br/despesasdiarias/' + cell[2].a['href']
            data['tipo'] = cell[3].text
            data['orgao_superior'] = cell[4].text
            data['orgao_entidade'] = cell[5].text
            data['unidade_gestora'] = cell[6].text
            data['elemento_despesa'] = cell[7].text
            data['favorecido'] = cell[8].text
            data['valor'] = cell[9].text
            d = analisaDiarias(data['url'])
            data['inicio'] = d['inicio'].isoformat()
            data['fim'] = d['fim'].isoformat()
            data['descricao'] = d['descricao']
            scraperwiki.sqlite.save(["id"],data)
            print data


d_start = datetime.date(2011,01,01)
d_end = d_start
today = datetime.date.today()

while d_end < today:
    d_end = d_start + datetime.timedelta(29)
    data_inicio = d_start.strftime("%d%%2F%m%%2F%Y")
    data_fim = d_end.strftime("%d%%2F%m%%2F%Y")
    print data_inicio
    print data_fim
    last_page = getPaginas(base_url + arg_what + arg_inicio + data_inicio + arg_fim + data_fim + arg_pagina + str(data_pagina))
    for pagina in range(1,last_page+1):
        print 'getting page ' + str(pagina)
        getDiarias(base_url + arg_what + arg_inicio + data_inicio + arg_fim + data_fim + arg_pagina + str(pagina))
    d_start = d_end + datetime.timedelta(1)
# Blank Python
import urllib
import BeautifulSoup
import scraperwiki
import re
import datetime

base_url = "http://www.portaltransparencia.gov.br/despesasdiarias/resultado?consulta=avancada&fase=PAG&codigoED=14&codigoFavorecido="

arg_os = "&codigoOS="
data_os = "24000" #Orgao Superior - MCT
arg_orgao = "&codigoOrgao="
data_orgao = "24101" #Entidade vinculada - MINC
arg_ug = "&codigoUG="
data_ug = "TOD" #Unidade Gestora - Todas

arg_what = arg_os + data_os + arg_orgao + data_orgao + arg_ug + data_ug;

arg_pagina = "&pagina="
data_pagina = 1

arg_inicio = "&periodoInicio="
arg_fim = "&periodoFim="


def getPaginas(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    last_page = soup.find("span", "paginaXdeN").text
    last_page = re.search("[0-9]* de ([0-9]+)", last_page).group(1)
    return int(last_page)

def analisaDiarias(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    descricao = soup.find("td", text=re.compile("Observa.* do Documento:")).next.next.text
    try:
        datas = re.search("PERIODO DE ([0-9 ]*) A ([0-9 ]*) ", descricao)
        data = {}
        d_ini = datas.group(1)
        d_fim = datas.group(2)
        d_ini = d_ini.strip()
        d_fim = d_fim.strip()
        data['inicio'] = datetime.datetime.strptime(d_ini, "%d %m %Y")
        data['fim'] = datetime.datetime.strptime(d_fim, "%d %m %Y")
    except:
        data['inicio'] = datetime.datetime(1,1,1) #null data
        data['fim'] = datetime.datetime(1,1,1) #null data
    data['descricao'] = descricao
    return data

def getDiarias(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    diarias = soup.find("table", "tabela")
    diarias = diarias.findAll("tr")
    diarias.pop(0)
    for row in diarias:
        cell = row.findAll("td")            
        hit = scraperwiki.sqlite.select("id from swdata where id=? limit 1", [cell[2].text])
        if hit == None:
            data = {}
            data["id"] = cell[2].text
            data['data_pgto'] = cell[0].text
            data['fase'] = cell[1].text
            data['documento'] = cell[2].text
            data['url'] = 'http://www.portaltransparencia.gov.br/despesasdiarias/' + cell[2].a['href']
            data['tipo'] = cell[3].text
            data['orgao_superior'] = cell[4].text
            data['orgao_entidade'] = cell[5].text
            data['unidade_gestora'] = cell[6].text
            data['elemento_despesa'] = cell[7].text
            data['favorecido'] = cell[8].text
            data['valor'] = cell[9].text
            d = analisaDiarias(data['url'])
            data['inicio'] = d['inicio'].isoformat()
            data['fim'] = d['fim'].isoformat()
            data['descricao'] = d['descricao']
            scraperwiki.sqlite.save(["id"],data)
            print data


d_start = datetime.date(2011,01,01)
d_end = d_start
today = datetime.date.today()

while d_end < today:
    d_end = d_start + datetime.timedelta(29)
    data_inicio = d_start.strftime("%d%%2F%m%%2F%Y")
    data_fim = d_end.strftime("%d%%2F%m%%2F%Y")
    print data_inicio
    print data_fim
    last_page = getPaginas(base_url + arg_what + arg_inicio + data_inicio + arg_fim + data_fim + arg_pagina + str(data_pagina))
    for pagina in range(1,last_page+1):
        print 'getting page ' + str(pagina)
        getDiarias(base_url + arg_what + arg_inicio + data_inicio + arg_fim + data_fim + arg_pagina + str(pagina))
    d_start = d_end + datetime.timedelta(1)
