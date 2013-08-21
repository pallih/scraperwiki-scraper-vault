import scraperwiki
import cookielib, urllib, urllib2, httplib2, re, datetime, time
from bs4 import BeautifulSoup as bs4
import types

http = httplib2.Http()

url_base = 'http://bandigara.avcp.it'

# #################################################
# Form di ricerca principale [/frontEndWeb/ricerca]
#(solo per ottenere ID sessione da usare per le altre chiamate)

#url = 'http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/GoToAdvancedSearch.action'
url = 'http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/NewSearch.action'   
response, content = http.request(url, 'GET' )

print response

cookie=response['set-cookie']
jsessionid=cookie[0:cookie.find(";")]

print "cookie: "+cookie
print "jsession: "+jsessionid

def ContentAt0(contents):
    return contents[0] if len(contents) > 0 else ""

#funzione di scraping di una scheda gara
def ScrapeGara(idGara,headers):
    
    #accede a pagina web
    response, content = http.request("http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/GoToDetail.action?numGara="+str(idGara),'GET',headers=headers)
    # scansione scheda gara tramite BeautifulSoup
    gara_bs = bs4(content)
    
    if gara_bs.find(text="La gara non esiste o non è stata pubblicata") is not None:
        gara_scrape= dict(
            load_date = datetime.date.today().strftime("%Y%m%d"),
            load_time = time.strftime("%H:%M:%S",time.gmtime()),
            load_result = 'ko',
            id = str(idGara)
            )
    else:
        try:
            gara_scrape= dict(
                load_date = datetime.date.today().strftime("%Y%m%d"),
                load_time = time.strftime("%H:%M:%S",time.gmtime()),
                load_result = 'ok',
                id = ContentAt0(gara_bs.find(text="Numero documento (codice gara)").findNext('td').contents),
                oggetto = ContentAt0(gara_bs.find(text="Oggetto").findNext('td').contents),
                data_pubbl_gara = ContentAt0(gara_bs.find(text="Data pubblicazione GURI").findNext('td').contents),
                data_scadenza_gara = ContentAt0(gara_bs.find(text="Scadenza").findNext('td').contents),
                luogo = ContentAt0(gara_bs.find(text="Luogo").findNext('td').contents),
                staz_app = ContentAt0(gara_bs.find(text="Denominazione stazione appaltante").findNext('td').contents),
                staz_app_cf = ContentAt0(gara_bs.find(text="Codice fiscale stazione appaltante").findNext('td').contents),
                tipo_contratto = ContentAt0(gara_bs.find(text="Tipologia contratto").findNext('td').contents),
                procedura_gara = ContentAt0(gara_bs.find(text="Procedura").findNext('td').contents),
                cpv_gara = ContentAt0(gara_bs.find(text="Codice CPV").findNext('td').contents),
                settore_gara = ContentAt0(gara_bs.find(text="Settore").findNext('td').contents),
                modo_realizz = ContentAt0(gara_bs.find(text="Modalità realizzazione").findNext('td').contents),
                CIG_aq = ContentAt0(gara_bs.find(text="CIG accordo quadro").findNext('td').contents)
                )
        except:
            gara_scrape= dict()

    return gara_scrape, gara_bs 

#funzione di scraping di una scheda lotto
def ScrapeLotto(idLotto,headers):
    response, content = http.request("http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/GoToDetailLotto.action?numLotto="+idLotto,'GET',headers=headers)

    # scansione scheda gara tramite BeautifulSoup
    lotto_bs = bs4(content)

    try:
        lotto_scrape= dict(
            load_date = datetime.date.today().strftime("%Y%m%d"),
            load_time = time.strftime("%H:%M:%S",time.gmtime()),
            idlotto = idlotto,
            cig = ContentAt0(lotto_bs.find(text="CIG").findNext('td').contents),
            oggetto_lotto = ContentAt0(lotto_bs.find(text="Oggetto").findNext('td').contents),
            importo_ba = ContentAt0(lotto_bs.find(text="Importo a base d'asta comprensivo degli oneri per la sicurezza").findNext('td').contents),
            tipo_contratto = ContentAt0(lotto_bs.find(text="Tipologia del contratto").findNext('td').contents),
            cpv = ContentAt0(lotto_bs.find(text="CPV").findNext('td').contents),
            categ_qualif = ContentAt0(lotto_bs.find(text="Categoria di qualificazione").findNext('td').contents),
            classif_qualif = ContentAt0(lotto_bs.find(text="Classificazione di qualificazione").findNext('td').contents),
            num_aggiud = ContentAt0(lotto_bs.find(text="Numero pubblicazione aggiudicazione").findNext('td').contents),
            data_aggiud = ContentAt0(lotto_bs.find(text="Data pubblicazione aggiudicazione").findNext('td').contents),
            criteria_aggiud = ContentAt0(lotto_bs.find(text="Criteri di aggiudicazione").findNext('td').contents),
            cod_istat = ContentAt0(lotto_bs.find(text="Codice ISTAT").findNext('td').contents),
            cod_nuts = ContentAt0(lotto_bs.find(text="Codice NUTS").findNext('td').contents),
            procedura = ContentAt0(lotto_bs.find(text="Procedura").findNext('td').contents)
            )
    except:
        lotto_scrape= dict()

    return lotto_scrape, lotto_bs 

