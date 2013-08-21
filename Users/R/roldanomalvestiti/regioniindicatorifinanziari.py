import scraperwiki
import mechanize
import lxml.html           


def scrapeSinglePage(page, codiceEnte, anno): 
    "scarica indicatori del regione"
    htmlPage = scraperwiki.scrape(page)
    print htmlPage 
    rootTot = lxml.html.fromstring(htmlPage)
    #estrai nome ente
    tds = rootTot.cssselect("td.asinistra")
    for td in tds:
        spans = td.cssselect("span")
        if len(spans)==1:
            print(spans[0].text_content())
            nomeEnte = spans[0].text_content()

    #spans = rootTot.cssselect("span.titoliblu")
    #nomeEnte = spans[3].text_content()

    #estrai indicatori
    tables = rootTot.cssselect("table.tabfin")
    for table in tables:
        rows = table.cssselect("tr")
        
        #initiatialize data with region name
        data = {'nomeEnte':codiceEnte};
        for row in rows:
            
            ths = row.cssselect("th")
            tds = row.cssselect("td")
            if len(tds)==5:
                #print(tds[0].text_content())
                if len(tds[0].text_content())>2:
                    valoreStr = tds[4].text_content().strip()
                    valoreStr = valoreStr .replace(",",".")
                    data['indicatore']= ths[0].text_content().strip()
                    data['valoreEnte']= float(valoreStr)
                    data['anno']= int (anno)
                    print data
                    scraperwiki.sqlite.save(unique_keys=['nomeEnte','indicatore', 'anno' ], data=data)
    return;
            

arrayCodici = {
"ABRUZZO","BASILICATA","CALABRIA","CAMPANIA","EMILIA ROMAGNA","LAZIO",
"LIGURIA","LOMBARDIA","MARCHE","MOLISE","PIEMONTE","PUGLIA","SARDEGNA",
"SICILIA","UMBRIA","VENETO"
}
#"FRIULI-VENEZIA GIULIA", "TRENTINO-ALTO ADIGE", "VALLE D''AOSTA"  // non funzionano neanche su sito istituzionale


#http://finanzalocale.interno.it/apps/floc.php/indicatori/index/anno/2008/cod/8/md/0/tipo_certificato/C/tipo_ente/AP/stratificazione/R/reg/ABRUZZO
baseUrl ="http://finanzalocale.interno.it/apps/floc.php/indicatori/index"
anni = {"2004","2005","2006","2007","2008","2009"}
tipoEnte= "AP/stratificazione/R/reg"

#parse html singola pagina di indicatori
for codice in arrayCodici:
    for anno in anni:
        urlIFComune = baseUrl + "/anno/" + anno + "/cod/8/md/0/tipo_certificato/C/tipo_ente/" + tipoEnte + "/" + codice
        scrapeSinglePage(urlIFComune, codice, anno)




