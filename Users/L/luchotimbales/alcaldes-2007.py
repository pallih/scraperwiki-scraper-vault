###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key','Provincia', 'Municipio', 'ALCALDE','LISTA ELECTORAL','FECHA DE POSESION'])
column=['Key','Provincia','Municipio', 'ALCALDE','LISTA ELECTORAL','FECHA DE POSESION']
provincia=1
counter=0

for provincia in range(1,53):
    startURL="http://cooplocal.mpt.es/cgi-bin/webapb/webdriver?MItabObj=elec_prov_pdf&MInamObj=prov&MIcolObj=documento&MItypeObj=application/pdf&MIvalObj="
    pdfurl = startURL + str(provincia)
    a = scraperwiki.scrape(pdfurl)
    s = BeautifulSoup(scraperwiki.pdftoxml(a))
    data = {}
    columna=0

    for t in s.findAll('text'):
        linea=t.text
        if "Versi" in linea:
             linea=" "
        if "Alcaldes" in linea:
             linea=" "
        if "ELECCIONES" in linea:
             linea=" "
        if "ALCALDE" in linea:
             linea=" "
        if "LISTA ELECTORAL" in linea:
             linea=" "
        if "FECHA DE" in linea:
             linea=" "
        if "MUNICIPIO" in linea:
             linea=" "
        if "LISTAS ELECTORALES" in linea:
             break
        print "linea "+ linea 
        print columna
        if linea != " " and columna==0: 
            data['Key'] = str(counter)
            data['Provincia']=provincia
            data['Municipio']=linea
            columna=columna+1
            print "columna 0"
        else:
            if linea != " " and columna==1:
                data['LISTA ELECTORAL']=linea
                columna=columna+1
                print "columna 1"
            else:
                if linea != " " and columna==2:
                    data['FECHA DE POSESION']=linea
                    columna=columna+1
                    print "columna 2"
                else:
                    if linea != " " and columna==3:
                        data['ALCALDE']=linea
                        print "columna 3"
                        columna=0
                        print "columna 3"
                        counter=counter+1
                        print data, '------------'
                        scraperwiki.datastore.save(["Key"], data)  

###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key','Provincia', 'Municipio', 'ALCALDE','LISTA ELECTORAL','FECHA DE POSESION'])
column=['Key','Provincia','Municipio', 'ALCALDE','LISTA ELECTORAL','FECHA DE POSESION']
provincia=1
counter=0

for provincia in range(1,53):
    startURL="http://cooplocal.mpt.es/cgi-bin/webapb/webdriver?MItabObj=elec_prov_pdf&MInamObj=prov&MIcolObj=documento&MItypeObj=application/pdf&MIvalObj="
    pdfurl = startURL + str(provincia)
    a = scraperwiki.scrape(pdfurl)
    s = BeautifulSoup(scraperwiki.pdftoxml(a))
    data = {}
    columna=0

    for t in s.findAll('text'):
        linea=t.text
        if "Versi" in linea:
             linea=" "
        if "Alcaldes" in linea:
             linea=" "
        if "ELECCIONES" in linea:
             linea=" "
        if "ALCALDE" in linea:
             linea=" "
        if "LISTA ELECTORAL" in linea:
             linea=" "
        if "FECHA DE" in linea:
             linea=" "
        if "MUNICIPIO" in linea:
             linea=" "
        if "LISTAS ELECTORALES" in linea:
             break
        print "linea "+ linea 
        print columna
        if linea != " " and columna==0: 
            data['Key'] = str(counter)
            data['Provincia']=provincia
            data['Municipio']=linea
            columna=columna+1
            print "columna 0"
        else:
            if linea != " " and columna==1:
                data['LISTA ELECTORAL']=linea
                columna=columna+1
                print "columna 1"
            else:
                if linea != " " and columna==2:
                    data['FECHA DE POSESION']=linea
                    columna=columna+1
                    print "columna 2"
                else:
                    if linea != " " and columna==3:
                        data['ALCALDE']=linea
                        print "columna 3"
                        columna=0
                        print "columna 3"
                        counter=counter+1
                        print data, '------------'
                        scraperwiki.datastore.save(["Key"], data)  

###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup

# define the order our columns are displayed in the datastore
scraperwiki.metadata.save('data_columns', ['Key','Provincia', 'Municipio', 'ALCALDE','LISTA ELECTORAL','FECHA DE POSESION'])
column=['Key','Provincia','Municipio', 'ALCALDE','LISTA ELECTORAL','FECHA DE POSESION']
provincia=1
counter=0

for provincia in range(1,53):
    startURL="http://cooplocal.mpt.es/cgi-bin/webapb/webdriver?MItabObj=elec_prov_pdf&MInamObj=prov&MIcolObj=documento&MItypeObj=application/pdf&MIvalObj="
    pdfurl = startURL + str(provincia)
    a = scraperwiki.scrape(pdfurl)
    s = BeautifulSoup(scraperwiki.pdftoxml(a))
    data = {}
    columna=0

    for t in s.findAll('text'):
        linea=t.text
        if "Versi" in linea:
             linea=" "
        if "Alcaldes" in linea:
             linea=" "
        if "ELECCIONES" in linea:
             linea=" "
        if "ALCALDE" in linea:
             linea=" "
        if "LISTA ELECTORAL" in linea:
             linea=" "
        if "FECHA DE" in linea:
             linea=" "
        if "MUNICIPIO" in linea:
             linea=" "
        if "LISTAS ELECTORALES" in linea:
             break
        print "linea "+ linea 
        print columna
        if linea != " " and columna==0: 
            data['Key'] = str(counter)
            data['Provincia']=provincia
            data['Municipio']=linea
            columna=columna+1
            print "columna 0"
        else:
            if linea != " " and columna==1:
                data['LISTA ELECTORAL']=linea
                columna=columna+1
                print "columna 1"
            else:
                if linea != " " and columna==2:
                    data['FECHA DE POSESION']=linea
                    columna=columna+1
                    print "columna 2"
                else:
                    if linea != " " and columna==3:
                        data['ALCALDE']=linea
                        print "columna 3"
                        columna=0
                        print "columna 3"
                        counter=counter+1
                        print data, '------------'
                        scraperwiki.datastore.save(["Key"], data)  

