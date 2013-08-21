import scraperwiki
import mechanize
import lxml.html

partidas = """
1006302110
1006302120
"""

fecha_inicio = "20/07/2013"
fecha_fin = "15/08/2013" # Ojo que sea válida.
regimen = "E"

# Acá abajo empieza programa. 
# No tocar.

partidas = partidas.split()

root_url= "http://servicios.aduanas.gub.uy/LuciaPub90/"

br = mechanize.Browser()


for partida in partidas:

    dua_urls = []

    response = br.open(root_url + "hcn1publico.aspx")
    
    br.select_form(name="MAINFORM")
    
    br["_VFCHINI"] = fecha_inicio
    br["_VFCHFNL"] = fecha_fin
    br["_TIPO_REGI"] = [regimen]

    br["_PARTIDA"] = partida

    response = br.submit()

    root = lxml.html.fromstring(response.read())
    page_count = root.cssselect("#span__TOTPAG")[0].text

    for pagenum in range(int(page_count)-1):
        # Levanta links de DUA en la página
        links = root.cssselect("[id^=span_NUME_CORRE] a")
        dua_urls += [linky.get("href") for linky in links]

        # Pasa de página
        br.select_form(name="MAINFORM")
        br.find_control("_EventName").readonly = False
        br["_EventName"] = "ESIGUIENTE.CLICK."
        response = br.submit()
        root = lxml.html.fromstring(response.read())

    for dua_url in dua_urls:
        dua_url = root_url + dua_url
        response = br.open(dua_url)
        # root = lxml.html.fromstring(response.read())
        br.select_form(name="MAINFORM")
        data = {
            "partida": partida,
            "link": dua_url,
            "total_valor_aduanas_usd": br["TVAD_INCR"],
            "total_peso_neto": br["TPESO_NETO"],
            "fecha_de_numeracion": br["FECH_INGSI"],
            "exportador": br["DNOMBRE"]
        }
        scraperwiki.sqlite.save(unique_keys=["link"], data=data)


