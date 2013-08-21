import scraperwiki
import urlparse
import lxml.html
import requests
import re
###############################

#import requests
#import lxml.html
#import re

#html = """<div id="info">
  #<table >
    #<tr >
      #<td  class="Tabla_01"><p>Nombre y Apellido</p></td>
     # <td  class="Tabla_03"><strong>David HIRTZ</strong></td>
    #</tr>
    #<tr >
      #<td class="textoTabla_01"><p>Cargo</p></td>
     # <td class="textoTabla_04"><strong>Intendente</strong></td>
    #</tr>
    #<!-- <tr >
      #<td class="Tabla_01"><p>Part&iacute;do pol&iacute;tico</p></td>
     # <td class="Tabla_04"><strong>Unión para el Desarrollo Social</strong></td>
    #</tr>
    #<tr >
      #<td class="Tabla_01"><p>Cobertura territorial de la agrupaci&oacute;n</p></td>
     # <td class="Tabla_04"><strong>Nacional</strong></td>
    #</tr> -->
    #<tr >
    #  <td class="Tabla_01"><p>Reelecto</p></td>
   #   <td <strong>No</strong></td>
  #  </tr>
 # </table>
#</div>"""

#cleaned_html = re.sub(r'(<!--)|(-->)', '', html)

#dom = lxml.html.fromstring(cleaned_html)

#print len(dom.cssselect('tr')), 'rows'

#for tr in dom.cssselect('tr'):
    #print '-', tr.text_content()

###############################
###############################

def scrape_divs(url):
    html = scraperwiki.scrape(url)
    cleaned_html = re.sub(r'(<!--)|(-->)', '', html)
    dom = lxml.html.fromstring(cleaned_html)
    
    rows = dom.cssselect("div#info") 

    for row in rows:
       
        print row
        record = {}
        
        municipio = ""
        
        h1s = row.cssselect("h1")
        if h1s:
            municipio=h1s[0].text


        record['Municipio'] = municipio
       
        tds = row.cssselect("td")
        if tds:
            nomyApell=tds[1].text_content()
        record['NomYApell'] = nomyApell    
        if tds[5]:
            parPol=tds[5].text_content()
        record['ParPol'] = parPol       
        print record, '------------'
        scraperwiki.sqlite.save(["Municipio"], record)
        

scrape_divs('http://www.mininterior.gov.ar/municipios/masinfo.php?municipio=BUE001&idName=municipios&idNameSubMenu=&idNameSubMenuDer=&idNameSubMenuDerNivel2=&idNameSubMenuDerPrincipal=')