def ListLotti(soup):

    link_lotti=[]
    # compilazione re: GoToDetailLotto.action?numLotto=
    re_goLotto = re.compile("GoToDetailLotto.action")
    
    # ciclo sulla lista dei link ai lotti
    for anchor in soup.find_all('a'):
        if re_goLotto.match(anchor.get('href')):
            link_lotti.append(anchor.get('href')[anchor.get('href').find("=")+1:])
    return link_lotti

parms = {
"tipologia":"LAVORI",
"settore":"",
"oggetto":"",
"categoria":"",
"classifica":"",
"metodoScelta":"Corrisponde",
"CPV":"",
"criterioAgg":"",
"sceltaContr":"",
"modalitaRealizzazione":"",
"cig":"",
"localizzazione":"",
"CFAmm":"",
"denominazioneAmm":"",
"importoMin":"",
"importoMax":"",
"dataPubb[0]":"",
"dataPubb[1]":"",
"dataPubb[2]":"",
"dataPubbFine[0]":"",
"dataPubbFine[1]":"",
"dataPubbFine[2]":"",
"dataPubbAgg[0]":"",
"dataPubbAgg[1]":"",
"dataPubbAgg[2]":"",
"dataPubbAggFine[0]":"",
"dataPubbAggFine[1]":"",
"dataPubbAggFine[2]":"",
"dataScadenza[0]":"",
"dataScadenza[1]":"",
"dataScadenza[2]":"",
"dataScadenzaFine[0]":"",
"dataScadenzaFine[1]":"",
"dataScadenzaFine[2]":"",
"tipologiaBando":"Attivi",
"listNumber":"50",
"sortColumn":"0",
"sortType":"1"
}



# costruzione header
headers= {
'Host': 'bandigara.avcp.it',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Referer': 'http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/GoToAdvancedSearch.action',
'Accept-Encoding': 'gzip,deflate,sdch',
'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Cookie': cookie
}

# costruzione POST body
"""
GET http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/GoToDetail.action?numGara=4646558 HTTP/1.1
Host: bandigara.avcp.it
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip,deflate,sdch
Accept-Language: it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
Cookie: JSESSIONID=7AD0960CC86966DEB6DF82E27B0353DA.node2; __utma=22302315.1818442550.1353257014.1353754865.1353756836.3; __utmc=22302315; __utmz=22302315.1353756836.3.2.utmcsr=bandigara.avcp.it|utmccn=(referral)|utmcmd=referral|utmcct=/AVCP-ConsultazioneBandiGara/; __utma=178142134.1223260485.1353256612.1353757128.1353759310.9; __utmb=178142134.7.10.1353759310; __utmc=178142134; __utmz=178142134.1353757128.8.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)
"""


"""
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
"""
gareScraped = 0
lottiScraped = 0
for numgara in range(4487380,3600000,-10): #gara con molti lotti: 2961254   4641000,4645000

    scraping, content_soup =ScrapeGara(numgara,headers)
    print "[bando:%s] %s" % (numgara, str(scraping))

    #se esiste la scheda bando si salva e si cercano i lotti
    if scraping:

        # salvataggio dati nel db scraperwiki
        scraperwiki.sqlite.save(['id'], scraping, table_name="avcp_bandi")
        gareScraped +=1
        print ">>record salvato. (%d+%d)" % (gareScraped,lottiScraped)

        #ricerca lotti
        list_idlotti= ListLotti(content_soup)
    
        for idlotto in list_idlotti:
            headers_lotto= {
                            'Host': 'bandigara.avcp.it',
                            'Connection': 'keep-alive',
                            'Cache-Control': 'max-age=0',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Referer': 'Referer: http://bandigara.avcp.it/AVCP-ConsultazioneBandiGara/GoToDetail.action?numGara='+str(numgara),
                            'Accept-Encoding': 'gzip,deflate,sdch',
                            'Accept-Language': 'it-IT,it;q=0.8,en-US;q=0.6,en;q=0.4',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                            'Cookie': cookie
                            }
    
            scraping, content_soup = ScrapeLotto(idlotto,headers_lotto)
            scraping['id']=numgara #aggiunge id gara
            print "[bando:%d|lotto:%s] %s" % (numgara, idlotto, scraping)

            # salvataggio dati nel db scraperwiki
            scraperwiki.sqlite.save(['id','idlotto'], scraping, table_name="avcp_lotti")
            lottiScraped +=1
            print ">>record salvato. (%d+%d)" % (gareScraped,lottiScraped)
            time.sleep(4)

