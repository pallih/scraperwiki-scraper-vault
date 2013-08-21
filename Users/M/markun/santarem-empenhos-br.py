import urllib
import BeautifulSoup
import re
import scraperwiki

def getOrgaos(url):
    url = "http://transparencia.santarem.pa.gov.br/servlet/pt_consultardespesa?0.1925523494611303,Abril%2F2011,2011.00000,4.00000,0.00000,Despesa+Geral,"
    arquivo = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(arquivo)
    orgaos = soup.find('input', { 'name' : 'Grid1ContainerDataV' })['value']
    orgaos = eval(orgaos)

    form_data = soup.find('form', { 'id' : 'MAINFORM' })['action']
    data = re.search(',([0-9]{4},[0-9]{1,2},[0-9]{1,2}),', form_data).group(1)
    return orgaos, data


def montaUrl(id_orgao, data):
    base_url = 'http://transparencia.santarem.pa.gov.br/servlet/pt_detalheempenhadaii?'
    data_extenso = ''
    tipo_despesa = ''
    id_orgao = id_orgao
    nome_orgao = ''
    valor_total = '243790.39'
    argX = ''
    data = data
    url = base_url + data_extenso + ',' + tipo_despesa + ',' + id_orgao + ',' + nome_orgao + ',' + valor_total + ',' + argX + ',' + data
    return url
    

def getEmpenhos(url):
    arquivo = urllib.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(arquivo)
    empenhos = soup.find('input', { 'name' : 'Grid1ContainerDataV' })['value']
    empenhos = eval(empenhos)
    return empenhos

def getEmpenho(empenho_id):
    base_url = 'http://transparencia.santarem.pa.gov.br/servlet/pt_mostrarempenho?'
    arquivo = urllib.urlopen(base_url + empenho_id)
    soup = BeautifulSoup.BeautifulSoup(arquivo)

    tabela = soup.find("table", { 'id' : 'TABLE2' })
    empenho = tabela
    data = {}
    #CREDOR
    data['id'] = empenho_id
    data['credor_nome'] = empenho.find('span', { 'id' : 'TEXTBLOCK9' }).string
    data['credor_cnpj'] = empenho.find('span', { 'id' : 'TEXTBLOCK12' }).string
    data['endereco'] = empenho.find('span', { 'id' : 'TEXTBLOCK11' }).string
    data['cidade'] = empenho.find('span', { 'id' : 'TB_CIDADE' }).string

    #PROCESSO LICITATORIO
    data['modalidade'] = empenho.find('span', { 'id' : 'TB_MODALIDADE' }).string
    data['processo'] = empenho.find('span', { 'id' : 'TB_PROCESSO2' }).string
    data['contrato'] = empenho.find('span', { 'id' : 'TB_CONTRATO2' }).string 

    #EMPENHO

    data['unidade_gestora'] = empenho.find('span', { 'id' : 'TEXTBLOCK1' }).string
    data['unidade_orcamentaria'] = empenho.find('span', { 'id' : 'TEXTBLOCK2' }).string
    data['funcao'] = empenho.find('span', { 'id' : 'TEXTBLOCK4' }).string
    data['subfuncao'] = empenho.find('span', { 'id' : 'TEXTBLOCK5' }).string
    data['programa'] = empenho.find('span', { 'id' : 'TEXTBLOCK13' }).string
    data['acao'] = empenho.find('span', { 'id' : 'TEXTBLOCK3' }).string
    data['elemento_despesa'] = empenho.find('span', { 'id' : 'TEXTBLOCK7' }).string
    data['sub_elemento'] = empenho.find('span', { 'id' : 'TB_SUBELEMENTO' }).string
    data['fonte_recurso'] = empenho.find('span', { 'id' : 'TEXTBLOCK6' }).string
    data['tipo_empenho'] = empenho.find('span', { 'id' : 'TB_TIPOEMPENHO' }).string
    data['data_empenho'] = empenho.find('span', { 'id' : 'TEXTBLOCK10' }).string
    data['valor_empenho'] = empenho.find('span', { 'id' : 'span_vV_VALOR' }).string
    data['historico'] = empenho.find('span', { 'id' : 'span_vV_HIST' }).string

    #to-do movimentos

    #stripa!
    for i in data:
        if data[i]:
            data[i] = data[i].strip()
    return data

def saveEmpenho(empenho):
    scraperwiki.sqlite.save(['id'], empenho)

def rockndroll():
    print 'Baixando orgaos...'
    orgaos, data = getOrgaos('nill')
    orgaos_urls = []
    print 'Montando urls...'
    for orgao in orgaos:
        orgaos_urls.append(montaUrl(orgao[0], data))
    for url in orgaos_urls:
        print 'Baixando empenhos...'
        empenhos = getEmpenhos(url)
        for empenho_id in empenhos:
            if not scraperwiki.sqlite.select("* from swdata where id=?",[empenho_id[0]]):
                print 'Baixando empenho ' + empenho_id[0]
                empenho = getEmpenho(empenho_id[0])
                saveEmpenho(empenho)
            else:
                print 'Empenho ' + empenho_id[0] + ' ja estava armazenado...'

rockndroll()