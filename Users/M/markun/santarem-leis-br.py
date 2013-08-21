import urllib
import BeautifulSoup
import re
import scraperwiki

def getLeis(args):
    url = 'http://www.camaradesantarem.pa.gov.br/santarem/arquivodeleis.php?consulta=0&pagina=1&inicio='

    arquivo = urllib.urlopen(url + str(args))
    soup = BeautifulSoup.BeautifulSoup(arquivo, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
    print soup

    leis = soup.findAll("div", { "id" : "box-leis" })
    leis.pop() #remove ultimo indice

    for l in leis:
        data = {}
        data['titulo'] = l.find('h3').string.strip()
        try:
            l_info = re.search('Lei n.* ([0-9]*.[0-9]*.[0-9]*), de ([0-9]{1,2} de .* de [0-9]{4})', data['titulo'])
            data['numero'] = l_info.group(1)
            data['data'] = l_info.group(2)
        except:
            data['numero'] = '-'
            data['data'] = '-'
        data['link'] = 'http://www.camaradesantarem.pa.gov.br/santarem/' + l.find('a')['href']
        data['ementa'] = l.find('div', { 'id' : 'dispoe-leis' }).string.strip()
        scraperwiki.sqlite.save(['titulo'], data)


def rockndroll():
    args = -6
    while args > -7:
        args += 6       
        try:
            getLeis(args)
        except:
            print 'Ultimas leis: ' + str(args)
            break

rockndroll()