"""
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

"""



"""
<form id="AdvancedSearch" name="AdvancedSearch" action="/AVCP-ConsultazioneBandiGara/AdvancedSearch.action" method="post">

<select name="tipologia" id="AdvancedSearch_tipologia">
    <option value="LAVORI">LAVORI</option>
<select name="settore" id="AdvancedSearch_settore">
    <option value=""></option>
<input type="text" name="oggetto" value="" id="AdvancedSearch_oggetto" />

<select name="categoria" id="AdvancedSearch_categoria">
    <option value=""></option>
<select name="classifica" id="AdvancedSearch_classifica">
    <option value=""></option>

<input type="radio" name="metodoScelta" id="AdvancedSearch_metodoSceltaFino a" value="Fino a" />
<input type="radio" name="metodoScelta" id="AdvancedSearch_metodoSceltaCorrisponde" checked="checked" value="Corrisponde"/>

<input type="text" name="CPV" value="" id="AdvancedSearch_CPV"/>
<select name="criterioAgg" id="AdvancedSearch_criterioAgg">
    <option value="">
<select name="sceltaContr" id="AdvancedSearch_sceltaContr">
    <option value=""></option>
<select name="modalitaRealizzazione" id="AdvancedSearch_modalitaRealizzazione">
    <option value=""></option>
<input type="text" name="cig" value="" id="AdvancedSearch_cig" />
<input type="text" name="localizzazione" value="" id="AdvancedSearch_localizzazione"/>
<input type="text" name="CFAmm" value="" id="AdvancedSearch_CFAmm" class="large"/>
<input type="text" name="denominazioneAmm" value="" id="AdvancedSearch_denominazioneAmm" class="larger"/>
<input type="text" name="importoMin" value="" id="AdvancedSearch_importoMin" class="small"/>
<input type="text" name="importoMax" value="" id="AdvancedSearch_importoMax" class="small"/>
<input type="text" name="dataPubb[0]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubb_0_" />
<input type="text" name="dataPubb[1]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubb_1_" />
<input type="text" name="dataPubb[2]" size="4" maxlength="4" value="" id="AdvancedSearch_dataPubb_2_" />
<input type="text" name="dataPubbFine[0]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubbFine_0_" />
<input type="text" name="dataPubbFine[1]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubbFine_1_" />
<input type="text" name="dataPubbFine[2]" size="4" maxlength="4" value="" id="AdvancedSearch_dataPubbFine_2_" />
<input type="text" name="dataPubbAgg[0]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubbAgg_0_" />
<input type="text" name="dataPubbAgg[1]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubbAgg_1_" />
<input type="text" name="dataPubbAgg[2]" size="4" maxlength="4" value="" id="AdvancedSearch_dataPubbAgg_2_" />
<input type="text" name="dataPubbAggFine[0]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubbAggFine_0_" />
<input type="text" name="dataPubbAggFine[1]" size="2" maxlength="2" value="" id="AdvancedSearch_dataPubbAggFine_1_" />
<input type="text" name="dataPubbAggFine[2]" size="4" maxlength="4" value="" id="AdvancedSearch_dataPubbAggFine_2_" />
<input type="text" name="dataScadenza[0]" size="2" maxlength="2" value="" id="AdvancedSearch_dataScadenza_0_" />
<input type="text" name="dataScadenza[1]" size="2" maxlength="2" value="" id="AdvancedSearch_dataScadenza_1_" />
<input type="text" name="dataScadenza[2]" size="4" maxlength="4" value="" id="AdvancedSearch_dataScadenza_2_" />
<input type="text" name="dataScadenzaFine[0]" size="2" maxlength="2" value="" id="AdvancedSearch_dataScadenzaFine_0_" />
<input type="text" name="dataScadenzaFine[1]" size="2" maxlength="2" value="" id="AdvancedSearch_dataScadenzaFine_1_" />
<input type="text" name="dataScadenzaFine[2]" size="4" maxlength="4" value="" id="AdvancedSearch_dataScadenzaFine_2_" />
<input type="radio" name="tipologiaBando" id="AdvancedSearch_tipologiaBandoAttivi" checked="checked" value="Attivi" 
<input type="radio" name="tipologiaBando" id="AdvancedSearch_tipologiaBandoArchivio (scaduti)" value="Archivio (scaduti)"/>
<select name="listNumber" id="AdvancedSearch_listNumber">
    <option value="10" selected="selected">50</option>
</select>
<select name="sortColumn" id="AdvancedSearch_sortColumn">
    <option value="0" selected="selected">Numero Gara</option>
</select>
<select name="sortType" id="AdvancedSearch_sortType">
    <option value="1">Discendente</option>
</select>
<input type="submit" id="AdvancedSearch_2" value="Cerca"/>
"""