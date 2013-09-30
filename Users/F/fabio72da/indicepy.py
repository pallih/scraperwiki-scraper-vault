import scraperwiki
import lxml.html
import urllib, urllib2, datetime, time, re, copy

urlbase="http://www.indicepa.gov.it/ricerca/"
urllist="risultati-alfabeto.php";

##http://www.indicepa.gov.it/ricerca/risultati-alfabeto.php?lettera=A
http://www.indicepa.gov.it/ricerca/dettaglioamministrazione.php?cod_amm=ATO_PU

html_content = urllib2.urlopen(urlbase+urllist+"?lettera=A").read();
page = lxml.html.fromstring(html_content)


anchors = page.cssselect("a") 
hrefs= []
i=0
for a in anchors:
    if re.match("dettaglioamministrazione.php",a.attrib['href']) and \
                    not scraperwiki.sqlite.select("id from swdata where cod_amm="+str(re.search(r'\?cod_amm=(\w+)',a.attrib['href']).group(1))):
    i+=1
    hrefs.append((a,i))
    
for a,i in hrefs:
    time.sleep(3)
    print "[](",str(i)+"/"+str(len(hrefs))+") >> "+a.attrib['href']
    html_content = scraperwiki.scrape(urlbase+a.attrib['href'])
    html = lxml.html.fromstring(html_content)
    
    pa = dict(
              load_date = datetime.date.today().strftime("%Y%m%d"),
              load_time = time.strftime("%H:%M:%S",time.gmtime()),
              cod_amm = str(re.search(r'\?cod_amm=(\w+)',a.attrib['href']).group(1))""",
              stazapp = TextAt0(html.cssselect("span#lbl_denominaz")),
              stato_bando = tender,
              provincia = prov,
              data_fine_lav = TextAt0(html.cssselect("span#data_fine_lav")),
              note = TextAt0(html.cssselect("span#note")),
              url_esito = TextAt0(html.cssselect("span#down_all"))"""
             )
    
    print " titolo: ",gara.get('oggetto')
    
    ## salvataggio dati nel db scraperwiki
    scraperwiki.sqlite.save(['id'], gara, table_name="swdata")
    numScraped+=1    
    print ">>record salvato. ("+str(numScraped)+")"
























viewstate=html.cssselect("input#__VIEWSTATE") #$viewstate = $html->find("input[id=__VIEWSTATE]");
eventval=html.cssselect("input#__EVENTVALIDATION") #$eventval= $html->find("input[id=__EVENTVALIDATION]");

print "viewstate: "+viewstate[0].value
print "eventval: "+eventval[0].value


def posting(url, params, method):
    params = urllib.urlencode(params)
    try:
        if method=='POST':
            f = urllib2.urlopen(url, params)
        else:
            f = urllib2.urlopen(url+'?'+params)
    except:
        return (None, None)
    return (f.read(), f.code)

def TextAt0(alist):
    return alist[0].text if len(alist) > 0 else ""

provinces= [
'AG',
'AL',
'AN',
'AO',
'AP',
'AQ',
'AR',
'AT',
'AV',
'BA',
'BG',
'BI',
'BL',
'BN',
'BO',
'BR',
'BS',
'BT',
'BZ',
'CA',
'CB',
'CE',
'CH',
'CI',
'CL',
'CN',
'CO',
'CR',
'CS',
'CT',
'CZ',
'EN',
'FC',
'FE',
'FG',
'FI',
'FM',
'FR',
'GE',
'GO',
'GR',
'IM',
'IS',
'KR',
'LC',
'LE',
'LI',
'LO',
'LT',
'LU',
'MB',
'MC',
'ME',
'MI',
'MN',
'MO',
'MS',
'MT',
'NA',
'NO',
'NU',
'OG',
'OR',
'OT',
'PA',
'PC',
'PD',
'PE',
'PG',
'PI',
'PN',
'PO',
'PR',
'PT',
'PU',
'PV',
'PZ',
'RA',
'RC',
'RE',
'RG',
'RI',
'RM',
'RN',
'RO',
'SA',
'SI',
'SO',
'SP',
'SR',
'SS',
'SV',
'TA',
'TE',
'TN',
'TO',
'TP',
'TR',
'TS',
'TV',
'UD',
'VA',
'VB',
'VC',
'VE',
'VI',
'VR',
'VS',
'VT',
'VV'
]


