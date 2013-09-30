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

    spans = rootTot.cssselect("span.titoliblu")
    if (len(spans)>=2):
        nomeEnte = spans[1].text_content()

        #estrai indicatori
        tables = rootTot.cssselect("table.tabfin")
        for table in tables:
            rows = table.cssselect("tr")
            
            #initiatialize data with region name
            data = {'nomeEnte':nomeEnte};
            data['codiceEnte']= codice
            for row in rows:
                
                #ths = row.cssselect("th")
                tds = row.cssselect("td")
                if len(tds)==6:
                    #print(tds[0].text_content())
                    if len(tds[0].text_content())>2:
                        valoreStr = tds[1].text_content().strip()
                        valoreStr = valoreStr .replace(",",".")
                        data['indicatore']= tds[0].text_content().strip()
                        data['valoreEnte']= float(valoreStr)
                        data['anno']= int (anno)
                        print data
                        scraperwiki.sqlite.save(unique_keys=['codiceEnte','indicatore', 'anno' ], data=data)
    return;
            

arrayCodici = {
"1010020000","1010070000","1010270000","1010520000","1010810000","1010880000","1010960000","1011020000","1020040000","1030120000","1030150000","1030240000",
"1030260000","1030450000","1030490000","1030570000","1030770000","1030860000","1030980000","1030990000","1031040000","1070340000","1070370000","1070390000",
"1070740000","2040140000","2040830000","2050100000","2050540000","2050710000","2050840000","2050870000","2050890000","2050900000","2060350000","2060850000",
"2060920000","2060930000","2080130000","2080290000","2080320000","2080500000","2080560000","2080610000","2080660000","2080680000","2081010000","3090050000",
"3090300000","3090360000","3090420000","3090430000","3090460000","3090620000","3090630000","3090750000","3091000000","3100580000","3100800000","3110030000",
"3110060000","3110440000","3110590000","3111050000","3120330000","3120400000","3120690000","3120700000","3120910000","4130230000","4130380000","4130600000",
"4130790000","4140190000","4140940000","4150080000","4150110000","4150200000","4150510000","4150720000","4160090000","4160160000","4160310000","4160410000",
"4160780000","4161060000","4170470000","4170640000","4180220000","4180250000","4180670000","4180970000","4181030000","5190010000","5190180000","5190210000",
"5190280000","5190480000","5190550000","5190650000","5190760000","5190820000","5200170000","5200530000","5200730000","5200950000","5201070000","5201080000",
"5201090000","5201100000"
}



#http://finanzalocale.interno.it/apps/floc.php/indicatori/index/codice_ente/5190010000/anno/2008/cod/8/md/0/tipo_certificato/C/tipo_ente/AP
baseUrl ="http://finanzalocale.interno.it/apps/floc.php/indicatori/index"
anni = {"2004","2005","2006","2007","2008","2009"}
tipoEnte= "AP"

#parse html singola pagina di indicatori
for codice in arrayCodici:
    for anno in anni:
        urlIFComune = baseUrl + "/codice_ente/" + codice + "/anno/" + anno + "/cod/8/md/0/tipo_certificato/C/tipo_ente/" + tipoEnte 
        scrapeSinglePage(urlIFComune, codice, anno)



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

    spans = rootTot.cssselect("span.titoliblu")
    if (len(spans)>=2):
        nomeEnte = spans[1].text_content()

        #estrai indicatori
        tables = rootTot.cssselect("table.tabfin")
        for table in tables:
            rows = table.cssselect("tr")
            
            #initiatialize data with region name
            data = {'nomeEnte':nomeEnte};
            data['codiceEnte']= codice
            for row in rows:
                
                #ths = row.cssselect("th")
                tds = row.cssselect("td")
                if len(tds)==6:
                    #print(tds[0].text_content())
                    if len(tds[0].text_content())>2:
                        valoreStr = tds[1].text_content().strip()
                        valoreStr = valoreStr .replace(",",".")
                        data['indicatore']= tds[0].text_content().strip()
                        data['valoreEnte']= float(valoreStr)
                        data['anno']= int (anno)
                        print data
                        scraperwiki.sqlite.save(unique_keys=['codiceEnte','indicatore', 'anno' ], data=data)
    return;
            

arrayCodici = {
"1010020000","1010070000","1010270000","1010520000","1010810000","1010880000","1010960000","1011020000","1020040000","1030120000","1030150000","1030240000",
"1030260000","1030450000","1030490000","1030570000","1030770000","1030860000","1030980000","1030990000","1031040000","1070340000","1070370000","1070390000",
"1070740000","2040140000","2040830000","2050100000","2050540000","2050710000","2050840000","2050870000","2050890000","2050900000","2060350000","2060850000",
"2060920000","2060930000","2080130000","2080290000","2080320000","2080500000","2080560000","2080610000","2080660000","2080680000","2081010000","3090050000",
"3090300000","3090360000","3090420000","3090430000","3090460000","3090620000","3090630000","3090750000","3091000000","3100580000","3100800000","3110030000",
"3110060000","3110440000","3110590000","3111050000","3120330000","3120400000","3120690000","3120700000","3120910000","4130230000","4130380000","4130600000",
"4130790000","4140190000","4140940000","4150080000","4150110000","4150200000","4150510000","4150720000","4160090000","4160160000","4160310000","4160410000",
"4160780000","4161060000","4170470000","4170640000","4180220000","4180250000","4180670000","4180970000","4181030000","5190010000","5190180000","5190210000",
"5190280000","5190480000","5190550000","5190650000","5190760000","5190820000","5200170000","5200530000","5200730000","5200950000","5201070000","5201080000",
"5201090000","5201100000"
}



#http://finanzalocale.interno.it/apps/floc.php/indicatori/index/codice_ente/5190010000/anno/2008/cod/8/md/0/tipo_certificato/C/tipo_ente/AP
baseUrl ="http://finanzalocale.interno.it/apps/floc.php/indicatori/index"
anni = {"2004","2005","2006","2007","2008","2009"}
tipoEnte= "AP"

#parse html singola pagina di indicatori
for codice in arrayCodici:
    for anno in anni:
        urlIFComune = baseUrl + "/codice_ente/" + codice + "/anno/" + anno + "/cod/8/md/0/tipo_certificato/C/tipo_ente/" + tipoEnte 
        scrapeSinglePage(urlIFComune, codice, anno)



