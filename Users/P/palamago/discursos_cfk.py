import scraperwiki
import urllib
import urllib2
from bs4 import BeautifulSoup
from collections import Counter
import unicodedata
from datetime import datetime, tzinfo

base_url = 'http://www.presidencia.gob.ar'
list_url = '/discursos?start=%s'
discursos = []
discursosId = []
exceptions = ['de','que','la','en','el','y','a','los','por','un',
                'del','se','con','lo','es','las','una','porque',
                'me','esta','para','como','pero','al','o','cuando','hay','fue','mas','ano',
                'tambien','hemos','ciento','este','todo','ha','nos','ser','era','millones','anos',
                'esto','muy','son','le']
replacement = [ 
                ('.',' '),
                (',',' '),
                ('(',' '),
                (')',' '),
                ('"',' '),
                ('!',' '),    
                ('?',' '),    
                (';',' '),
                (':',' '),
                ('-',' '),
                ('%',' '),
                ('/',' '),
                ('\n',' ')
                ]

paginado = 0

def init():
    scrap_list_discursos(paginado)
    scrap_discursos(discursos)

def fetch_url(url): 
    return BeautifulSoup(urllib2.urlopen(url).read()) 
 
def get_date(datestr):
    datesplitted = datestr.split(',')[1]
    datesplitted = datesplitted.strip().split(' ')
    meses = {
        'enero':1,
        'febrero':2,
        'marzo':3,
        'abril':4,
        'mayo':5,
        'junio':6,
        'julio':7,
        'agosto':8,
        'septiembre':9,
        'octubre':10,
        'noviembre':11,
        'diciembre':12                                                                
    }

    return datetime(int(datesplitted[4]), meses[datesplitted[2].lower()], int(datesplitted[0]),12,0,0)

def scrap_list_discursos(paginado):
    url = base_url + list_url % paginado
    #print "\t- Fetching %s" % url
    soup = fetch_url(url)
    nextLink = soup.find("a", title="Fin")

    blocks = soup.find_all("div", "item-parablog")

    if nextLink:
        nextLink = True
    else:
        nextLink = False

    nextPage=True

    for block in blocks:

        link = block.find("a","contentpagetitle").get('href')
        discurso_id = link.split("/")
        discurso_id = discurso_id[2]
        discurso_id = discurso_id.split("-")[0]
        
        exists = scraperwiki.sqlite.execute("select id from discurso where id = " + discurso_id)
        if len(exists['data'])>0:
            print "El id " + discurso_id + " ya EXISTE, se termina."
            nextPage=False
            break
            
        else:
            print "El id " + discurso_id + " es NUEVO, se agrega."
            nextPage=True
            d = {
                'date': get_date(block.find("p","fechag").get_text()),
                'name': block.find("a","contentpagetitle").get_text(),
                'link': base_url + link,
                'id': int(discurso_id)
                }
        
            discursos.append(d)
            discursosId.append(discurso_id)

    if nextPage & nextLink:
        paginado+=11
        scrap_list_discursos(paginado)



def scrap_discursos(ds):
    for d in ds:
        scrap_discurso(d)

def scrap_discurso(discurso):
    print "\t- Fetching %s" % discurso["link"]
    soup = fetch_url(discurso["link"])

    textoOriginal = soup.find("td", valign="top").get_text()

    texto = textoOriginal.lower()

    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore')

    for k, v in replacement:
        texto = texto.replace(k, v)

    wordsArray = texto.split(' ') 
    
    c = Counter(wordsArray)  

    del c[""]
    
    d = {
        'text': textoOriginal,
        'counter': c,
        'total': len(wordsArray)
        }

    discurso.update(d)

    scraperwiki.sqlite.save(unique_keys=["id"], data=discurso, table_name="discurso") 

#run
init()


import scraperwiki
import urllib
import urllib2
from bs4 import BeautifulSoup
from collections import Counter
import unicodedata
from datetime import datetime, tzinfo

base_url = 'http://www.presidencia.gob.ar'
list_url = '/discursos?start=%s'
discursos = []
discursosId = []
exceptions = ['de','que','la','en','el','y','a','los','por','un',
                'del','se','con','lo','es','las','una','porque',
                'me','esta','para','como','pero','al','o','cuando','hay','fue','mas','ano',
                'tambien','hemos','ciento','este','todo','ha','nos','ser','era','millones','anos',
                'esto','muy','son','le']
replacement = [ 
                ('.',' '),
                (',',' '),
                ('(',' '),
                (')',' '),
                ('"',' '),
                ('!',' '),    
                ('?',' '),    
                (';',' '),
                (':',' '),
                ('-',' '),
                ('%',' '),
                ('/',' '),
                ('\n',' ')
                ]

paginado = 0

def init():
    scrap_list_discursos(paginado)
    scrap_discursos(discursos)

def fetch_url(url): 
    return BeautifulSoup(urllib2.urlopen(url).read()) 
 
def get_date(datestr):
    datesplitted = datestr.split(',')[1]
    datesplitted = datesplitted.strip().split(' ')
    meses = {
        'enero':1,
        'febrero':2,
        'marzo':3,
        'abril':4,
        'mayo':5,
        'junio':6,
        'julio':7,
        'agosto':8,
        'septiembre':9,
        'octubre':10,
        'noviembre':11,
        'diciembre':12                                                                
    }

    return datetime(int(datesplitted[4]), meses[datesplitted[2].lower()], int(datesplitted[0]),12,0,0)

def scrap_list_discursos(paginado):
    url = base_url + list_url % paginado
    #print "\t- Fetching %s" % url
    soup = fetch_url(url)
    nextLink = soup.find("a", title="Fin")

    blocks = soup.find_all("div", "item-parablog")

    if nextLink:
        nextLink = True
    else:
        nextLink = False

    nextPage=True

    for block in blocks:

        link = block.find("a","contentpagetitle").get('href')
        discurso_id = link.split("/")
        discurso_id = discurso_id[2]
        discurso_id = discurso_id.split("-")[0]
        
        exists = scraperwiki.sqlite.execute("select id from discurso where id = " + discurso_id)
        if len(exists['data'])>0:
            print "El id " + discurso_id + " ya EXISTE, se termina."
            nextPage=False
            break
            
        else:
            print "El id " + discurso_id + " es NUEVO, se agrega."
            nextPage=True
            d = {
                'date': get_date(block.find("p","fechag").get_text()),
                'name': block.find("a","contentpagetitle").get_text(),
                'link': base_url + link,
                'id': int(discurso_id)
                }
        
            discursos.append(d)
            discursosId.append(discurso_id)

    if nextPage & nextLink:
        paginado+=11
        scrap_list_discursos(paginado)



def scrap_discursos(ds):
    for d in ds:
        scrap_discurso(d)

def scrap_discurso(discurso):
    print "\t- Fetching %s" % discurso["link"]
    soup = fetch_url(discurso["link"])

    textoOriginal = soup.find("td", valign="top").get_text()

    texto = textoOriginal.lower()

    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore')

    for k, v in replacement:
        texto = texto.replace(k, v)

    wordsArray = texto.split(' ') 
    
    c = Counter(wordsArray)  

    del c[""]
    
    d = {
        'text': textoOriginal,
        'counter': c,
        'total': len(wordsArray)
        }

    discurso.update(d)

    scraperwiki.sqlite.save(unique_keys=["id"], data=discurso, table_name="discurso") 

#run
init()


