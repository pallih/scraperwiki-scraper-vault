# -*- coding: utf-8 -*-     
import urllib
import BeautifulSoup
import scraperwiki
import re
import datetime

base_url = "http://www.portaltransparencia.gov.br/despesasdiarias/resultado?consulta=avancada&fase=PAG&codigoOS=42000&codigoOrgao=42101&codigoUG=420016&codigoED=14&codigoFavorecido="
arg_inicio = "&periodoInicio="
arg_fim = "&periodoFim="

def analisaDiarias(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(html, fromEncoding='utf-8')

    descricao = soup.find("td", text=re.compile("Observa.* do Documento:")).next.next.text
    datas = re.search("PERIODO DE ([0-9 ]*) A ([0-9 ]*) ", descricao)
    data = {}
    d_ini = datas.group(1)
    d_fim = datas.group(2)
    d_ini = d_ini.strip()
    d_fim = d_fim.strip()
    data['inicio'] = datetime.datetime.strptime(d_ini, "%d %m %Y")
    data['fim'] = datetime.datetime.strptime(d_fim, "%d %m %Y")
    return data

def getDiarias(url, data_inicio):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup.BeautifulSoup(html)
    diarias = soup.find("table", "tabela")
    diarias = diarias.findAll("tr")
    diarias.pop(0)
    id = 0
    for row in diarias:
        data = {}
        data["id"] = data_inicio + "-" + str(id)
        cell = row.findAll("td")            
        data['favorecido'] = cell[8].text
        data['valor'] = cell[9].text
        data['url'] = 'http://www.portaltransparencia.gov.br/despesasdiarias/' + cell[2].a['href']
        d = analisaDiarias(data['url'])
        data['inicio'] = d['inicio'].isoformat()
        data['fim'] = d['fim'].isoformat()
        scraperwiki.sqlite.save(["id"],data)
        print data
        id = id + 1


d_start = datetime.date(2011,01,01)
d_end = d_start
today = datetime.date.today()
while d_end < today:
    d_end = d_start + datetime.timedelta(29)
    data_inicio = d_start.strftime("%d%%2F%m%%2F%Y")
    data_fim = d_end.strftime("%d%%2F%m%%2F%Y")
    print data_inicio
    print data_fim
    getDiarias(base_url + arg_inicio + data_inicio + arg_fim + data_fim, data_inicio)
    d_start = d_end + datetime.timedelta(1)