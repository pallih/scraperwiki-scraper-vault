import scraperwiki
from lxml import html


url = "http://www.portaltransparencia.gov.br/servidores/Servidor-DetalhaRemuneracao.asp?Op=4&IdServidor=1840818&CodOS=40107&DescOS=MINISTERIO%20DA%20CULTURA&CodOrgao=40107&DescOrgao=MINISTERIO%20DA%20CULTURA&CodAtividade=0053&DescAtividade=ASSESSOR&CodFuncao=DAS&CodNivel=1024&Ano=2012&Mes=8"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for row in doc.cssselect(".name_class "):
link_in_header = row.cssselect("h4 a").pop()
event_title = link_in_header.text

print event_title

import scraperwiki
from lxml import html


url = "http://www.portaltransparencia.gov.br/servidores/Servidor-DetalhaRemuneracao.asp?Op=4&IdServidor=1840818&CodOS=40107&DescOS=MINISTERIO%20DA%20CULTURA&CodOrgao=40107&DescOrgao=MINISTERIO%20DA%20CULTURA&CodAtividade=0053&DescAtividade=ASSESSOR&CodFuncao=DAS&CodNivel=1024&Ano=2012&Mes=8"
doc_text = scraperwiki.scrape(url)
doc = html.fromstring(doc_text)

for row in doc.cssselect(".name_class "):
link_in_header = row.cssselect("h4 a").pop()
event_title = link_in_header.text

print event_title

