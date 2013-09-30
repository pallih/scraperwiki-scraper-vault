import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.sistema.puglia.it/portal/pls/portal/SISPUGLIA.RPT_ELENCO_BANDI_ASS.show?p_arg_names=_total_rows&p_arg_values=118&p_arg_names=_max_rows&p_arg_values=5&p_arg_names=_paginate&p_arg_values=NO&p_arg_names=_comp_name&p_arg_values=RPT_ELENCO_BANDI_ASS&p_arg_names=artema&p_arg_values=46&p_arg_names=chiamante&p_arg_values=2")
root = lxml.html.fromstring(html)
print html
for el in root.cssselect("table.lista_doc h3"):           
      print el.text

i=1
for el in root.cssselect("div.paginazione a"):           
         print i
         html =el.attrib['href']
         print html
         html2=scraperwiki.scrape(html)
         root = lxml.html.fromstring(html2)
         for el2 in root.cssselect("table.lista_doc h3"):
            print el2.text
         i=i+1



import scraperwiki
import lxml.html
html = scraperwiki.scrape("http://www.sistema.puglia.it/portal/pls/portal/SISPUGLIA.RPT_ELENCO_BANDI_ASS.show?p_arg_names=_total_rows&p_arg_values=118&p_arg_names=_max_rows&p_arg_values=5&p_arg_names=_paginate&p_arg_values=NO&p_arg_names=_comp_name&p_arg_values=RPT_ELENCO_BANDI_ASS&p_arg_names=artema&p_arg_values=46&p_arg_names=chiamante&p_arg_values=2")
root = lxml.html.fromstring(html)
print html
for el in root.cssselect("table.lista_doc h3"):           
      print el.text

i=1
for el in root.cssselect("div.paginazione a"):           
         print i
         html =el.attrib['href']
         print html
         html2=scraperwiki.scrape(html)
         root = lxml.html.fromstring(html2)
         for el2 in root.cssselect("table.lista_doc h3"):
            print el2.text
         i=i+1



