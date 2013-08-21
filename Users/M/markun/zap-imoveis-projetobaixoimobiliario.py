import scraperwiki
from lxml.html import parse
import urllib
from unidecode import unidecode

# Blank Python
url_base = "http://www.zap.com.br/imoveis/brasil/?q="
enderecos = ['Alameda Barao de Limeira', 'Rua General Rondon ', 'Rua Guaianases ', 'Alameda Glete', 'Rua Conselheiro Nebias ', 'Alameda Nothmann ', 'Alameda Eduardo Prado', 'Rua Capistrano de Abreu', 'Rua Sousa Lima', 'Rua Barra Funda', 'Rua Albuquerque Lins ', 'Rua Brigadeiro Galvao ', 'Praca Olavo Bilac ', 'Rua Barra Funda', 'Alameda Ribeiro da Silva ', 'Rua General Julio Marcondes Salgado ', 'Avenida Sao João', 'Rua Helvetia ']

enderecos = ['Rua Vitorino Carmilo', 'Alameda Eduardo Prado', 'Rua Barra Funda', 'Rua Conselheiro Brotero', 'Rua Capistrano de Abreu', 'Rua Conselheiro Nebias', 'Rua Barao de Limeira', 'Alameda Glete', 'Julio Marcondes Salgado', 'Alameda Ribeiro da Silva']

enderecos = ['Julio Marcondes Salgado']

def scrapeia(url):
    soup = parse(url).getroot()
    resultados = soup.cssselect(".item.itemOf")
    
    for r in resultados:
        data = {}
        data['url'] = r.cssselect('.valorOferta')[0].get('href')
        data['bairro'] = r.cssselect('h3 a')[0].text_content()
        data['endereco'] = r.cssselect('h3 a')[3].text_content()
        caracteristicas = r.cssselect('.labelCar')
        for c in caracteristicas:
            data[unidecode(c.text)] = c.tail
        data['preco'] = r.cssselect('.valorOferta')[0].text_content()
        scraperwiki.sqlite.save(['url'], data)

for endereco in enderecos:
    url = url_base + urllib.quote_plus(unidecode(endereco).lower() + " sao paulo sp")
    try:
        scrapeia(url)
    except IOError:
        print url + ' url com problemas'
