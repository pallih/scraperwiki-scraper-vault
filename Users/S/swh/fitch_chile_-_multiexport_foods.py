import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.fitchratings.cl/FichaEmpresaResearchRelacionado1.asp?Id_Resumen=427&Glosa=EMPRESAS&Pagina=Sectores/Ratings.asp&Id_Grupo=Id_Grupo&Id_TipoOpcion=2&Letra=M&Buscar=EMPRESAS"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}

for story in root.cssselect('tr.texto3'):
  stories['date'] = parser.parse(story.cssselect('td')[0].text)
  stories['story'] = story.cssselect('td')[1].text_content()
  stories['link'] = 'http://www.fitchratings.cl/Upload/'+ story.cssselect('td')[1].cssselect('a')[0].attrib['href']
  scraperwiki.sqlite.save(['link'],stories)
  print story.cssselect('td')[0].text_content()
 

import scraperwiki

import lxml.html

import urllib
from dateutil import parser

url = "http://www.fitchratings.cl/FichaEmpresaResearchRelacionado1.asp?Id_Resumen=427&Glosa=EMPRESAS&Pagina=Sectores/Ratings.asp&Id_Grupo=Id_Grupo&Id_TipoOpcion=2&Letra=M&Buscar=EMPRESAS"
root = lxml.html.fromstring(scraperwiki.scrape(url))
stories = {}

for story in root.cssselect('tr.texto3'):
  stories['date'] = parser.parse(story.cssselect('td')[0].text)
  stories['story'] = story.cssselect('td')[1].text_content()
  stories['link'] = 'http://www.fitchratings.cl/Upload/'+ story.cssselect('td')[1].cssselect('a')[0].attrib['href']
  scraperwiki.sqlite.save(['link'],stories)
  print story.cssselect('td')[0].text_content()
 

