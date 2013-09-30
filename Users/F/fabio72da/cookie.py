import scraperwiki
import cookielib, urllib, urllib2, httplib2, re, datetime, time
from bs4 import BeautifulSoup as bs4

http = httplib2.Http()

url_base = 'http://apq.infrastrutture.gov.it'

# #################################################
# Form di ricerca principale [/frontEndWeb/ricerca]
#(solo per ottenere ID sessione da usare per le altre chiamate)

url = 'http://apq.infrastrutture.gov.it/frontEndWeb/ricerca'   
response, content = http.request(url, 'GET' )

#print response

jsessionid=response['set-cookie']
jsessionid=jsessionid[0:jsessionid.find(";")]

print "sessione: "+jsessionid


numScraped = 0

def ContentAt0(contents):
    return contents[0] if len(contents) > 0 else ""


lista_modalita=[
                "Stradale",
                "Ferroviaria", 
                "Aeroportuale", 
                "Portuale" ,
                "Interportuale Logistica", 
                """"Mobilita' urbana","""
                "Riqualificazione urbana", 
                "Altro..."
                ]

lista_modalita=[
                "Stradale",
                "Ferroviaria", 
                "Aeroportuale", 
                "Portuale" ,
                "Interportuale Logistica",
 
                "Riqualificazione urbana", 
                "Altro..."
                ]

territorio = [
("ABRUZZO",["TERAMO","PESCARA","L'AQUILA","CHIETI"] ) ,
("BASILICATA",["POTENZA "," MATERA"] ),
("CALABRIA",["VIBO VALENTIA","REGGIO CALABRIA","CROTONE","COSENZA","CATANZARO"] ),
("CAMPANIA",["SALERNO","NAPOLI","CASERTA","BENEVENTO","AVELLINO"] ),
("EMILIA ROMAGNA",["RIMINI","REGGIO EMILIA","RAVENNA","PIACENZA","PARMA","MODENA","FORLI'-CESENA","FERRARA","BOLOGNA"] ),
("FRIULI - VENEZIA GIULIA",["UDINE","TRIESTE","PORDENONE","GORIZIA"] ),
("LAZIO",["VITERBO","ROMA","RIETI","LATINA","FROSINONE"] ),
("LIGURIA ",["GENOVA","SAVONA","LA SPEZIA","IMPERIA"] ),
("LOMBARDIA",["VARESE","SONDRIO","PAVIA","MILANO","MANTOVA","LODI","LECCO","CREMONA","COMO","BRESCIA","BERGAMO"] ),
("MARCHE",["PESARO E URBINO"," MACERATA","ASCOLI PICENO","ANCONA"] ),
("MOLISE",["ISERNIA","CAMPOBASSO"] ),
("PIEMONTE ",["ALESSANDRIA","VERCELLI","VERBANO-CUSIO-OSSOLA"," TORINO","NOVARA","CUNEO","BIELLA","ASTI"] ),
("PUGLIA",["TARANTO","LECCE","FOGGIA","BRINDISI","BARI"] ),
("SARDEGNA",["SASSARI","ORISTANO","NUORO","CAGLIARI"] ),
("SICILIA ",["AGRIGENTO","TRAPANI","SIRACUSA","RAGUSA","PALERMO","MESSINA","ENNA","CATANIA","CALTANISSETTA"] ),
("TOSCANA",["SIENA","PRATO","PISTOIA","PISA","MASSA-CARRARA","LUCCA","LIVORNO","GROSSETO","FIRENZE","AREZZO"] ),
("TRENTINO - ALTO ADIGE",["TRENTO","BOLZANO"] ),
("UMBRIA",["TERNI","PERUGIA"] ),
("VALLE D'AOSTA",["AOSTA"] ),
("VENETO",["VICENZA","VERONA","VENEZIA","TREVISO","ROVIGO","PADOVA","BELLUNO"] )
]

