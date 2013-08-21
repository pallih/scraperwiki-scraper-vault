import scraperwiki
import lxml.html
import unicodedata
import zipfile
from StringIO import StringIO
import csv 

pegellisteUrl="http://www.pegelonline.wsv.de//internal/karte/openlayers/pegelinfo"
pegelliste=scraperwiki.scrape(pegellisteUrl)
print pegelliste
pg=0

pegelDaten = csv.reader(pegelliste.splitlines(),"excel-tab")
for pegel in pegelDaten:
    pegelnummer = pegel[5]
    if pegelnummer != "pegelNummer":
        print pg
        print pegelnummer
        pg = pg+1
        
   

        link="https://www.pegelonline.wsv.de/webservices/zeitreihe/text?zeitpunktVon=2012-11-10T00:00:00.000&zeitpunktBis=2012-11-13T23:59:59.999&pegelnummer="+pegelnummer
        
        kmzData = scraperwiki.scrape(link)
            
        myzipfile = zipfile.ZipFile(StringIO(kmzData))
        zeilen = myzipfile.open("download.txt").read().splitlines()
        
        aktuelleUhrzeit=""
        
        blockzeile=1
        
        for zeile in zeilen:
        
            if zeile =='': # Leere Zeile, neuer Block beginnt
                blockzeile = 0
                aktuelleUhrzeit=""
        
            if blockzeile == 1: # Der erste Wert
                datum=zeile
            
            if blockzeile == 3:
                fluss = zeile

            if blockzeile == 4:
                pegelname = zeile
        
            if blockzeile >= 13:
                
                data=zeile.split("#")
                stunde=data[0].split(":")[0]
                if stunde != aktuelleUhrzeit and len(stunde) == 2:
                    print stunde + " / " + data[0]
                    aktuelleUhrzeit= stunde   
                    pegeldata= {
                            'pegelnummer': pegelnummer,
                            "datum": datum,
                            "zeit": data[0],
                            "pegel": data[1],
                            "pegelname": pegelname.encode("utf-8"),
                            "fluss": fluss.encode("utf-8"),    
                            "id": pegelnummer+datum+data[0]
                    }
                    scraperwiki.sqlite.save(unique_keys=['id'], data=pegeldata)
                    #print pegelnummer+" "+datum+" "+data[0]
        
            blockzeile = blockzeile +1

# Blank Python

