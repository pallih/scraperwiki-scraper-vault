###############################################################################
#                                  RUAGI                                      #
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import randint

# Global                                                                       

start_id = 43688
end_id = 52300
sleep_time = randint (1 ,10)

# Metadata                                                                     

scraperwiki.metadata.save('data_columns', ['sujeto_obligado_cargo', 'sujeto_obligado', 'dependencia', 'fecha_de_solicitud', 'solicitante_cargo', 'solicitante_id', 'solicitante', 'interes_invocado', 'representado', 'fecha_audiencia', 'lugar', 'participantes', 'estado', 'sintesis'])

# Scraper                                                                      

def scrape_dapp(soup):
    record = {}
    results = soup.findAll('span')
    print results
    if results:
        record['id'] = url_id
        record['sujeto_obligado_cargo'] = results[1].text
        record['sujeto_obligado'] = results[2].text
        record['dependencia'] = results[3].text
        record['fecha_de_solicitud'] = results[4].text
        record['solicitante_cargo'] = results[5].text
        record['solicitante_id'] = results[6].text
        record['solicitante'] = results[7].text
        record['interes_invocado'] = results[8].text
        record['representado'] = results[9].text
        record['fecha_audiencia'] = results[10].text
        record['lugar'] = results[11].text
        record['participantes'] = results[12].text
        record['estado'] = results[13].text
        record['sintesis'] = results[14].text
        scraperwiki.datastore.save(["id"], record)

# URLs                                                                        

for url_id in range (start_id ,end_id):
    url_base = "http://open.dapper.net/transform.php?dappName=RUAGIScraper3&transformer=HTML&extraArg_microFormat=1&v_url_id="
    dapp_url = url_base + str(url_id)
    print url_id
    html = scraperwiki.scrape(dapp_url)
    soup = BeautifulSoup(html)
    scrape_dapp(soup)
    sleep(sleep_time)

###############################################################################
#                                  RUAGI                                      #
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import randint

# Global                                                                       

start_id = 43688
end_id = 52300
sleep_time = randint (1 ,10)

# Metadata                                                                     

scraperwiki.metadata.save('data_columns', ['sujeto_obligado_cargo', 'sujeto_obligado', 'dependencia', 'fecha_de_solicitud', 'solicitante_cargo', 'solicitante_id', 'solicitante', 'interes_invocado', 'representado', 'fecha_audiencia', 'lugar', 'participantes', 'estado', 'sintesis'])

# Scraper                                                                      

def scrape_dapp(soup):
    record = {}
    results = soup.findAll('span')
    print results
    if results:
        record['id'] = url_id
        record['sujeto_obligado_cargo'] = results[1].text
        record['sujeto_obligado'] = results[2].text
        record['dependencia'] = results[3].text
        record['fecha_de_solicitud'] = results[4].text
        record['solicitante_cargo'] = results[5].text
        record['solicitante_id'] = results[6].text
        record['solicitante'] = results[7].text
        record['interes_invocado'] = results[8].text
        record['representado'] = results[9].text
        record['fecha_audiencia'] = results[10].text
        record['lugar'] = results[11].text
        record['participantes'] = results[12].text
        record['estado'] = results[13].text
        record['sintesis'] = results[14].text
        scraperwiki.datastore.save(["id"], record)

# URLs                                                                        

for url_id in range (start_id ,end_id):
    url_base = "http://open.dapper.net/transform.php?dappName=RUAGIScraper3&transformer=HTML&extraArg_microFormat=1&v_url_id="
    dapp_url = url_base + str(url_id)
    print url_id
    html = scraperwiki.scrape(dapp_url)
    soup = BeautifulSoup(html)
    scrape_dapp(soup)
    sleep(sleep_time)