territorio = [
("BASILICATA",["POTENZA "," MATERA"] ),
("CALABRIA",["VIBO VALENTIA","REGGIO CALABRIA","CROTONE","COSENZA","CATANZARO"] ),
("CAMPANIA",["SALERNO","NAPOLI","CASERTA","BENEVENTO","AVELLINO"] ),
("FRIULI - VENEZIA GIULIA",["UDINE","TRIESTE","PORDENONE","GORIZIA"] ),
("LAZIO",["VITERBO","ROMA","RIETI","LATINA","FROSINONE"] ),
("LIGURIA ",["GENOVA","SAVONA","LA SPEZIA","IMPERIA"] ),
("LOMBARDIA",["VARESE","SONDRIO","PAVIA","MILANO","MANTOVA","LODI","LECCO","CREMONA","COMO","BRESCIA","BERGAMO"] ),
("MARCHE",["PESARO E URBINO"," MACERATA","ASCOLI PICENO","ANCONA"] ),
("MOLISE",["ISERNIA","CAMPOBASSO"] ),
("PIEMONTE ",["ALESSANDRIA","VERCELLI","VERBANO-CUSIO-OSSOLA"," TORINO","NOVARA","CUNEO","BIELLA","ASTI"] ),
("PUGLIA",["TARANTO","LECCE","FOGGIA","BRINDISI","BARI"] ),
("SARDEGNA",["SASSARI","ORISTANO","NUORO","CAGLIARI"] ),
("SICILIA ",["AGRIGENTO","TRAPANI","SIRACUSA","RAGUSA","PALERMO","MESSINA","ENNA","CATANIA","CALTANISSETTA"] ),
("TOSCANA",["SIENA","PRATO","PISTOIA","PISA","MASSA-CARRARA","LUCCA","LIVORNO","GROSSETO","FIRENZE","AREZZO"] ),
("TRENTINO - ALTO ADIGE",["TRENTO","BOLZANO"] ),
("UMBRIA",["TERNI","PERUGIA"] ),
("VENETO",["VICENZA","VERONA","VENEZIA","TREVISO","ROVIGO","PADOVA","BELLUNO"] )
]