tenders= ['ba','agg']


#set min max dates
mindate=datetime.date(2000, 1, 1)
maxdate=datetime.date.today()

numScraped=0;

for tender in tenders:
    for prov in provinces:

        #set inf=min sup=max
        infdate=copy.deepcopy(mindate)
        supdate=copy.deepcopy(maxdate)
        print "["+tender+"|"+prov+"] time range: "+infdate.strftime('%d/%m/%Y')+" <-> "+supdate.strftime('%d/%m/%Y')
        
        #ciclo su frame di tempo
        while not (infdate==supdate and supdate==maxdate): 
            #ciclo infinito finchè la pagina è di errore     
            while True:
                #prepara i dati per la richiesta POST
                data = {
                            '__VIEWSTATE':viewstate[0].value,
                             '__EVENTVALIDATION':eventval[0].value,
                             'tipoappalto':tender,
                             'regioni':'- qualsiasi -',
                             'province':prov,
                             'tipo_ente':'- qualsiasi -',
                             'tipoapp':'1',
                             'imp_fino_a':'',
                             'cat_qual':'- qualsiasi -',
                             'pubbl_dopo':infdate.strftime('%d/%m/%Y'),
                             'pubbl_prima':supdate.strftime('%d/%m/%Y')    
                        }
                #richiesta POST
                content, response = posting( urlbase+urllist, data, 'POST')
                if response:
                    #parsing lxml
                    page = lxml.html.fromstring(content)
                    if page.cssselect("span#err_source"):
                        print "["+tender+"|"+prov+"] errore: standby 10s"
                        time.sleep(10)
                    else:
                        break
                else:
                    print ">> errore posting url ... retry"
        
            #se la pagina non ha risultati => skip next timeframe
            if page.cssselect("span#no_res"):
                print "["+tender+"|"+prov+"] nessun risultato"
                #inf=sup & sup=max
                infdate=copy.deepcopy(supdate)
                supdate=copy.deepcopy(maxdate)
                print "["+tender+"|"+prov+"] no res >> new range: "+str(infdate)+" <-> "+str(supdate)
                # ritorna al while per valutare se la condizione è ancora valida
                # se inf=sup=max => si esce dal ciclo xkè è stato scansionato tutto il range temporale
                continue
    
            #numero di risultati della pagina
            numres = page.cssselect("span#num_res")
            print "["+tender+"|"+prov+"] risultati: "+TextAt0(numres)
            
            #check: ci sono troppi (>200) risultati?
            if re.search(r'visualizzati',TextAt0(numres)):
                #sup=inf+(sup-inf)/2
                #supdate=infdate+(supdate-infdate)/2
                supdate = infdate + datetime.timedelta(days=int((supdate-infdate).days/2))
                print "["+tender+"|"+prov+"] too res >> new range: "+str(infdate)+" <-> "+str(supdate)            
                # ritorna al while per valutare se nuova condizione
                continue
            
            anchors = page.cssselect("a") 
            hrefs= []
            i=0
            for a in anchors:
                if re.match("dett_"+tender+"_lav.aspx",a.attrib['href']) and \
                    not scraperwiki.sqlite.select("id from swdata where id="+str(re.search(r'\?id=(\d+)',a.attrib['href']).group(1))+" and stato_bando = '"+tender+"'"):
                    i+=1
                    hrefs.append((a,i))
    
            for a,i in hrefs:
                time.sleep(3)
                print "["+tender+"|"+prov+"](",str(i)+"/"+str(len(hrefs))+") >> "+a.attrib['href'],
                html_content = scraperwiki.scrape("https://www.serviziocontrattipubblici.it/ricerca/"+a.attrib['href'])
                html = lxml.html.fromstring(html_content)
    
                gara = dict(
                        load_date = datetime.date.today().strftime("%Y%m%d"),
                        load_time = time.strftime("%H:%M:%S",time.gmtime()),
                        id = str(re.search(r'\?id=(\d+)',a.attrib['href']).group(1)),
                        stazapp = TextAt0(html.cssselect("span#lbl_denominaz")),
                        stazapp_cfpiva= TextAt0(html.cssselect("span#lbl_cf_piva")),
                        stazapp_ufficio= TextAt0(html.cssselect("span#lbl_ufficio")),
                        tipo_settore = TextAt0(html.cssselect("span#tipo_settore")),
                        infr_strat = TextAt0(html.cssselect("span#infr_strat")),
                        tipo_bando = TextAt0(html.cssselect("span#tipo_realizz")),
                        stato_bando = tender,
                        contr_gen = TextAt0(html.cssselect("span#contr_gen")),
                        oggetto = TextAt0(html.cssselect("span#oggetto")),
                        lotti = TextAt0(html.cssselect("span#lotti")),
                        num_lotti = TextAt0(html.cssselect("span#num_lotto")),
                        cpv1 = TextAt0(html.cssselect("span#desccpv1")),
                        cpv2 = TextAt0(html.cssselect("span#desccpv2")),
                        cpv3 = TextAt0(html.cssselect("span#desccpv3")),
                        tipo_interv = TextAt0(html.cssselect("span#tipo_interv")),
                        cup = TextAt0(html.cssselect("span#cup")),
                        cig_list = TextAt0(html.cssselect("span#elenco_cig")),
                        cig_mono = TextAt0(html.cssselect("span#cig_no_lotti")),
                        luogo = TextAt0(html.cssselect("span#desc_istat")),
                        provincia = prov,
                        imp_base = TextAt0(html.cssselect("span#imp_base")),
                        sicur= TextAt0(html.cssselect("span#lbl_sicurez")),
                        imp_sicur = TextAt0(html.cssselect("span#imp_sicurez")),
                        imp_contr = TextAt0(html.cssselect("span#imp_contratt")),
                        pct_rib = TextAt0(html.cssselect("span#perc_rib_asta")),
                        proc_agg = TextAt0(html.cssselect("span#proc_agg")),
                        data_guce = TextAt0(html.cssselect("span#data_guce")),
                        data_guri = TextAt0(html.cssselect("span#data_guri")),
                        data_albo = TextAt0(html.cssselect("span#data_albo")),
                        prof_comm = TextAt0(html.cssselect("span#prof_comm")),
                        n_quot_naz = TextAt0(html.cssselect("span#n_quot_naz")),
                        n_quot_reg = TextAt0(html.cssselect("span#n_quot_reg")),
                        data_guce_agg = TextAt0(html.cssselect("span#data_guce_agg")),
                        data_scadenza = TextAt0(html.cssselect("span#data_scadenza")),
                        imp_corpo = TextAt0(html.cssselect("span#imp_corpo")),
                        imp_misura = TextAt0(html.cssselect("span#imp_misura")),
                        imp_corpo_mis = TextAt0(html.cssselect("span#imp_corpo_mis")),
                        cat_prev = TextAt0(html.cssselect("span#cat_prev")),
                        imp_cat_prev = TextAt0(html.cssselect("span#imp_cat_prev")),
                        cat_sc1 = TextAt0(html.cssselect("span#cat_scorp1")),
                        imp_cat_sc1 = TextAt0(html.cssselect("span#imp_cat_scorp1")),
                        cat_sc2 = TextAt0(html.cssselect("span#cat_scorp2")),
                        imp_cat_sc2 = TextAt0(html.cssselect("span#imp_cat_scorp2")),
                        cat_sc3 = TextAt0(html.cssselect("span#cat_scorp3")),
                        imp_cat_sc3 = TextAt0(html.cssselect("span#imp_cat_scorp3")),
                        cat_sc4 = TextAt0(html.cssselect("span#cat_scorp4")),
                        imp_cat_sc4 = TextAt0(html.cssselect("span#imp_cat_scorp4")),
                        cat_sc5 = TextAt0(html.cssselect("span#cat_scorp5")),
                        imp_cat_sc5 = TextAt0(html.cssselect("span#imp_cat_scorp5")),
                        cat_sc6 = TextAt0(html.cssselect("span#cat_scorp6")),
                        imp_cat_sc6 = TextAt0(html.cssselect("span#imp_cat_scorp6")),
                        cat_sc7 = TextAt0(html.cssselect("span#cat_scorp7")),
                        imp_cat_sc7 = TextAt0(html.cssselect("span#imp_cat_scorp7")),
                        data_agg = TextAt0(html.cssselect("span#data_agg")),
                        n_imp_rich = TextAt0(html.cssselect("span#n_imp_rich")),
                        n_imp_inv = TextAt0(html.cssselect("span#n_imp_inv")),
                        n_imp_off = TextAt0(html.cssselect("span#n_imp_off")),
                        n_imp_amm = TextAt0(html.cssselect("span#n_imp_amm")),
                        lista_agg = TextAt0(html.cssselect("span#list_az")),
                        tipo_agg = TextAt0(html.cssselect("span#tipo_agg")),
                        durata = TextAt0(html.cssselect("span#n_gg_termine")),
                        data_fine_lav = TextAt0(html.cssselect("span#data_fine_lav")),
                        note = TextAt0(html.cssselect("span#note")),
                        url_esito = TextAt0(html.cssselect("span#down_all"))
                        )
    
                print " titolo: ",gara.get('oggetto')
    
                # salvataggio dati nel db scraperwiki
                scraperwiki.sqlite.save(['id'], gara, table_name="swdata")
                numScraped+=1    
                print ">>record salvato. ("+str(numScraped)+")"

            #dopo aver acquisito le gare si sposta in avanti la finestra temporale
            infdate=copy.deepcopy(supdate)
            supdate=copy.deepcopy(maxdate)
            print "["+tender+"|"+prov+"] end scraping >> new range: "+str(infdate)+" <-> "+str(supdate)

