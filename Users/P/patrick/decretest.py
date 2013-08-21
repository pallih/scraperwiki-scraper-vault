import scraperwiki
import lxml.html

#Def ScrapeTeam(url):
#    return 

LeagueUrl = "http://www.acb.com/"
TeamUrl = "plantilla.php?cod_equipo="
TeamCod = "BAR"
RowTitles = []
RowData = []

localfile = "file:///Users/patrick/Downloads/Iniciativas.html"
url0 = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Iniciativas_piref73_2148295_73_1335437_1335437.next_page=/wc/"
url = url0 + "enviarCgiBuscadorIniciativas"

allurl = url0 + '/servidorCGI&CMD=VERLST&BASE=IWIC&FMT=INITXLUS.fmt&DOCS=1-521&DOCORDER=FIFO&OPDEF=Y&QUERY=%28I%29.ACIN1.+%26+%28"REAL-DECRETO-LEY"%29.SINI.'

# Grab the web page and scrape using lxml.html
html = scraperwiki.scrape(localfile)
root = lxml.html.fromstring(html)

# Blank Python
for el in root.cssselect("div.resultados_encontrados p"):
    contenido = el.cssselect("p.titulo_iniciativa a").text_content
    link = el.cssselect("p.titulo_iniciativa a").attrib['href']
    print contenido
    print link
