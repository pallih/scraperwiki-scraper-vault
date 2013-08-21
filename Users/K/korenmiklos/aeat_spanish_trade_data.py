import scraperwiki

# Blank Python
def year_url(year):
    if year>=2002:
        return "http://www.agenciatributaria.es/AEAT.internet/Inicio_es_ES/Aduanas_e_Impuestos_Especiales/Estadisticas_Comercio_Exterior/Informacion_Estadistica/Datos_estadisticos/Descarga_de_Datos_Estadisticos/Descarga_de_datos_mensuales_maxima_desagregacion_en_Euros__centimos_/%(year)d/%(year)d.shtml" % dict(year=year)
    else:
        return "http://www.agenciatributaria.es/AEAT.internet/Inicio_es_ES/Aduanas_e_Impuestos_Especiales/Estadisticas_Comercio_Exterior/Informacion_Estadistica/Datos_estadisticos/Descarga_de_Datos_Estadisticos/Descarga_de_datos_anuales_maxima_desagregacion_en_Euros__centimos_/%(year)d/%(year)d.shtml" % dict(year=year)

import lxml.html
import os.path

urls = []
for year in range(1993,2002):
    html = scraperwiki.scrape(year_url(year))
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.contenido a"):           
        follow = el.attrib['href']           
        urls.append(dict(file=os.path.basename(follow), link=follow))
for year in range(2002,2014):
    html = scraperwiki.scrape(year_url(year))
    root = lxml.html.fromstring(html)
    for el in root.cssselect("div.contenido a"):           
        month = lxml.html.fromstring(scraperwiki.scrape('http://www.agenciatributaria.es'+el.attrib['href']))
        for link in month.cssselect("div.contenido a"):
            follow = link.attrib['href']           
            urls.append(dict(file=os.path.basename(follow), link=follow))
print len(urls)
scraperwiki.sqlite.save(unique_keys=["file"], data=urls)