for modalita in lista_modalita:
    for regione, province in territorio:
    
        # ##################################################################
        # Form di ricerca-dettaglio province [/frontEndWeb/selezionaCriteri]
        
        # costruzione header
        headers= {
        'Host': 'apq.infrastrutture.gov.it',
        'Connection': 'keep-alive',
        'Content-Length': str(121+len(regione)+len(modalita)),
        'Cache-Control':' max-age=0',
        'Origin': 'http://apq.infrastrutture.gov.it',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://apq.infrastrutture.gov.it/frontEndWeb/ricerca',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Cookie': jsessionid
        }
        
        #print headers
        
        # costruzione POST body
        body= {
                'query':'',
                'modalita':modalita,
                'data1':'gg-mm-aaaa',
                'data2':'gg-mm-aaaa',
                'pagina':'registrazione',
                'regione':regione,
                'maxris':99,
                'mostraProvince':'Mostra Province'
                }
        
        # richiede il form di dettaglio delle province della regione/modalità indicata
        response, content = http.request("http://apq.infrastrutture.gov.it/frontEndWeb/selezionaCriteri", 'POST', headers=headers,body=urllib.urlencode(body))
        
        #print response
        #print content
        
        
        # #########################################
        # Lista APQ [/frontEndWeb/selezionaCriteri]
        
        for provincia in province:
        
            # costruzione header
            headers= {
            'Host': 'apq.infrastrutture.gov.it',
            'Connection': 'keep-alive',
            'Content-Length': str(124+len(regione)+len(provincia)+len(modalita)),
            'Cache-Control':' max-age=0',
            'Origin': 'http://apq.infrastrutture.gov.it',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://apq.infrastrutture.gov.it/frontEndWeb/ricerca',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Cookie': jsessionid
            }
            
            #print headers
            
            body= {
                    'query':'',
                    'modalita':modalita,
                    'data1':'gg-mm-aaaa',
                    'data2':'gg-mm-aaaa',
                    'pagina':'registrazione',
                    'regioneSelezionata':regione,
                    'provincia':provincia,
                    'maxris':'99',
                    'cerca':'Cerca'
                    }
            
            # richiede la lista degli APQ appartenti alla provincia/regione indicata + modalità indicata
            response, content = http.request("http://apq.infrastrutture.gov.it/frontEndWeb/selezionaCriteri", 'POST', headers=headers,body=urllib.urlencode(body))
            
            #print response
            #print content
            
            
            # ##################################################
            # Lista ? [/frontEndWeb/visualizzaInterventi]
            
            # costruzione header fisso
            headers= {
                    'Host': 'apq.infrastrutture.gov.it',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Referer': 'http://apq.infrastrutture.gov.it/frontEndWeb/selezionaCriteri',
                    'Accept-Encoding': 'gzip,deflate,sdch',
                    'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Cookie': jsessionid
                    }
            
            # scansione lista progetti tramite BeautifulSoup
            apq_soup = bs4(content)
            
            # compilazione re: /frontEndWeb/visualizzaInterventi?
            re_vizInt = re.compile("/frontEndWeb/visualizzaInterventi?")
            # compilazione re: /frontEndWeb/visualizzaInterventi?
            re_vizScheda = re.compile("/alovmap/cartografia.jsp?")
            
            # ciclo sulla lista degli APQ trovati
            for apq_link in apq_soup.find_all('a'):
                if re_vizInt.match(apq_link.get('href')):
                    #print 'link: '+url_base+urllib2.quote(apq_link.get('href').encode('ISO-8859-1'), safe="%/:=&?~#+!$,;'@()*[]")
                    response, content = http.request(url_base+urllib.quote(apq_link.get('href').encode('ISO-8859-1'), safe="%/:=&?~#+!$,;'@()*[]"), 'GET', headers=headers )
                    #print content
                    # scansione lista progetti tramite BeautifulSoup
                    ints_soup = bs4(content)
            
                    # ciclo sulla lista degli interventi trovati
                    print ints_soup.find_all('a')
                    for ints_link in ints_soup.find_all('a'):
                        if re_vizScheda.match(ints_link.get('href')):
                            print "["+modalita+"|"+regione+"|"+provincia+"] scheda: "+ints_link.get('href')
                            if not scraperwiki.sqlite.select("id from swdata where id='"+str(re.search(r"\?apq=(\w+)",ints_link.get('href')).group(1))+"'"):
                                response, content = http.request(url_base+urllib.quote(ints_link.get('href').encode('utf8'), safe="%/:=&?~#+!$,;'@()*[]"), 'GET', headers=headers )
                                #print content
                                int_soup = bs4(content)
                                intervento= dict(
                                        load_date = datetime.date.today().strftime("%Y%m%d"),
                                        load_time = time.strftime("%H:%M:%S",time.gmtime()),
                                        id = ContentAt0(int_soup.find(text="CODICE SIGI:").findNext('td').contents),
                                        regione=regione,
                                        provincia=provincia,
                                        tipo_settore=modalita,
                                        soggetto_attuatore = ContentAt0(int_soup.find(text="SOGGETTO ATTUATORE:").findNext('td').contents),
                                        oggetto = ContentAt0(int_soup.find(text="TITOLO INTERVENTO:").findNext('td').contents),
                                        livello_progettazione = ContentAt0(int_soup.find(text="LIVELLO PROGETTAZIONE:").findNext('td').contents),
                                        data_aggiud_lavori = ContentAt0(int_soup.find(text="AGGIUDICAZIONE LAVORI:").findNext('td').contents),
                                        data_esecuz_lavori = ContentAt0(int_soup.find(text="ESECUZIONE LAVORI:").findNext('td').contents),
                                        data_collaudo = ContentAt0(int_soup.find(text="COLLAUDO:").findNext('td').contents),
                                        data_esercizio = ContentAt0(int_soup.find(text="MESSA IN ESERCIZIO:").findNext('td').contents),
                                        costo = ContentAt0(int_soup.find(text="COSTO INTERVENTO:").findNext('td').contents)
                                        )
                    
                                print "["+modalita+"|"+regione+"|"+provincia+"] titolo: ",intervento.get('oggetto')
                    
                                # salvataggio dati nel db scraperwiki
                                scraperwiki.sqlite.save(['id'], intervento, table_name="swdata")
                                numScraped+=1
                                print ">>record salvato. ("+str(numScraped)+")"
                                time.sleep(3)import scraperwiki
