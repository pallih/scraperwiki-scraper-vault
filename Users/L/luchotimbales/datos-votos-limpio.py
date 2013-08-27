# ---------------------------------------------------------------------------
#  
# 
# ---------------------------------------------------------------------------

import scraperwiki,re, urllib2
from BeautifulSoup import BeautifulSoup
#scraperwiki.cache(True)

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key', 'Municipio', 'NombreMun', 'Provincia','NombreProv' 'Year', 'Partido','PartidoLargo', 'Votos', 'Escanos'])

#Read elements from the list 
def read_elements (singleMun0):
    getList =  re.findall("[^,]+", singleMun0)
    MunNum = getList[2]
    MunName = getList[3][1:-1].replace('"','')
    ProvNum = getList[0]
    ProvName = getList[1][1:-1]
    get_html(MunNum,MunName,ProvNum,ProvName)
    

#URL to get data from
def get_html(MunNum,MunName,ProvNum,ProvName):
    url='http://www.elecciones.mir.es/MIR/jsp/resultados/comunes/detalleResultado.jsp?tipoAmbito=0&cdMunicipio='+MunNum+'&dsMunicipio=Municipio%3A+ALEGRIA-DULANTZI&distritoMunicipal=99&cdProvincia='+ProvNum+'&dsProvincia=ALAVA&descripcion=Municipio%3A+ALEGRIA-DULANTZI%20%28ALAVA%29&cdEleccion=4&anio=2003&tipoEleccion=2&mes=5&numVuelta=1&nombreEleccion=Municipales&horaCierre=null&horaAvance1=null&horaAvance2=null'

    #gets the html from website and handles errors
    try:
        html = scraperwiki.scrape(url)
    except:
        print 'no hay datos', url
    else:
        #here we prepare the html so that we can then grab the tables we need and so that we have the same number of td´s
        html=html.replace('<table width="99%">','<table width="99%" class="datos">')
        html=html.replace('<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>','<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td><td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>')
        soup = BeautifulSoup(html)
        scrape_table(soup,MunNum,ProvNum,MunName,ProvName)

# scrape_table function: gets passed an individual page to scrape into the table
def scrape_table(soup, mun, prov, MunName, ProvName):
    data_table = soup.find("table", { "class" : "datos" })
    #print data_table
    rows = data_table.findAll("tr")
    #print rows
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("font")
        if table_cells and table_cells[4].text<>"Concejales": 
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
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Key"], record)


# Read file with the municipios and provincias codes and names into a list 
website='http://aa.1asphost.com/luchotimbales/municipios.txt'
response = urllib2.urlopen(website)
singleMun= response.readlines()
n = len(singleMun)
print "total muns", n
for i, singleMun0 in enumerate(singleMun):
    if (i % 10) == 0:
        print "At counter", i
    read_elements (singleMun0)

# ---------------------------------------------------------------------------
#  
# 
# ---------------------------------------------------------------------------

import scraperwiki,re, urllib2
from BeautifulSoup import BeautifulSoup
#scraperwiki.cache(True)

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key', 'Municipio', 'NombreMun', 'Provincia','NombreProv' 'Year', 'Partido','PartidoLargo', 'Votos', 'Escanos'])

#Read elements from the list 
def read_elements (singleMun0):
    getList =  re.findall("[^,]+", singleMun0)
    MunNum = getList[2]
    MunName = getList[3][1:-1].replace('"','')
    ProvNum = getList[0]
    ProvName = getList[1][1:-1]
    get_html(MunNum,MunName,ProvNum,ProvName)
    

