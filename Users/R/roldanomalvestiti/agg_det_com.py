import scraperwiki

#Venezia
scraperwiki.sqlite.attach("comunevenezia_determinazioni2012", "src")           
#print scraperwiki.sqlite.table_info("src.swdata")
venItems = scraperwiki.sqlite.select("* from src.swdata where anno >= 2012")
for delibera in venItems: 
    #print delibera

    data = {
           'codiceIstat' : 27042,
           'comune' : 'Venezia',
           'num' : delibera['num'],
           'codice' : delibera['codice'],
            'categoria': "",
           'importo' : delibera['importo'] ,
           'anno' : delibera['anno'],
           'descrizione' : delibera['descrizione'],
           'DataSalvataggio' : delibera['DataSalvataggio'],
           'DataUltimoUpdate' : delibera['DataUltimoUpdate'],
           'url' : delibera['url']
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['codice'], data=data)

#Torino
#1272
scraperwiki.sqlite.attach("torinodeterminazioni", "srcTo")           
#print scraperwiki.sqlite.table_info("srcTo.swdata")
venItems = scraperwiki.sqlite.select("* from srcTo.swdata where anno >= 2012")
for delibera in venItems: 
    #print delibera

    data = {
           'codiceIstat' : 1272,
           'comune' : 'Torino',
           'num' : delibera['num'],
           'codice' : delibera['codice'],
           'categoria': "",
           'importo' : delibera['importo'] ,
           'anno' : delibera['anno'],
           'descrizione' : delibera['descrizione'],
           'DataSalvataggio' : delibera['DataSalvataggio'],
           'DataUltimoUpdate' : delibera['DataUltimoUpdate'],
           'url' : delibera['url']
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['codice'], data=data)

#Milano
#15146
scraperwiki.sqlite.attach("comunemilano_determinazioni2012", "srcMi")           
#print scraperwiki.sqlite.table_info("srcMi.swdata")
venItems = scraperwiki.sqlite.select("* from srcMi.swdata where anno >= 2012")
for delibera in venItems: 
    #print delibera

    data = {
           'codiceIstat' : 15146,
           'comune' : 'Milano',
           'num' : delibera['num'],
           'codice' : delibera['codice'],
           'categoria': "",
           'importo' : delibera['importo'] ,
           'anno' : delibera['anno'],
           'descrizione' : delibera['descrizione'],
           'DataSalvataggio' : delibera['DataSalvataggio'],
           'DataUltimoUpdate' : delibera['DataUltimoUpdate'],
           'url' : delibera['url']
    }
    #print data
    scraperwiki.sqlite.save(unique_keys=['codice'], data=data)


         

