import scraperwiki
import urllib
from BeautifulSoup import BeautifulStoneSoup
from lxml.html import parse
url_todos = "http://www.excelencias.org.br/@busca.php"

def pega_url_parlamentar():
    html = parse(url_todos).getroot()
    ids = html.cssselect(".listapar")
    for id in ids:
        pega_dados_parlamentar(id.get("href"))

def pega_dados_parlamentar(parlamentar):
    url_parlamentar = parse("http://www.excelencias.org.br/" + parlamentar).getroot()
    url_xml = "http://www.excelencias.org.br/" + str(url_parlamentar.cssselect(".imdir a")[0].get("href"))
    try:
        xml = urllib.urlopen(url_xml)
        soup = BeautifulStoneSoup(xml)
        data = {}
        data["id"] = soup.principal.id.text
        data["apelido"] = soup.principal.apelido.text
        data["nome_de_batismo"] = soup.principal.nomebatismo.text
        data["uf"] = soup.principal.uf.text
        data["orgao"] = soup.principal.orgao.text
        data["partido"] = soup.principal.partidoeleito.text
        data["email"] = soup.principal.email.text
        data["id"] = url_xml.split("=")[1]
        scraperwiki.sqlite.save(["id"], data, table_name="parlamentares")
    except:
        data = {}
        data["erros"] = str(url_xml)
        scraperwiki.sqlite.save(["erros"], data, table_name="urls com erros")

pega_url_parlamentar()import scraperwiki
import urllib
from BeautifulSoup import BeautifulStoneSoup
from lxml.html import parse
url_todos = "http://www.excelencias.org.br/@busca.php"

def pega_url_parlamentar():
    html = parse(url_todos).getroot()
    ids = html.cssselect(".listapar")
    for id in ids:
        pega_dados_parlamentar(id.get("href"))

def pega_dados_parlamentar(parlamentar):
    url_parlamentar = parse("http://www.excelencias.org.br/" + parlamentar).getroot()
    url_xml = "http://www.excelencias.org.br/" + str(url_parlamentar.cssselect(".imdir a")[0].get("href"))
    try:
        xml = urllib.urlopen(url_xml)
        soup = BeautifulStoneSoup(xml)
        data = {}
        data["id"] = soup.principal.id.text
        data["apelido"] = soup.principal.apelido.text
        data["nome_de_batismo"] = soup.principal.nomebatismo.text
        data["uf"] = soup.principal.uf.text
        data["orgao"] = soup.principal.orgao.text
        data["partido"] = soup.principal.partidoeleito.text
        data["email"] = soup.principal.email.text
        data["id"] = url_xml.split("=")[1]
        scraperwiki.sqlite.save(["id"], data, table_name="parlamentares")
    except:
        data = {}
        data["erros"] = str(url_xml)
        scraperwiki.sqlite.save(["erros"], data, table_name="urls com erros")

pega_url_parlamentar()