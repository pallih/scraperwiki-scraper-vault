import urllib
import BeautifulSoup
import re
import scraperwiki

def saveProgress(url, tipo, ano):
    data = {
        'url' : url,
        'tipo': tipo,
        'ano' : ano
        }
    scraperwiki.sqlite.save(['url'], data, table_name='progress')

def getRepasses():
    url = 'http://www.sefa.pa.gov.br/site/tesouro/dites/repasse/repasse.htm'
    arquivo = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(arquivo)
    links = soup.findAll('a')
    tipos = ['IPI', 'ICMS', 'IPVA', 'FUNDEB']

    for l in links:
        link = 'http://www.sefa.pa.gov.br' + l['href']

        tipo = None

        for t in tipos:  
            if re.search(t, l['href']):
                tipo = t

        ano = re.search('([0-9]{4})', link)
        if ano:
            ano = ano.group(1)
        else:
            ano = ''
                
        if tipo and ano:
            if not scraperwiki.sqlite.select('url from progress where url=?', link):
                getRepasse(link, ano, tipo)
    
def getRepasse(url, ano, tipo):
    arquivo = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(arquivo)
    tabela = soup.findAll('table')
    
    #2005 usava outro formato de html
    if len(tabela) == 1:
        linhas = tabela[0].findAll('tr')
    else:
        linhas = tabela[1].findAll('tr')
    meses = ['meses']
    linhas.pop(0) #remove tbheaders
    
    #TABELAS de 2006 usam outro formato
    if url == 'http://www.sefa.pa.gov.br/site/tesouro/dites/repasse/ICMS/2006/icms_2006_1sem.htm':
        for a in range(0,9):
            linhas.pop(0)
        for a in range(0,3):
            linhas.pop()

    elif url == 'http://www.sefa.pa.gov.br/site/tesouro/dites/repasse/ICMS/2006/icms_2006_2sem.htm':
        for a in range(0,9):
            linhas.pop(0)
        for a in range(0,4):
            linhas.pop()
    

    #ICMS do 2008 tem um <div> outros tem <strong> no <td>
    try:
        for m in linhas[0].findAll('td'):
            print m
            mes = m.string.strip()
            mes = mes.strip('&nbsp;')
            meses.append(mes)
    except:
        for m in linhas[0].findAll('td'):
            mes = m.string.strip()
            mes = mes.strip('&nbsp;')
            meses.append(mes)

    linhas.pop(0) #remove tbheaders
    linhas.pop() #remove totais


    for linha in linhas:
        data = {}
        for mes in ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']:
            data[mes] = ''
        cols = linha.findAll('td')
        data['MUNICIPIO'] = cols[0].string
        
        #<span> no meio do nome do municipio
        if ano == '2007' and not data['MUNICIPIO']:
            data['MUNICIPIO'] = 'CONCEICAO ARAGUAIA'
        elif ano == '2006' and not data['MUNICIPIO']:
            data['MUNICIPIO'] = 'CONCEICAO ARAGUAIA'
        
        data[meses[1]] = cols[1].string
        data[meses[2]] = cols[2].string
        data[meses[3]] = cols[3].string
        data[meses[4]] = cols[4].string
        data[meses[5]] = cols[5].string
        data[meses[6]] = cols[6].string
        if meses[1] == 'JANEIRO':
            semestre = '_1'
        elif meses[1] == 'JULHO':
            semestre = '_2'         
        data['TOTAL' + semestre] = cols[7].string
        data['QUOTA' + semestre] = cols[8].string
        data['ANO'] = ano
        data['ID'] = data['ANO'] + '_' + data['MUNICIPIO'] + semestre
        scraperwiki.sqlite.save(['ID'], data, table_name=tipo)
    saveProgress(url, ano, tipo)

           
getRepasses()import urllib
import BeautifulSoup
import re
import scraperwiki

def saveProgress(url, tipo, ano):
    data = {
        'url' : url,
        'tipo': tipo,
        'ano' : ano
        }
    scraperwiki.sqlite.save(['url'], data, table_name='progress')

def getRepasses():
    url = 'http://www.sefa.pa.gov.br/site/tesouro/dites/repasse/repasse.htm'
    arquivo = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(arquivo)
    links = soup.findAll('a')
    tipos = ['IPI', 'ICMS', 'IPVA', 'FUNDEB']

    for l in links:
        link = 'http://www.sefa.pa.gov.br' + l['href']

        tipo = None

        for t in tipos:  
            if re.search(t, l['href']):
                tipo = t

        ano = re.search('([0-9]{4})', link)
        if ano:
            ano = ano.group(1)
        else:
            ano = ''
                
        if tipo and ano:
            if not scraperwiki.sqlite.select('url from progress where url=?', link):
                getRepasse(link, ano, tipo)
    
def getRepasse(url, ano, tipo):
    arquivo = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(arquivo)
    tabela = soup.findAll('table')
    
    #2005 usava outro formato de html
    if len(tabela) == 1:
        linhas = tabela[0].findAll('tr')
    else:
        linhas = tabela[1].findAll('tr')
    meses = ['meses']
    linhas.pop(0) #remove tbheaders
    
    #TABELAS de 2006 usam outro formato
    if url == 'http://www.sefa.pa.gov.br/site/tesouro/dites/repasse/ICMS/2006/icms_2006_1sem.htm':
        for a in range(0,9):
            linhas.pop(0)
        for a in range(0,3):
            linhas.pop()

    elif url == 'http://www.sefa.pa.gov.br/site/tesouro/dites/repasse/ICMS/2006/icms_2006_2sem.htm':
        for a in range(0,9):
            linhas.pop(0)
        for a in range(0,4):
            linhas.pop()
    

    #ICMS do 2008 tem um <div> outros tem <strong> no <td>
    try:
        for m in linhas[0].findAll('td'):
            print m
            mes = m.string.strip()
            mes = mes.strip('&nbsp;')
            meses.append(mes)
    except:
        for m in linhas[0].findAll('td'):
            mes = m.string.strip()
            mes = mes.strip('&nbsp;')
            meses.append(mes)

    linhas.pop(0) #remove tbheaders
    linhas.pop() #remove totais


    for linha in linhas:
        data = {}
        for mes in ['JANEIRO', 'FEVEREIRO', 'MARCO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']:
            data[mes] = ''
        cols = linha.findAll('td')
        data['MUNICIPIO'] = cols[0].string
        
        #<span> no meio do nome do municipio
        if ano == '2007' and not data['MUNICIPIO']:
            data['MUNICIPIO'] = 'CONCEICAO ARAGUAIA'
        elif ano == '2006' and not data['MUNICIPIO']:
            data['MUNICIPIO'] = 'CONCEICAO ARAGUAIA'
        
        data[meses[1]] = cols[1].string
        data[meses[2]] = cols[2].string
        data[meses[3]] = cols[3].string
        data[meses[4]] = cols[4].string
        data[meses[5]] = cols[5].string
        data[meses[6]] = cols[6].string
        if meses[1] == 'JANEIRO':
            semestre = '_1'
        elif meses[1] == 'JULHO':
            semestre = '_2'         
        data['TOTAL' + semestre] = cols[7].string
        data['QUOTA' + semestre] = cols[8].string
        data['ANO'] = ano
        data['ID'] = data['ANO'] + '_' + data['MUNICIPIO'] + semestre
        scraperwiki.sqlite.save(['ID'], data, table_name=tipo)
    saveProgress(url, ano, tipo)

           
getRepasses()