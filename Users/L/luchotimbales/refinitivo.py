###############################################################################
# This scripts gets data from about spanish electoral results 
###############################################################################

import scraperwiki,re, urllib2
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key', 'Municipio', 'NombreMun', 'Provincia','NombreProv' 'Year', 'Partido','PartidoLargo', 'Votos', 'Escanos'])

# scrape_table function: gets passed an individual page to scrape
def scrape_table(soup, mun, prov, MunName, ProvName):
    data_table = soup.find("table", { "class" : "datos" })
    #print data_table
    rows = data_table.findAll("tr")
    #print rows
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("font")
        if table_cells: 
            record['Key'] = 'mun_'+mun+'prov_'+prov+'2003'+table_cells[0].text
            record['Municipio'] = mun
            record['NombreMun'] = MunName
            record['NombreProv'] = ProvName
            record['Provincia'] = prov
            record['Year'] = '2003'
            record['Partido'] = table_cells[0].text
            record['PartidoLargo'] = table_cells[1].text
            record['Votos'] = table_cells[2].text
            record['Escanos'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Key"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url,i,singleMun):
    print i
    getList =  re.findall("[^,]+", singleMun[i])
    MunNum = getList[2]
    MunName = getList[3][1:-1]
    ProvNum = getList[0]
    ProvName = getList[1][1:-1]
    try:
        html = scraperwiki.scrape(url)
    except:
        print 'no hay datos'
        getList =  re.findall("[^,]+", singleMun[i+1])
        MunNum = getList[2]
        MunName = getList[3][1:-1]
        ProvNum = getList[0]
        ProvName = getList[1][1:-1]
        next_url='http://www.elecciones.mir.es/MIR/jsp/resultados/comunes/detalleResultado.jsp?tipoAmbito=0&cdMunicipio='+MunNum+'&dsMunicipio=Municipio%3A+ALEGRIA-DULANTZI&distritoMunicipal=99&cdProvincia='+ProvNum+'&dsProvincia=ALAVA&descripcion=Municipio%3A+ALEGRIA-DULANTZI%20%28ALAVA%29&cdEleccion=4&anio=2003&tipoEleccion=2&mes=5&numVuelta=1&nombreEleccion=Municipales&horaCierre=null&horaAvance1=null&horaAvance2=null'
        scrape_and_look_for_next_link(next_url, i+1,singleMun)
    else:
        #here we prepare the html so that we can then grab the tables we need and so that we have the same number of td´s
        html=html.replace('<table width="99%">','<table width="99%" class="datos">')
        html=html.replace('<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>','<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td><td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>')
        soup = BeautifulSoup(html)
        scrape_table(soup,MunNum,ProvNum,MunName,ProvName)
        next_url='http://www.elecciones.mir.es/MIR/jsp/resultados/comunes/detalleResultado.jsp?tipoAmbito=0&cdMunicipio='+MunNum+'&dsMunicipio=Municipio%3A+ALEGRIA-DULANTZI&distritoMunicipal=99&cdProvincia='+ProvNum+'&dsProvincia=ALAVA&descripcion=Municipio%3A+ALEGRIA-DULANTZI%20%28ALAVA%29&cdEleccion=4&anio=2003&tipoEleccion=2&mes=5&numVuelta=1&nombreEleccion=Municipales&horaCierre=null&horaAvance1=null&horaAvance2=null'
        print next_url
        scrape_and_look_for_next_link(next_url, i+1,singleMun)
# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
# File with the information about municipios from INE
website='http://aa.1asphost.com/luchotimbales/municipios.txt'
req = urllib2.Request(website)
response = urllib2.urlopen(req)
input = urllib2.urlopen(req)
singleMun= input.readlines()
n = len(singleMun)
#URL to start with
base_url = 'http://www.elecciones.mir.es/MIR/jsp/resultados/comunes/detalleResultado.jsp?tipoAmbito=0&cdMunicipio=2&dsMunicipio=Municipio%3A+ALEGRIA-DULANTZI&distritoMunicipal=99&cdProvincia=2&dsProvincia=ALAVA&descripcion=Municipio%3A+ALEGRIA-DULANTZI%20%28ALAVA%29&cdEleccion=4&anio=2003&tipoEleccion=2&mes=5&numVuelta=1&nombreEleccion=Municipales&horaCierre=null&horaAvance1=null&horaAvance2=null'
starting_url = base_url 
scrape_and_look_for_next_link(starting_url,0,singleMun)