print ">> Sessione conclusa >>Totale bandi acquisiti: "+str(numScraped)
import scraperwiki
import lxml.html
import urllib, urllib2, datetime, time, re, copy

urlbase="http://www.indicepa.gov.it/ricerca/"
urllist="risultati-alfabeto.php";

##http://www.indicepa.gov.it/ricerca/risultati-alfabeto.php?lettera=A
http://www.indicepa.gov.it/ricerca/dettaglioamministrazione.php?cod_amm=ATO_PU

html_content = urllib2.urlopen(urlbase+urllist+"?lettera=A").read();
page = lxml.html.fromstring(html_content)


anchors = page.cssselect("a") 
hrefs= []
i=0
for a in anchors:
    if re.match("dettaglioamministrazione.php",a.attrib['href']) and \
                    not scraperwiki.sqlite.select("id from swdata where cod_amm="+str(re.search(r'\?cod_amm=(\w+)',a.attrib['href']).group(1))):
    i+=1
    hrefs.append((a,i))
    
for a,i in hrefs:
    time.sleep(3)
    print "[](",str(i)+"/"+str(len(hrefs))+") >> "+a.attrib['href']
    html_content = scraperwiki.scrape(urlbase+a.attrib['href'])
    html = lxml.html.fromstring(html_content)
    
    pa = dict(
              load_date = datetime.date.today().strftime("%Y%m%d"),
              load_time = time.strftime("%H:%M:%S",time.gmtime()),
              cod_amm = str(re.search(r'\?cod_amm=(\w+)',a.attrib['href']).group(1))""",
              stazapp = TextAt0(html.cssselect("span#lbl_denominaz")),
              stato_bando = tender,
              provincia = prov,
              data_fine_lav = TextAt0(html.cssselect("span#data_fine_lav")),
              note = TextAt0(html.cssselect("span#note")),
              url_esito = TextAt0(html.cssselect("span#down_all"))"""
             )
    
    print " titolo: ",gara.get('oggetto')
    
    ## salvataggio dati nel db scraperwiki
    scraperwiki.sqlite.save(['id'], gara, table_name="swdata")
    numScraped+=1    
    print ">>record salvato. ("+str(numScraped)+")"
