import cookielib, urllib, urllib2, httplib2, re, datetime, time
from bs4 import BeautifulSoup as bs4

http = httplib2.Http()

url_base = 'http://apq.infrastrutture.gov.it'

# #################################################
# Form di ricerca principale [/frontEndWeb/ricerca]
#(solo per ottenere ID sessione da usare per le altre chiamate)

url = 'http://apq.infrastrutture.gov.it/frontEndWeb/ricerca'   
response, content = http.request(url, 'GET' )

#print response

jsessionid=response['set-cookie']
jsessionid=jsessionid[0:jsessionid.find(";")]

print "sessione: "+jsessionid


numScraped = 0

def ContentAt0(contents):
    return contents[0] if len(contents) > 0 else ""


lista_modalita=[
                "Stradale",
                "Ferroviaria", 
                "Aeroportuale", 
                "Portuale" ,
                "Interportuale Logistica", 
                """"Mobilita' urbana","""
                "Riqualificazione urbana", 
                "Altro..."
                ]

lista_modalita=[
                "Stradale",
                "Ferroviaria", 
                "Aeroportuale", 
                "Portuale" ,
                "Interportuale Logistica",
 
                "Riqualificazione urbana", 
                "Altro..."
                ]

territorio = [
("ABRUZZO",["TERAMO","PESCARA","L'AQUILA","CHIETI"] ) ,
("BASILICATA",["POTENZA "," MATERA"] ),
("CALABRIA",["VIBO VALENTIA","REGGIO CALABRIA","CROTONE","COSENZA","CATANZARO"] ),
("CAMPANIA",["SALERNO","NAPOLI","CASERTA","BENEVENTO","AVELLINO"] ),
("EMILIA ROMAGNA",["RIMINI","REGGIO EMILIA","RAVENNA","PIACENZA","PARMA","MODENA","FORLI'-CESENA","FERRARA","BOLOGNA"] ),
("FRIULI - VENEZIA GIULIA",["UDINE","TRIESTE","PORDENONE","GORIZIA"] ),
("LAZIO",["VITERBO","ROMA","RIETI","LATINA","FROSINONE"] ),
("LIGURIA ",["GENOVA","SAVONA","LA SPEZIA","IMPERIA"] ),
("LOMBARDIA",["VARESE","SONDRIO","PAVIA","MILANO","MANTOVA","LODI","LECCO","CREMONA","COMO","BRESCIA","BERGAMO"] ),
("MARCHE",["PESARO E URBINO"," MACERATA","ASCOLI PICENO","ANCONA"] ),
("MOLISE",["ISERNIA","CAMPOBASSO"] ),
("PIEMONTE ",["ALESSANDRIA","VERCELLI","VERBANO-CUSIO-OSSOLA"," TORINO","NOVARA","CUNEO","BIELLA","ASTI"] ),
("PUGLIA",["TARANTO","LECCE","FOGGIA","BRINDISI","BARI"] ),
("SARDEGNA",["SASSARI","ORISTANO","NUORO","CAGLIARI"] ),
("SICILIA ",["AGRIGENTO","TRAPANI","SIRACUSA","RAGUSA","PALERMO","MESSINA","ENNA","CATANIA","CALTANISSETTA"] ),
("TOSCANA",["SIENA","PRATO","PISTOIA","PISA","MASSA-CARRARA","LUCCA","LIVORNO","GROSSETO","FIRENZE","AREZZO"] ),
("TRENTINO - ALTO ADIGE",["TRENTO","BOLZANO"] ),
("UMBRIA",["TERNI","PERUGIA"] ),
("VALLE D'AOSTA",["AOSTA"] ),
("VENETO",["VICENZA","VERONA","VENEZIA","TREVISO","ROVIGO","PADOVA","BELLUNO"] )
]

