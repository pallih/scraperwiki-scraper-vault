import scraperwiki
import csv
import tempfile
import zipfile
import urllib
import os
import datetime
import dateutil.parser 
from sys import exit


def extractPegel(pegelnummer, date1, date2):

    
    url  = 'http://www.pegelonline.wsv.de/webservices/zeitreihe/text'
    url += '?zeitpunktVon='+date1+'T00:00:00.000'
    url += '&zeitpunktBis='+date2+'T23:59:59.999'
    url += '&pegelnummer='+pegelnummer

    print 'Lese Pegel "'+pegelnummer+'" von "'+url+'"'
    
    try:
        t = tempfile.NamedTemporaryFile(suffix=".zip")
        t.write(urllib.urlopen(url).read())
        t.seek(0)
        
        z = zipfile.ZipFile(t.name)
        
        contents = z.namelist()
        
        z.extract('download.txt')
        
        data = open(os.getcwd() + '/download.txt', 'r').read()
        
        lines = data.splitlines()
        
        headerPosition = 1
        date = ''
        
        for line in lines:
            if line == '':
                headerPosition = 0
            
            if headerPosition == 1:
                date = line
            
            if headerPosition >= 13:
                felder = line.split('#')
                zeit = felder[0]
                pegel = felder[1]
                minuten = zeit[-2:]
                if (minuten == '00' or minuten == '30') and (pegel[-1:] != 'X') :
                    scraperwiki.sqlite.save(
                        unique_keys=['Zeit', 'Pegelnummer'],
                        data={'Zeit':date+' '+zeit, 'Pegelnummer':pegelnummer, 'Pegelstand':pegel },
                        table_name="pegel"
                    )
            
            headerPosition = headerPosition + 1

    except Exception as e:
        print 'FEHLER: '+str(e)





today = datetime.date.today()

date2 = (today - datetime.timedelta(1)).isoformat()
date1 = (today - datetime.timedelta(5)).isoformat()

print date1
print date2

print 'Lese "pegelinfo"'

pegelinfo = scraperwiki.scrape("http://www.pegelonline.wsv.de/internal/karte/openlayers/pegelinfo")
pegelinfo = csv.reader(pegelinfo.splitlines(), delimiter="\t")
pegelnummern = []


for zeile in pegelinfo:
    if zeile[5] != 'pegelNummer':
        pegelnummern.append(zeile[5])
        daten = {
            'lat':zeile[0],
            'lon':zeile[1],
            'pegelNummer':zeile[5],
            'gewaesserName':zeile[6],
            'pegelName':zeile[8],
            'datum':today.isoformat()
        }
        scraperwiki.sqlite.save(
            unique_keys=['pegelNummer', 'lat', 'lon'],
            data=daten, table_name="stationen", verbose=2)


for pegelnummer in pegelnummern:
    extractPegel(pegelnummer, date1, date2)

import scraperwiki
import csv
import tempfile
import zipfile
import urllib
import os
import datetime
import dateutil.parser 
from sys import exit


def extractPegel(pegelnummer, date1, date2):

    
    url  = 'http://www.pegelonline.wsv.de/webservices/zeitreihe/text'
    url += '?zeitpunktVon='+date1+'T00:00:00.000'
    url += '&zeitpunktBis='+date2+'T23:59:59.999'
    url += '&pegelnummer='+pegelnummer

    print 'Lese Pegel "'+pegelnummer+'" von "'+url+'"'
    
    try:
        t = tempfile.NamedTemporaryFile(suffix=".zip")
        t.write(urllib.urlopen(url).read())
        t.seek(0)
        
        z = zipfile.ZipFile(t.name)
        
        contents = z.namelist()
        
        z.extract('download.txt')
        
        data = open(os.getcwd() + '/download.txt', 'r').read()
        
        lines = data.splitlines()
        
        headerPosition = 1
        date = ''
        
        for line in lines:
            if line == '':
                headerPosition = 0
            
            if headerPosition == 1:
                date = line
            
            if headerPosition >= 13:
                felder = line.split('#')
                zeit = felder[0]
                pegel = felder[1]
                minuten = zeit[-2:]
                if (minuten == '00' or minuten == '30') and (pegel[-1:] != 'X') :
                    scraperwiki.sqlite.save(
                        unique_keys=['Zeit', 'Pegelnummer'],
                        data={'Zeit':date+' '+zeit, 'Pegelnummer':pegelnummer, 'Pegelstand':pegel },
                        table_name="pegel"
                    )
            
            headerPosition = headerPosition + 1

    except Exception as e:
        print 'FEHLER: '+str(e)





today = datetime.date.today()

date2 = (today - datetime.timedelta(1)).isoformat()
date1 = (today - datetime.timedelta(5)).isoformat()

print date1
print date2

print 'Lese "pegelinfo"'

pegelinfo = scraperwiki.scrape("http://www.pegelonline.wsv.de/internal/karte/openlayers/pegelinfo")
pegelinfo = csv.reader(pegelinfo.splitlines(), delimiter="\t")
pegelnummern = []


for zeile in pegelinfo:
    if zeile[5] != 'pegelNummer':
        pegelnummern.append(zeile[5])
        daten = {
            'lat':zeile[0],
            'lon':zeile[1],
            'pegelNummer':zeile[5],
            'gewaesserName':zeile[6],
            'pegelName':zeile[8],
            'datum':today.isoformat()
        }
        scraperwiki.sqlite.save(
            unique_keys=['pegelNummer', 'lat', 'lon'],
            data=daten, table_name="stationen", verbose=2)


for pegelnummer in pegelnummern:
    extractPegel(pegelnummer, date1, date2)