viewstate=html.cssselect("input#__VIEWSTATE") #$viewstate = $html->find("input[id=__VIEWSTATE]");
eventval=html.cssselect("input#__EVENTVALIDATION") #$eventval= $html->find("input[id=__EVENTVALIDATION]");

print "viewstate: "+viewstate[0].value
print "eventval: "+eventval[0].value


def posting(url, params, method):
    params = urllib.urlencode(params)
    try:
        if method=='POST':
            f = urllib2.urlopen(url, params)
        else:
            f = urllib2.urlopen(url+'?'+params)
    except:
        return (None, None)
    return (f.read(), f.code)

def TextAt0(alist):
    return alist[0].text if len(alist) > 0 else ""

provinces= [
'AG',
'AL',
'AN',
'AO',
'AP',
'AQ',
'AR',
'AT',
'AV',
'BA',
'BG',
'BI',
'BL',
'BN',
'BO',
'BR',
'BS',
'BT',
'BZ',
'CA',
'CB',
'CE',
'CH',
'CI',
'CL',
'CN',
'CO',
'CR',
'CS',
'CT',
'CZ',
'EN',
'FC',
'FE',
'FG',
'FI',
'FM',
'FR',
'GE',
'GO',
'GR',
'IM',
'IS',
'KR',
'LC',
'LE',
'LI',
'LO',
'LT',
'LU',
'MB',
'MC',
'ME',
'MI',
'MN',
'MO',
'MS',
'MT',
'NA',
'NO',
'NU',
'OG',
'OR',
'OT',
'PA',
'PC',
'PD',
'PE',
'PG',
'PI',
'PN',
'PO',
'PR',
'PT',
'PU',
'PV',
'PZ',
'RA',
'RC',
'RE',
'RG',
'RI',
'RM',
'RN',
'RO',
'SA',
'SI',
'SO',
'SP',
'SR',
'SS',
'SV',
'TA',
'TE',
'TN',
'TO',
'TP',
'TR',
'TS',
'TV',
'UD',
'VA',
'VB',
'VC',
'VE',
'VI',
'VR',
'VS',
'VT',
'VV'
]