#URL to get data from
def get_html(MunNum,MunName,ProvNum,ProvName):
    url='http://www.elecciones.mir.es/MIR/jsp/resultados/comunes/detalleResultado.jsp?tipoAmbito=0&cdMunicipio='+MunNum+'&dsMunicipio=Municipio%3A+ALEGRIA-DULANTZI&distritoMunicipal=99&cdProvincia='+ProvNum+'&dsProvincia=ALAVA&descripcion=Municipio%3A+ALEGRIA-DULANTZI%20%28ALAVA%29&cdEleccion=4&anio=2003&tipoEleccion=2&mes=5&numVuelta=1&nombreEleccion=Municipales&horaCierre=null&horaAvance1=null&horaAvance2=null'

    #gets the html from website and handles errors
    try:
        html = scraperwiki.scrape(url)
    except:
        print 'no hay datos', url
    else:
        #here we prepare the html so that we can then grab the tables we need and so that we have the same number of td´s
        html=html.replace('<table width="99%">','<table width="99%" class="datos">')
        html=html.replace('<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>','<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td><td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>')
        soup = BeautifulSoup(html)
        scrape_table(soup,MunNum,ProvNum,MunName,ProvName)

# scrape_table function: gets passed an individual page to scrape into the table
def scrape_table(soup, mun, prov, MunName, ProvName):
    data_table = soup.find("table", { "class" : "datos" })
    #print data_table
    rows = data_table.findAll("tr")
    #print rows
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("font")
        if table_cells and table_cells[4].text<>"Concejales": 
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
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Key"], record)


# Read file with the municipios and provincias codes and names into a list 
website='http://aa.1asphost.com/luchotimbales/municipios.txt'
response = urllib2.urlopen(website)
singleMun= response.readlines()
n = len(singleMun)
print "total muns", n
for i, singleMun0 in enumerate(singleMun):
    if (i % 10) == 0:
        print "At counter", i
    read_elements (singleMun0)

# ---------------------------------------------------------------------------
#  
# 
# ---------------------------------------------------------------------------

import scraperwiki,re, urllib2
from BeautifulSoup import BeautifulSoup
#scraperwiki.cache(True)

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key', 'Municipio', 'NombreMun', 'Provincia','NombreProv' 'Year', 'Partido','PartidoLargo', 'Votos', 'Escanos'])

#Read elements from the list 
def read_elements (singleMun0):
    getList =  re.findall("[^,]+", singleMun0)
    MunNum = getList[2]
    MunName = getList[3][1:-1].replace('"','')
    ProvNum = getList[0]
    ProvName = getList[1][1:-1]
    get_html(MunNum,MunName,ProvNum,ProvName)
    

#URL to get data from
def get_html(MunNum,MunName,ProvNum,ProvName):
    url='http://www.elecciones.mir.es/MIR/jsp/resultados/comunes/detalleResultado.jsp?tipoAmbito=0&cdMunicipio='+MunNum+'&dsMunicipio=Municipio%3A+ALEGRIA-DULANTZI&distritoMunicipal=99&cdProvincia='+ProvNum+'&dsProvincia=ALAVA&descripcion=Municipio%3A+ALEGRIA-DULANTZI%20%28ALAVA%29&cdEleccion=4&anio=2003&tipoEleccion=2&mes=5&numVuelta=1&nombreEleccion=Municipales&horaCierre=null&horaAvance1=null&horaAvance2=null'

    #gets the html from website and handles errors
    try:
        html = scraperwiki.scrape(url)
    except:
        print 'no hay datos', url
    else:
        #here we prepare the html so that we can then grab the tables we need and so that we have the same number of td´s
        html=html.replace('<table width="99%">','<table width="99%" class="datos">')
        html=html.replace('<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>','<td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td><td align="center"><font class="FuenteTituloTablaCandidaturas">Concejales</font></td>')
        soup = BeautifulSoup(html)
        scrape_table(soup,MunNum,ProvNum,MunName,ProvName)

# scrape_table function: gets passed an individual page to scrape into the table
def scrape_table(soup, mun, prov, MunName, ProvName):
    data_table = soup.find("table", { "class" : "datos" })
    #print data_table
    rows = data_table.findAll("tr")
    #print rows
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.findAll("font")
        if table_cells and table_cells[4].text<>"Concejales": 
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
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.datastore.save(["Key"], record)


# Read file with the municipios and provincias codes and names into a list 
website='http://aa.1asphost.com/luchotimbales/municipios.txt'
response = urllib2.urlopen(website)
singleMun= response.readlines()
n = len(singleMun)
print "total muns", n
for i, singleMun0 in enumerate(singleMun):
    if (i % 10) == 0:
        print "At counter", i
    read_elements (singleMun0)

