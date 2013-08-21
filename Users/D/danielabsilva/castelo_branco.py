import scraperwiki
import urllib
from lxml.html import parse

url_base = "http://www.carloscastellobranco.com.br/"

def parsetudo():
    meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    for ano in range(1963, 1994):
        for mes in meses:
            try:
                url = url_base + "sec_coluna.php?mes=" + mes + "&ano=" + str(ano)
                html = parse(url).getroot()
                pegatudo(html)
            except:
                print url

def pegatudo(html):
    textos = html.cssselect(".lista_texto")
    for texto in textos:
        data = {}
        data["dia"] = texto.cssselect(".lista_texto")[0].text
        data["titulo"] = texto.cssselect(".lista_texto a")[0].text
        data["link"] = url_base + texto.cssselect(".lista_texto a")[0].get("href").split("'")[1]
        scraperwiki.sqlite.save(["link"],data,table_name="links")

def pegatexto(data):
    try:
        html = parse(data["link"]).getroot()
        data["texto"] = html.cssselect(".coluna_texto")[0].text_content()
        scraperwiki.sqlite.save(["link"],data,table_name="links")
    except:
        print data["link"]


listaurl = scraperwiki.sqlite.select("* from links")
for data in listaurl:
    pegatexto(data)

#urls que estao dando erro
#http://www.carloscastellobranco.com.br/sec_coluna_view.php?id=4745
#http://www.carloscastellobranco.com.br/sec_coluna.php?mes=03&ano=1963