tenders= ['ba','agg']


#set min max dates
mindate=datetime.date(2000, 1, 1)
maxdate=datetime.date.today()

numScraped=0;

for tender in tenders:
    for prov in provinces:

        #set inf=min sup=max
        infdate=copy.deepcopy(mindate)
        supdate=copy.deepcopy(maxdate)
        print "["+tender+"|"+prov+"] time range: "+infdate.strftime('%d/%m/%Y')+" <-> "+supdate.strftime('%d/%m/%Y')
        
        #ciclo su frame di tempo
        while not (infdate==supdate and supdate==maxdate): 
            #ciclo infinito finchè la pagina è di errore     
            while True:
                #prepara i dati per la richiesta POST
                data = {
                            '__VIEWSTATE':viewstate[0].value,
                             '__EVENTVALIDATION':eventval[0].value,
                             'tipoappalto':tender,
                             'regioni':'- qualsiasi -',
                             'province':prov,
                             'tipo_ente':'- qualsiasi -',
                             'tipoapp':'1',
                             'imp_fino_a':'',
                             'cat_qual':'- qualsiasi -',
                             'pubbl_dopo':infdate.strftime('%d/%m/%Y'),
                             'pubbl_prima':supdate.strftime('%d/%m/%Y')    
                        }
                #richiesta POST
                content, response = posting( urlbase+urllist, data, 'POST')
                if response:
                    #parsing lxml
                    page = lxml.html.fromstring(content)
                    if page.cssselect("span#err_source"):
                        print "["+tender+"|"+prov+"] errore: standby 10s"
                        time.sleep(10)
                    else:
                        break
                else:
                    print ">> errore posting url ... retry"
        
            #se la pagina non ha risultati => skip next timeframe
            if page.cssselect("span#no_res"):
                print "["+tender+"|"+prov+"] nessun risultato"
                #inf=sup & sup=max
                infdate=copy.deepcopy(supdate)
                supdate=copy.deepcopy(maxdate)
                print "["+tender+"|"+prov+"] no res >> new range: "+str(infdate)+" <-> "+str(supdate)
                # ritorna al while per valutare se la condizione è ancora valida
                # se inf=sup=max => si esce dal ciclo xkè è stato scansionato tutto il range temporale
                continue
    
            #numero di risultati della pagina
            numres = page.cssselect("span#num_res")
            print "["+tender+"|"+prov+"] risultati: "+TextAt0(numres)
            
            #check: ci sono troppi (>200) risultati?
            if re.search(r'visualizzati',TextAt0(numres)):
                #sup=inf+(sup-inf)/2
                #supdate=infdate+(supdate-infdate)/2
                supdate = infdate + datetime.timedelta(days=int((supdate-infdate).days/2))
                print "["+tender+"|"+prov+"] too res >> new range: "+str(infdate)+" <-> "+str(supdate)            
                # ritorna al while per valutare se nuova condizione
                continue
            
            anchors = page.cssselect("a") 
            hrefs= []
            i=0
            for a in anchors:
                if re.match("dett_"+tender+"_lav.aspx",a.attrib['href']) and \
                    not scraperwiki.sqlite.select("id from swdata where id="+str(re.search(r'\?id=(\d+)',a.attrib['href']).group(1))+" and stato_bando = '"+tender+"'"):
                    i+=1
                    hrefs.append((a,i))
    
            for a,i in hrefs:
                time.sleep(3)
                print "["+tender+"|"+prov+"](",str(i)+"/"+str(len(hrefs))+") >> "+a.attrib['href'],
                html_content = scraperwiki.scrape("https://www.serviziocontrattipubblici.it/ricerca/"+a.attrib['href'])
                html = lxml.html.fromstring(html_content)
    
                gara = dict(
                        load_date = datetime.date.today().strftime("%Y%m%d"),
                        load_time = time.strftime("%H:%M:%S",time.gmtime()),
                        id = str(re.search(r'\?id=(\d+)',a.attrib['href']).group(1)),
                        stazapp = TextAt0(html.cssselect("span#lbl_denominaz")),
                        stazapp_cfpiva= TextAt0(html.cssselect("span#lbl_cf_piva")),
                        stazapp_ufficio= TextAt0(html.cssselect("span#lbl_ufficio")),
                        tipo_settore = TextAt0(html.cssselect("span#tipo_settore")),
                        infr_strat = TextAt0(html.cssselect("span#infr_strat")),
                        tipo_bando = TextAt0(html.cssselect("span#tipo_realizz")),
                        stato_bando = tender,
                        contr_gen = TextAt0(html.cssselect("span#contr_gen")),
                        oggetto = TextAt0(html.cssselect("span#oggetto")),
                        lotti = TextAt0(html.cssselect("span#lotti")),
                        num_lotti = TextAt0(html.cssselect("span#num_lotto")),
                        cpv1 = TextAt0(html.cssselect("span#desccpv1")),
                        cpv2 = TextAt0(html.cssselect("span#desccpv2")),
                        cpv3 = TextAt0(html.cssselect("span#desccpv3")),
                        tipo_interv = TextAt0(html.cssselect("span#tipo_interv")),
                        cup = TextAt0(html.cssselect("span#cup")),
                        cig_list = TextAt0(html.cssselect("span#elenco_cig")),
                        cig_mono = TextAt0(html.cssselect("span#cig_no_lotti")),
                        luogo = TextAt0(html.cssselect("span#desc_istat")),
                        provincia = prov,
                        imp_base = TextAt0(html.cssselect("span#imp_base")),
                        sicur= TextAt0(html.cssselect("span#lbl_sicurez")),
                        imp_sicur = TextAt0(html.cssselect("span#imp_sicurez")),
                        imp_contr = TextAt0(html.cssselect("span#imp_contratt")),
                        pct_rib = TextAt0(html.cssselect("span#perc_rib_asta")),
                        proc_agg = TextAt0(html.cssselect("span#proc_agg")),
                        data_guce = TextAt0(html.cssselect("span#data_guce")),
                        data_guri = TextAt0(html.cssselect("span#data_guri")),
                        data_albo = TextAt0(html.cssselect("span#data_albo")),
                        prof_comm = TextAt0(html.cssselect("span#prof_comm")),
                        n_quot_naz = TextAt0(html.cssselect("span#n_quot_naz")),
                        n_quot_reg = TextAt0(html.cssselect("span#n_quot_reg")),
                        data_guce_agg = TextAt0(html.cssselect("span#data_guce_agg")),
                        data_scadenza = TextAt0(html.cssselect("span#data_scadenza")),
                        imp_corpo = TextAt0(html.cssselect("span#imp_corpo")),
                        imp_misura = TextAt0(html.cssselect("span#imp_misura")),
                        imp_corpo_mis = TextAt0(html.cssselect("span#imp_corpo_mis")),
                        cat_prev = TextAt0(html.cssselect("span#cat_prev")),
                        imp_cat_prev = TextAt0(html.cssselect("span#imp_cat_prev")),
                        cat_sc1 = TextAt0(html.cssselect("span#cat_scorp1")),
                        imp_cat_sc1 = TextAt0(html.cssselect("span#imp_cat_scorp1")),
                        cat_sc2 = TextAt0(html.cssselect("span#cat_scorp2")),
                        imp_cat_sc2 = TextAt0(html.cssselect("span#imp_cat_scorp2")),
                        cat_sc3 = TextAt0(html.cssselect("span#cat_scorp3")),
                        imp_cat_sc3 = TextAt0(html.cssselect("span#imp_cat_scorp3")),
                        cat_sc4 = TextAt0(html.cssselect("span#cat_scorp4")),
                        imp_cat_sc4 = TextAt0(html.cssselect("span#imp_cat_scorp4")),
                        cat_sc5 = TextAt0(html.cssselect("span#cat_scorp5")),
                        imp_cat_sc5 = TextAt0(html.cssselect("span#imp_cat_scorp5")),
                        cat_sc6 = TextAt0(html.cssselect("span#cat_scorp6")),
                        imp_cat_sc6 = TextAt0(html.cssselect("span#imp_cat_scorp6")),
                        cat_sc7 = TextAt0(html.cssselect("span#cat_scorp7")),
                        imp_cat_sc7 = TextAt0(html.cssselect("span#imp_cat_scorp7")),
                        data_agg = TextAt0(html.cssselect("span#data_agg")),
                        n_imp_rich = TextAt0(html.cssselect("span#n_imp_rich")),
                        n_imp_inv = TextAt0(html.cssselect("span#n_imp_inv")),
                        n_imp_off = TextAt0(html.cssselect("span#n_imp_off")),
                        n_imp_amm = TextAt0(html.cssselect("span#n_imp_amm")),
                        lista_agg = TextAt0(html.cssselect("span#list_az")),
                        tipo_agg = TextAt0(html.cssselect("span#tipo_agg")),
                        durata = TextAt0(html.cssselect("span#n_gg_termine")),
                        data_fine_lav = TextAt0(html.cssselect("span#data_fine_lav")),
                        note = TextAt0(html.cssselect("span#note")),
                        url_esito = TextAt0(html.cssselect("span#down_all"))
                        )
    
                print " titolo: ",gara.get('oggetto')
    
                # salvataggio dati nel db scraperwiki
                scraperwiki.sqlite.save(['id'], gara, table_name="swdata")
                numScraped+=1    
                print ">>record salvato. ("+str(numScraped)+")"

            #dopo aver acquisito le gare si sposta in avanti la finestra temporale
            infdate=copy.deepcopy(supdate)
            supdate=copy.deepcopy(maxdate)
            print "["+tender+"|"+prov+"] end scraping >> new range: "+str(infdate)+" <-> "+str(supdate)

print ">> Sessione conclusa >>Totale bandi acquisiti: "+str(numScraped)
