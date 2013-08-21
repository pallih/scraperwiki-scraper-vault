# Cosmico Python Scraper Visa Caixa

import scraperwiki
import lxml.html


from lxml.html import parse
import re

url = "https://internetbanking.caixa.gov.br/SIIBC/siwinCtrl?swAction=7&navegacao=1"
html = scraperwiki.scrape(url)
print html

root = lxml.html.fromstring(html)
#ps = parse(url).getroot()

#print ps

#print root.cssselect('#cabecalho strong')[0]text_content()

#url = "http://thacker.com.br/users?page=0"

#data = {}


#ps = parse(url).getroot()

#print ps.cssselect('#menu h1')[o].text_content()
#print ps.cssselect('#view-id-user_page-page_1 a')[1].text_content()