territorio = [
("BASILICATA",["POTENZA "," MATERA"] ),
("CALABRIA",["VIBO VALENTIA","REGGIO CALABRIA","CROTONE","COSENZA","CATANZARO"] ),
("CAMPANIA",["SALERNO","NAPOLI","CASERTA","BENEVENTO","AVELLINO"] ),
("FRIULI - VENEZIA GIULIA",["UDINE","TRIESTE","PORDENONE","GORIZIA"] ),
("LAZIO",["VITERBO","ROMA","RIETI","LATINA","FROSINONE"] ),
("LIGURIA ",["GENOVA","SAVONA","LA SPEZIA","IMPERIA"] ),
("LOMBARDIA",["VARESE","SONDRIO","PAVIA","MILANO","MANTOVA","LODI","LECCO","CREMONA","COMO","BRESCIA","BERGAMO"] ),
("MARCHE",["PESARO E URBINO"," MACERATA","ASCOLI PICENO","ANCONA"] ),
("MOLISE",["ISERNIA","CAMPOBASSO"] ),
("PIEMONTE ",["ALESSANDRIA","VERCELLI","VERBANO-CUSIO-OSSOLA"," TORINO","NOVARA","CUNEO","BIELLA","ASTI"] ),
("PUGLIA",["TARANTO","LECCE","FOGGIA","BRINDISI","BARI"] ),
("SARDEGNA",["SASSARI","ORISTANO","NUORO","CAGLIARI"] ),
("SICILIA ",["AGRIGENTO","TRAPANI","SIRACUSA","RAGUSA","PALERMO","MESSINA","ENNA","CATANIA","CALTANISSETTA"] ),
("TOSCANA",["SIENA","PRATO","PISTOIA","PISA","MASSA-CARRARA","LUCCA","LIVORNO","GROSSETO","FIRENZE","AREZZO"] ),
("TRENTINO - ALTO ADIGE",["TRENTO","BOLZANO"] ),
("UMBRIA",["TERNI","PERUGIA"] ),
("VENETO",["VICENZA","VERONA","VENEZIA","TREVISO","ROVIGO","PADOVA","BELLUNO"] )
]

