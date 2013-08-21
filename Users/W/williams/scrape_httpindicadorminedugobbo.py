import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://indicador.minedu.gob.bo/frmficha.php?id_mun=040101")

root = lxml.html.fromstring(html)

titleTable = root.cssselect("body table table")[0]

city = {}

for (index, row) in enumerate(titleTable.cssselect("tr")):
    col = row.cssselect("td")
    city = {
        'codigo' : col[0].text().strip(),
        'ciudad' : col[1].text().strip(),
        'sub_codigo' : col[2].text().strip()
    }
    print city
    
infoTables = root.cssselect('body table table table table')

povertyTable = infoTables[0]

firstRow = povertyTable.cssselect("tr")[0]
secondRow = povertyTable.cssselect("tr")[1]

tituloNoPobreza = firstRow.cssselect("td")[0].text_content()
tituloPobreza = firstRow.cssselect("td")[1].text_content()

porcentajeNoPobreza = secondRow.cssselect("td")[0].text_content()
porcentajePobreza = secondRow.cssselect("td")[1].text_content()

poverty_data = {
    tituloNoPobreza.strip() : porcentajeNoPobreza.strip(),
    tituloPobreza.strip() : porcentajePobreza.strip()
}

print poverty_data
