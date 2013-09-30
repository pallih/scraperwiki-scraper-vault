# -*- coding: utf-8 -*-
## author: Francis Lacoste
## date: 13 january 2013
## scrap street name of Saint-Hyacinthe website

import scraperwiki     
import lxml.html        
import urllib, urllib2

## prepare the browser
opener = urllib2.build_opener()
urllib2.install_opener(opener)

## get a cookie
m = urllib2.Request("http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/TrouveResolution.asp")
tmp = urllib2.urlopen(m)
cookie = tmp.headers.get('Set-Cookie')

## get all streetname
s = urllib2.Request("http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Liste_Adresses.asp?PROV=VOIE")
s.add_header('Cookie', cookie)
tmp = urllib2.urlopen(s)

data = lxml.html.fromstring(tmp.read())

for link in data.xpath('//a'): 
    streetname = urllib.quote(link.text)
    if (streetname != "Aide"):
        ## search the streetname
        url = "http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Recherche.asp"
        values = {'slcArrondissement' : '54048',
                  'SELECT_VOIE' : streetname, 'SELECT_TYPE_VOIE' : '',
                  'SELECT_DE' : '1', 'SELECT_A' : '1000000',
                  'RADIO_RECH' : 'RECH_ADRESSE', 'RECHERCHER' : 'Y',
                  'NB_ENREG' : '', 'CHANGE_LANGUE' : '',
                  'ACTION' : 'RECH',
                 }

        ## send post request
        data = urllib.urlencode(values)
        asp = urllib2.Request(url, data)
        asp.add_header('Cookie', cookie)

        response = urllib2.urlopen(asp)
        
        ## scrape information (get all address)
        url = "http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Resultats.asp?RECH_SELECT_VOIE=%s&RECH_SELECT_DE=1&RECH_SELECT_A=100000" % streetname
        
        matr = urllib2.Request(url)
        matr.add_header('Cookie', cookie)
        tmp = urllib2.urlopen(matr)

        ## fill array with evaluation report url
        evalurl = []
        matricule = lxml.html.fromstring(tmp.read())
        for el in matricule.cssselect('a.LIEN_SOULIGNE'):
            url = "http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/%s" % el.attrib['href']
            evalurl.append(url)
            
        ## fetch evaluation report for this street.
        for url in evalurl:
            data = { 'taxreport' : url }
            scraperwiki.sqlite.save(unique_keys=['taxreport'], data=data)
            
            # -*- coding: utf-8 -*-
## author: Francis Lacoste
## date: 13 january 2013
## scrap street name of Saint-Hyacinthe website

import scraperwiki     
import lxml.html        
import urllib, urllib2

## prepare the browser
opener = urllib2.build_opener()
urllib2.install_opener(opener)

## get a cookie
m = urllib2.Request("http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/TrouveResolution.asp")
tmp = urllib2.urlopen(m)
cookie = tmp.headers.get('Set-Cookie')

## get all streetname
s = urllib2.Request("http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Liste_Adresses.asp?PROV=VOIE")
s.add_header('Cookie', cookie)
tmp = urllib2.urlopen(s)

data = lxml.html.fromstring(tmp.read())

for link in data.xpath('//a'): 
    streetname = urllib.quote(link.text)
    if (streetname != "Aide"):
        ## search the streetname
        url = "http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Recherche.asp"
        values = {'slcArrondissement' : '54048',
                  'SELECT_VOIE' : streetname, 'SELECT_TYPE_VOIE' : '',
                  'SELECT_DE' : '1', 'SELECT_A' : '1000000',
                  'RADIO_RECH' : 'RECH_ADRESSE', 'RECHERCHER' : 'Y',
                  'NB_ENREG' : '', 'CHANGE_LANGUE' : '',
                  'ACTION' : 'RECH',
                 }

        ## send post request
        data = urllib.urlencode(values)
        asp = urllib2.Request(url, data)
        asp.add_header('Cookie', cookie)

        response = urllib2.urlopen(asp)
        
        ## scrape information (get all address)
        url = "http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/Resultats.asp?RECH_SELECT_VOIE=%s&RECH_SELECT_DE=1&RECH_SELECT_A=100000" % streetname
        
        matr = urllib2.Request(url)
        matr.add_header('Cookie', cookie)
        tmp = urllib2.urlopen(matr)

        ## fill array with evaluation report url
        evalurl = []
        matricule = lxml.html.fromstring(tmp.read())
        for el in matricule.cssselect('a.LIEN_SOULIGNE'):
            url = "http://www.ville.st-hyacinthe.qc.ca/RoleEvaluation/asp/%s" % el.attrib['href']
            evalurl.append(url)
            
        ## fetch evaluation report for this street.
        for url in evalurl:
            data = { 'taxreport' : url }
            scraperwiki.sqlite.save(unique_keys=['taxreport'], data=data)
            
            