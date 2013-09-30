#############################################################################
# Test scraper to extract the current respirable dust concentration in Berlin 
#############################################################################
import urllib
import scraperwiki
# up to date source file 
url = "http://www.met.fu-berlin.de/senum/messwerte/aktuell.txt"
f = urllib.urlopen(url)
lines = f.readlines()

#status searching: line containing 'Feinstaub' not yet found
#status extracting1: line containing 'Feinstaub' found and extracting first value
#status extracting2: line containing 'Feinstaub' found and extracting second value
#status finishing: ignoring the remaining lines
status = "searching" 

#cache for respirable dust concentration values  
value1 = 0 
value2 = 0 

for line in lines:
    if  status == "searching":
        output= line.find("Feinstaub")
        if output == 0: #line with "Feinstaub" found
            print line
            status="extracting1"

    elif status == "extracting1":
        print line[3:5]# extracting first value
        value1 = line[3:5]
        status="extracting2"

    elif status == "extracting2":
        print line[3:5]# extracting second value
        value2 = line[3:5]
        status="finishing"


#scraperwiki.datastore. --> alte speichermethode

scraperwiki.sqlite.save(unique_keys=["Berlin Feinstaub PM10"], data={"Berlin Feinstaub PM10": "Sensor (Partikelgröße < 10 µm)",'Verkehrsmessstelle_Silbersteinstr':value1, 'innerstaedtischen_Wohngebietsmessstelle_Amrumer_Str':value2}) #storing values to scraperwiki 



#############################################################################
# Test scraper to extract the current respirable dust concentration in Berlin 
#############################################################################
import urllib
import scraperwiki
# up to date source file 
url = "http://www.met.fu-berlin.de/senum/messwerte/aktuell.txt"
f = urllib.urlopen(url)
lines = f.readlines()

#status searching: line containing 'Feinstaub' not yet found
#status extracting1: line containing 'Feinstaub' found and extracting first value
#status extracting2: line containing 'Feinstaub' found and extracting second value
#status finishing: ignoring the remaining lines
status = "searching" 

#cache for respirable dust concentration values  
value1 = 0 
value2 = 0 

for line in lines:
    if  status == "searching":
        output= line.find("Feinstaub")
        if output == 0: #line with "Feinstaub" found
            print line
            status="extracting1"

    elif status == "extracting1":
        print line[3:5]# extracting first value
        value1 = line[3:5]
        status="extracting2"

    elif status == "extracting2":
        print line[3:5]# extracting second value
        value2 = line[3:5]
        status="finishing"


#scraperwiki.datastore. --> alte speichermethode

scraperwiki.sqlite.save(unique_keys=["Berlin Feinstaub PM10"], data={"Berlin Feinstaub PM10": "Sensor (Partikelgröße < 10 µm)",'Verkehrsmessstelle_Silbersteinstr':value1, 'innerstaedtischen_Wohngebietsmessstelle_Amrumer_Str':value2}) #storing values to scraperwiki 



