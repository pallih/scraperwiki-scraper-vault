import scraperwiki
import lxml.html
import unicodedata
import zipfile
import sys #used for debugging - makes the program stop
from StringIO import StringIO

#http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

#Data is from http://sigel.aneel.gov.br/kmz.html which provides KMZ files of the data used in the interface at http://sigel.aneel.gov.br/

#layers and their identifiers

#layer number counting starts with 0
powerPlantLayerNames = ["Usinas Hidrelétricas - UHE", 
                        "Pequenas Centrais Hidrelétricas - PCH", 
                        "Centrais Geradoras Hidrelétricas - CGH", 
                        "Centrais Geradoras Eolioelétricas - EOL", 
                        "Usinas Termelétricas - UTE", 
                        "Usinas Termonucleares - UTN", 
                        "Centrais Geradoras Undi-Elétricas - CGU", 
                        "Centrais Geradoras Solares Fotovoltaicas - SOL", 
                        "Produtores de Bioenergia - BIO", 
                        "Casa de Força - UHE"]

#This is the wind farm layer
#http://sigel.aneel.gov.br/ArcGIS/services/SIGEL/ExportKMZ/MapServer/KmlServer?Composite=false&LayerIDs=3&BBOX=-75,-40,30,10;CAMERA=-48.3280264999999,-30.1084437051282,3972260.50466667,0,0;VIEW=60,60,1000,1000,TRUE

for layerID in range(0,10):
    link = "http://sigel.aneel.gov.br/ArcGIS/services/SIGEL/ExportKMZ/MapServer/KmlServer?Composite=false&LayerIDs=" + str(layerID) + "&BBOX=-75,-40,30,10;CAMERA=-48.3280264999999,-30.1084437051282,3972260.50466667,0,0;VIEW=60,60,1000,1000,TRUE"

    #this link is a kmz and needs to be unzipped
    #Thank you Internet: http://stackoverflow.com/questions/5710867/python-downloading-and-unzipping-a-zip-file-without-writing-to-disk

    kmzData = scraperwiki.scrape(link)
    
    myzipfile = zipfile.ZipFile(StringIO(kmzData))
    #get the doc.kml file from the kmz
    root = lxml.html.fromstring(myzipfile.open("doc.kml").read())
    
    #get the tables containing the data shown for each of the placemarks
    #the first row and first td contains the name
    dataTables = root.xpath("//tr[1]/td[1][text()='Nome']/../..")
    
    
    for dataTable in dataTables:
        installationInfo = dict()
    
        #need to track down unique identifier
        #method 1
        uniqueID = dataTable.xpath("../../../../../@id")
        if len(uniqueID) == 0:
            #method 2
            uniqueID = dataTable.xpath("../../../../../../@id")
        
        if len(uniqueID) == 0:
            sys.exit(1) #Stop the scraper - not able to find a unique ID, code will need update
        else: 
            uniqueID = uniqueID[0]
            installationInfo['uniqueID'] = uniqueID
            installationInfo['powerPlantType'] = powerPlantLayerNames[layerID]
            print uniqueID

        #get the set of rows
        rows = dataTable.xpath("./tr")
    
        for row in rows:
            key = row.xpath("./td[1]/text()")[0]
            value = row.xpath("./td[2]/text()")[0]
            
            #key = unicodedata.normalize('NFD', key.decode('utf-8')).encode('ascii', 'ignore')
            key = strip_accents(unicode(key)).encode('ascii', 'ignore').replace(')', '').replace('(','').replace('.', '')
            installationInfo[key] = value
    
        scraperwiki.sqlite.save(unique_keys=['uniqueID'], data=installationInfo)