for modalita in lista_modalita:
    for regione, province in territorio:
    
        # ##################################################################
        # Form di ricerca-dettaglio province [/frontEndWeb/selezionaCriteri]
        
        # costruzione header
        headers= {
        'Host': 'apq.infrastrutture.gov.it',
        'Connection': 'keep-alive',
        'Content-Length': str(121+len(regione)+len(modalita)),
        'Cache-Control':' max-age=0',
        'Origin': 'http://apq.infrastrutture.gov.it',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://apq.infrastrutture.gov.it/frontEndWeb/ricerca',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Cookie': jsessionid
        }
        
        #print headers
        
        # costruzione POST body
        body= {
                'query':'',
                'modalita':modalita,
                'data1':'gg-mm-aaaa',
                'data2':'gg-mm-aaaa',
                'pagina':'registrazione',
                'regione':regione,
                'maxris':99,
                'mostraProvince':'Mostra Province'
                }
        
        # richiede il form di dettaglio delle province della regione/modalità indicata
        response, content = http.request("http://apq.infrastrutture.gov.it/frontEndWeb/selezionaCriteri", 'POST', headers=headers,body=urllib.urlencode(body))
        
        #print response
        #print content
        
        
        # #########################################
        # Lista APQ [/frontEndWeb/selezionaCriteri]
        
        for provincia in province:
        
            # costruzione header
            headers= {
            'Host': 'apq.infrastrutture.gov.it',
            'Connection': 'keep-alive',
            'Content-Length': str(124+len(regione)+len(provincia)+len(modalita)),
            'Cache-Control':' max-age=0',
            'Origin': 'http://apq.infrastrutture.gov.it',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://apq.infrastrutture.gov.it/frontEndWeb/ricerca',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Cookie': jsessionid
            }
            
            #print headers
            
            body= {
                    'query':'',
                    'modalita':modalita,
                    'data1':'gg-mm-aaaa',
                    'data2':'gg-mm-aaaa',
                    'pagina':'registrazione',
                    'regioneSelezionata':regione,
                    'provincia':provincia,
                    'maxris':'99',
                    'cerca':'Cerca'
                    }
            
            # richiede la lista degli APQ appartenti alla provincia/regione indicata + modalità indicata
            response, content = http.request("http://apq.infrastrutture.gov.it/frontEndWeb/selezionaCriteri", 'POST', headers=headers,body=urllib.urlencode(body))
            
            #print response
            #print content
            
            
            # ##################################################
            # Lista ? [/frontEndWeb/visualizzaInterventi]
            
            # costruzione header fisso
            headers= {
                    'Host': 'apq.infrastrutture.gov.it',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Referer': 'http://apq.infrastrutture.gov.it/frontEndWeb/selezionaCriteri',
                    'Accept-Encoding': 'gzip,deflate,sdch',
                    'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Cookie': jsessionid
                    }
            
            # scansione lista progetti tramite BeautifulSoup
            apq_soup = bs4(content)
            
            # compilazione re: /frontEndWeb/visualizzaInterventi?
            re_vizInt = re.compile("/frontEndWeb/visualizzaInterventi?")
            # compilazione re: /frontEndWeb/visualizzaInterventi?
            re_vizScheda = re.compile("/alovmap/cartografia.jsp?")
            
            # ciclo sulla lista degli APQ trovati
            for apq_link in apq_soup.find_all('a'):
                if re_vizInt.match(apq_link.get('href')):
                    #print 'link: '+url_base+urllib2.quote(apq_link.get('href').encode('ISO-8859-1'), safe="%/:=&?~#+!$,;'@()*[]")
                    response, content = http.request(url_base+urllib.quote(apq_link.get('href').encode('ISO-8859-1'), safe="%/:=&?~#+!$,;'@()*[]"), 'GET', headers=headers )
                    #print content
                    # scansione lista progetti tramite BeautifulSoup
                    ints_soup = bs4(content)
            
                    # ciclo sulla lista degli interventi trovati
                    print ints_soup.find_all('a')
                    for ints_link in ints_soup.find_all('a'):
                        if re_vizScheda.match(ints_link.get('href')):
                            print "["+modalita+"|"+regione+"|"+provincia+"] scheda: "+ints_link.get('href')
                            if not scraperwiki.sqlite.select("id from swdata where id='"+str(re.search(r"\?apq=(\w+)",ints_link.get('href')).group(1))+"'"):
                                response, content = http.request(url_base+urllib.quote(ints_link.get('href').encode('utf8'), safe="%/:=&?~#+!$,;'@()*[]"), 'GET', headers=headers )
                                #print content
                                int_soup = bs4(content)
                                intervento= dict(
                                        load_date = datetime.date.today().strftime("%Y%m%d"),
                                        load_time = time.strftime("%H:%M:%S",time.gmtime()),
                                        id = ContentAt0(int_soup.find(text="CODICE SIGI:").findNext('td').contents),
                                        regione=regione,
                                        provincia=provincia,
                                        tipo_settore=modalita,
                                        soggetto_attuatore = ContentAt0(int_soup.find(text="SOGGETTO ATTUATORE:").findNext('td').contents),
                                        oggetto = ContentAt0(int_soup.find(text="TITOLO INTERVENTO:").findNext('td').contents),
                                        livello_progettazione = ContentAt0(int_soup.find(text="LIVELLO PROGETTAZIONE:").findNext('td').contents),
                                        data_aggiud_lavori = ContentAt0(int_soup.find(text="AGGIUDICAZIONE LAVORI:").findNext('td').contents),
                                        data_esecuz_lavori = ContentAt0(int_soup.find(text="ESECUZIONE LAVORI:").findNext('td').contents),
                                        data_collaudo = ContentAt0(int_soup.find(text="COLLAUDO:").findNext('td').contents),
                                        data_esercizio = ContentAt0(int_soup.find(text="MESSA IN ESERCIZIO:").findNext('td').contents),
                                        costo = ContentAt0(int_soup.find(text="COSTO INTERVENTO:").findNext('td').contents)
                                        )
                    
                                print "["+modalita+"|"+regione+"|"+provincia+"] titolo: ",intervento.get('oggetto')
                    
                                # salvataggio dati nel db scraperwiki
                                scraperwiki.sqlite.save(['id'], intervento, table_name="swdata")
                                numScraped+=1
                                print ">>record salvato. ("+str(numScraped)+")"
                                time.sleep(3)