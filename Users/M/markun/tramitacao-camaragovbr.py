# -*- coding: utf-8 -*-                                                                                                                                               
###############################################################################                                                                                       
# Basic scraper                                                                                                                                                       
###############################################################################                                                                                       

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

materia = '268907'
# retrieve a page                                                                                                                                                     

starting_url = 'http://www.camara.gov.br/internet/sileg/Prop_Detalhe.asp?id=' + materia
html = unicode(scraperwiki.scrape(starting_url), 'utf-8', 'ignore')

#soup = BeautifulSoup(html, fromEncoding='utf-8', convertEntities='html')
soup = BeautifulSoup(html, fromEncoding='utf-8')

tramitacao = soup.find(text="Andamento").findNext("tbody")
tramite = tramitacao.findAll("tr")

id_data = 0
for row in tramite:
    data = {}
    data['date'] = row.td.string.strip()
    data['where'] = row.td.findNext("td").strong
    data['where'].extract()
    data['where'] = data['where'].text.encode("utf-8")
    if row.td.findNext("td").a:
        data['link'] = row.td.findNext("td").a['href']
    else:
        data['link'] = ''
    data['action'] = row.td.findNext("td").text
    data['id'] = id_data
    id_data = id_data + 1
    scraperwiki.datastore.save(['id'], data) # save the records one by one                          
