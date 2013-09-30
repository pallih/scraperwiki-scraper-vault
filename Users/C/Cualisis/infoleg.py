###############################################################################
#                                  INFOLEG                                      #
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import randint

# Global                                                                       

start_id = 171000
end_id = 171500
sleep_time = randint (1 ,2)

# Metadata                                                                     

scraperwiki.metadata.save('data_columns', ['norma', 'dependencia', 'tema', 'titulo', 'fecha_publicacion', 'boletin_oficial', 'pagina', 'resumen', 'modifica_a', 'modificado_por', 'lugar'])

# Scraper                                                                      

def scrape_dapp(soup):
    record = {}
    results = soup.findAll('span')
    print results
    if results:
        record['id'] = url_id
        record['norma'] = results[1].text
        record['dependencia'] = results[2].text
        record['tema'] = results[3].text
        record['titulo'] = results[4].text
        record['fecha_publicacion'] = results[5].text
        record['boletin_oficial'] = results[6].text
        record['pagina'] = results[7].text
        record['resumen'] = results[8].text
        record['modifica_a'] = results[9].text
        record['modificado_por'] = results[10].text
        scraperwiki.datastore.save(["id"], record)

# URLs                                                                        

for url_id in range (start_id ,end_id):
    url_base = "http://open.dapper.net/transform.php?dappName=INFOLEG&transformer=HTML&extraArg_microFormat=1&v_url_id="
    dapp_url = url_base + str(url_id)
    print url_id
    html = scraperwiki.scrape(dapp_url)
    soup = BeautifulSoup(html)
    scrape_dapp(soup)
    sleep(sleep_time)###############################################################################
#                                  INFOLEG                                      #
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import randint

# Global                                                                       

start_id = 171000
end_id = 171500
sleep_time = randint (1 ,2)

# Metadata                                                                     

scraperwiki.metadata.save('data_columns', ['norma', 'dependencia', 'tema', 'titulo', 'fecha_publicacion', 'boletin_oficial', 'pagina', 'resumen', 'modifica_a', 'modificado_por', 'lugar'])

# Scraper                                                                      

def scrape_dapp(soup):
    record = {}
    results = soup.findAll('span')
    print results
    if results:
        record['id'] = url_id
        record['norma'] = results[1].text
        record['dependencia'] = results[2].text
        record['tema'] = results[3].text
        record['titulo'] = results[4].text
        record['fecha_publicacion'] = results[5].text
        record['boletin_oficial'] = results[6].text
        record['pagina'] = results[7].text
        record['resumen'] = results[8].text
        record['modifica_a'] = results[9].text
        record['modificado_por'] = results[10].text
        scraperwiki.datastore.save(["id"], record)

# URLs                                                                        

for url_id in range (start_id ,end_id):
    url_base = "http://open.dapper.net/transform.php?dappName=INFOLEG&transformer=HTML&extraArg_microFormat=1&v_url_id="
    dapp_url = url_base + str(url_id)
    print url_id
    html = scraperwiki.scrape(dapp_url)
    soup = BeautifulSoup(html)
    scrape_dapp(soup)
    sleep(sleep_time)