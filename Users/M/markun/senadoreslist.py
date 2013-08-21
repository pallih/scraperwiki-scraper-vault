# Blank Python
import scraperwiki
import urllib
import BeautifulSoup
import re

senadores_list = 'http://www.senado.gov.br/senadores/'
base_comission = 'http://www.senado.gov.br/atividade/comissoes/consParl.asp?p_cod_senador='

def getSenadores():
    html = urllib.urlopen(senadores_list)
    soup = BeautifulSoup.BeautifulSoup(html)
    soup = soup.find('table', { 'id' : 'senadores' })
    rows = soup.tbody.findAll('tr')
    senadores_ids = []

    for row in rows:
        data = {}
        cell = row.findAll('td')
        data['id'] = re.search('senador([0-9]*)a\.asp', cell[0].a['href']).group(1)
        data['name'] = cell[0].text
        data['uf'] = re.search('([A-Z][A-Z])', cell[1].text).group(1)
        data['party'] = cell[2].text
        data['period_start'] = re.search('^(.*)-',cell[3].text).group(1)
        data['period_end'] = re.search('-(.*)$',cell[3].text).group(1)
        data['phone'] = cell[4].text
        data['fax'] = cell[5].text
        data['email'] = re.search('mailto:(.*)',cell[6].a['href']).group(1)
        try:
            data['url'] = cell[7].a['href']
        except:
            data['url'] = ''
        scraperwiki.datastore.save(["id"], data, table_name='senadores_list')
        senadores_ids.append(data['id'])
    return senadores_ids

def getComissionPages(senator_id):
    html = urllib.urlopen(base_comission + str(senator_id))
    soup = BeautifulSoup.BeautifulSoup(html)
    s = soup.find(text=re.compile("Total de registros:"))
    pages = re.search('[0-9]* de ([0-9]*)', str(s))
    return int(pages.group(1))

def getComissions(senator_id, pages):
    id = 0
    html = urllib.urlopen(base_comission + str(senator_id))
    soup = BeautifulSoup.BeautifulSoup(html)
    soup = soup.find('table', { 'cellpadding' : '2' })
    rows = soup.tbody.findAll('tr')
    comission = {}
    for row in rows:
        cell = row.findAll('td')
        
        try:
            end_date = cell[2].text
            actual = 1
        except:
            end_date = ''
            actual = 0
        try:
            comission_id = re.search('montaURL([0-9]*),', cell[0].a['onclick']).group(1)
        except:
            comission_id = ''

        comission['id'] = str(senator_id) + '_' + str(id)
        comission['senator_id'] = senator_id
        comission['short_name'] = re.search('(^[A-Z]*)', cell[0].text).group(1)
        comission['full_name'] = cell[0].text
        comission['comission_id'] = comission_id
        comission['start_date'] = cell[1].text
        comission['end_date'] = end_date
        comission['actual'] = actual
        comission['participation'] = cell[3].text
        scraperwiki.datastore.save(["id"], comission, table_name='comissions')
        id += 1

senadores_ids = getSenadores()
last_id = 0
for id in senadores_ids:
    pages = getComissionPages(id)
    getComissions(id, pages)
