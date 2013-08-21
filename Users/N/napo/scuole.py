import scraperwiki
params={"desAnnoAccademico":"undefined","desCodiceMeccanografico":"undefined","desComune":"ALTINO","desDenominazione":"undefined","desIndirizzo":"undefined","desIndirizzoRiferimento":"undefined","desOrdineScuola":"SCUOLA DELL'INFANZIA","desParitaria":"undefined","desProvincia":"CHIETI","desRaggio":"undefined","desRegione":"ABRUZZO","desTipoScuola":"STATALE E PARITARIA","desTipologia":"undefined","finestra":"criteriRicerca"}
html = scraperwiki.scrape("http://cercalatuascuola.istruzione.it/cercalatuascuola/ricercaAvanzata/start.do",params) 
html = scraperwiki.scrape("http://cercalatuascuola.istruzione.it/cercalatuascuola/jsp/common/criteriRicerca.jsp?desRegione=BASILICATA&desProvincia=MATERA&desComune=ACCETTURA&desTipoScuola=STATALE%20E%20PARITARIA&desParitaria=undefined&desAnnoAccademico=undefined&desOrdineScuola=SCUOLA%20DELL%27INFANZIA&desTipologia=undefined&desIndirizzo=undefined&desDenominazione=undefined&desCodiceMeccanografico=undefined&desIndirizzoRiferimento=undefined&desRaggio=undefined&finestra=criteriRicerca")
html = scraperwiki.scrape("http://cercalatuascuola.istruzione.it/cercalatuascuola/common/CreaJson/load.do",params)
print html

