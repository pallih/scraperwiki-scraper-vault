import urllib
import urllib2
import scraperwiki
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime, tzinfo
import string
from urlparse import parse_qs
import unicodedata
import sys

baseUrl = "http://www.cemla.com/busqueda/buscador_action.php?d-dia=01&d-mes=01&h-dia=31&h-mes=12"

def init():
    parseAvailableYears()
    parseByYear(baseUrl)
    #parseByLetter(baseUrl)
    #parseByPages(baseUrl)
    #parseByPage("http://www.cemla.com/busqueda/buscador_action.php?d-dia=01&d-mes=01&h-dia=31&h-mes=12&h-anio=1882&d-anio=1882&Apellido=AN&pageNum_Recordset1=99")
    #parseByPage("http://www.cemla.com/busqueda/buscador_action.php?Apellido=BA&Nombre=&d-dia=01&d-mes=01&d-anio=1882&h-dia=31&h-mes=12&h-anio=1882&Apellido=Basag")

def fetch_url(url): 
    return BeautifulSoup(urllib2.urlopen(url).read().replace("º"," ")) 

#Parse and save available years
def parseAvailableYears():
    soup = fetch_url("http://www.cemla.com/busqueda.php")
    anios = soup.find("select", id="d-anio")
    anios = anios.find_all("option")
    for anio in anios:
        try:        
            y = int(anio.get_text())
            scraperwiki.sqlite.save(unique_keys=['anio'], data={'anio':y}, table_name="anio")
        except ValueError:
            print "Not an integer %s" % anio.get_text()

#parse by year 1882 1883 ...
def parseByYear(url):
    data = {}
    anios =  scraperwiki.sqlite.execute("select anio from anio")
    for anio in anios['data']:
        data['year'] = anio[0]
        parseByLetter(url + '&h-anio='+ str( anio[0] ) + '&d-anio='+ str( anio[0] ) , data ) 

letters = map(chr, range(65, 91))
letters = map(chr, range(65, 68))


def parseByLetter(url, data):

    for f in letters:
        for s in letters:
            data['first'] = f
            data['second'] = s
            parseByPages(url + '&Apellido='+ f + s , data )


#Parse by pages 0 1 2 ...
#pageNum_Recordset1=
def parseByPages(url, data):
    page = 0

    data['page'] = page

    while (parseByPage(url + '&pageNum_Recordset1='+ str( page ), data)):
        page += 1
        data['page'] = page


#Parse page
def parseByPage(url,data):

    #print data

    #it True, process
    if saveCurrentDataAndVerify(data):

        soup = fetch_url(url)
        regs = soup.find_all("tr","txt")
    
        #No results
        if soup.find("td","mensaje"):
            return False
    
        cl = parse_qs(url)
        cl = cl['Apellido'][0]
    
        for r in regs:

            cols = r.find_all("td")
            if (len(cols) == 10):
                #No results
                if cols[0].get_text().strip() == ',':
                    return False

                try:
                    date = cols[8].get_text().split(' - ')[0].strip()
                    datesplitted = date.split('/')
        
                    data = {
                        'nombre':   cols[0].get_text().split(', ')[1].strip(),
                        'apellido': cols[0].find('strong').get_text().strip(),
                        'edad':     int(cols[1].get_text().strip()),
                        'estado':   cols[2].get_text().strip(),
                        'profesion':cols[3].get_text().strip(),
                        'religion': cols[4].get_text().strip(),
                        'nacionalidad': cols[5].get_text().strip(),
                        'barco':    cols[6].get_text().strip(),
                        'procedencia': cols[7].get_text().strip(),
                        'anio':     int(datesplitted[2]),
                        'mes':      int(datesplitted[1]),
                        'dia':      int(datesplitted[0]),
                        'fecha':    datetime(int(datesplitted[2]), int(datesplitted[1]), int(datesplitted[0]),12,0,0),
                        'puerto':   cols[8].get_text().split(' - ')[1].strip(),
                        'nacido':   cols[9].get_text().strip()
                    }
        
                    #Prevent duplicates
                    if data['apellido'].upper().startswith( cl.upper() ):
                        h = hashlib.new('ripemd160')
                        h.update(normalize(data['nombre'] + data['apellido'] + str(data['edad'])))
                        data['id'] =  h.hexdigest()
                        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="inmigrante")
    
                except Exception,e:
                     scraperwiki.sqlite.save(unique_keys=['date'],data={"date":str(datetime.now()),"desc":str(e),"url":url}, table_name="log")
    
    return True

    #http://www.cemla.com/busqueda/buscador_action.php?
    #pageNum_Recordset1=5&
    #Apellido=pala&
    #Nombre=&
    #d-dia=01&
    #d-mes=01&
    #d-anio=1882&
    #h-dia=31&
    #h-mes=12&
    #h-anio=1882&
    #Apellido=PALA    

def saveCurrentDataAndVerify(data):
    year = data['year']
    first = data['first']
    second = data['second']
    page = data['page']
    id_process = str(year) + first + second + str(page)
    
    process = True

    try:
        result = scraperwiki.sqlite.execute("select id from processing where id = '"+id_process+"'")
        
        if len(result['data']) > 0 :
            process = False

    except Exception,e:
        print "Do nothing, first time, no table"

    data["id"] = id_process
    data["date"] = str(datetime.now()) 
    scraperwiki.sqlite.save(unique_keys=['id'],data=data, table_name="processing")

    #print id_process + "-" + str(process)
    return process

def normalize(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

#init
init()
