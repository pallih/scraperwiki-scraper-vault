# -*- coding: utf-8 -*-
## author: Francis Lacoste
## date: 2 april 2013
## scrap la liste des cours offert pour un trimestre specfique

import scraperwiki  
import lxml.html

import urllib, urllib2

## scrap la liste des URLs pour obtenir les cours disponible.
##params = urllib.urlencode(dict(an_ses2='Hiver 2013'))

## la request
##f = urllib2.urlopen(url, params)

## récupère la liste des programmes disponible.
f = urllib2.urlopen("http://www.websysinfo.uqam.ca/regis/pkg_wpub.afficher_tous_les_prog")
data = lxml.html.fromstring(f.read())
f.close()

ProgNo = []
for i in data.cssselect("div#contenant div#banniere div#colonneCentre2colsGauche ul.liste li a.bold"):
    ProgNo.append((i.attrib['href']).split('/')[-1])

## récupère la liste des cours offert pour chaque programme
for no in ProgNo:
    f = urllib2.urlopen("http://www.websysinfo.uqam.ca/regis/PKG_WPUB.AFFICHE_CHEMINEMENT?P_prog=")
    data = lxml.html.fromstring(f.read())
    f.close()

    for i in data.cssselect("ul.liste li a"):
        data = {
            'url' : "http://www.websysinfo.uqam.ca/regis/"+i.attrib['href'],
            'progno' : no
        }
        
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)

# -*- coding: utf-8 -*-
## author: Francis Lacoste
## date: 2 april 2013
## scrap la liste des cours offert pour un trimestre specfique

import scraperwiki  
import lxml.html

import urllib, urllib2

## scrap la liste des URLs pour obtenir les cours disponible.
##params = urllib.urlencode(dict(an_ses2='Hiver 2013'))

## la request
##f = urllib2.urlopen(url, params)

## récupère la liste des programmes disponible.
f = urllib2.urlopen("http://www.websysinfo.uqam.ca/regis/pkg_wpub.afficher_tous_les_prog")
data = lxml.html.fromstring(f.read())
f.close()

ProgNo = []
for i in data.cssselect("div#contenant div#banniere div#colonneCentre2colsGauche ul.liste li a.bold"):
    ProgNo.append((i.attrib['href']).split('/')[-1])

## récupère la liste des cours offert pour chaque programme
for no in ProgNo:
    f = urllib2.urlopen("http://www.websysinfo.uqam.ca/regis/PKG_WPUB.AFFICHE_CHEMINEMENT?P_prog=")
    data = lxml.html.fromstring(f.read())
    f.close()

    for i in data.cssselect("ul.liste li a"):
        data = {
            'url' : "http://www.websysinfo.uqam.ca/regis/"+i.attrib['href'],
            'progno' : no
        }
        
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)

