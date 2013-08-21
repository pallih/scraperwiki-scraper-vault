import scraperwiki
from lxml.html import parse

url_base= "http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?"
l_args = "Legislatura=43&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=T&forma=lista&nome=&ordem=partido&origem=None"

def scrape(url):
    soup = parse(url).getroot()
    print soup

url = url_base + l_args
results = scrape(url)