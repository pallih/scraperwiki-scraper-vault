# -*- coding: UTF-8 -*-
#
##############################################################################
#
# == ENGLISH ==
# (italiano sotto)
#
# === LICENCE ===
# Copyright (C) 2013 Cristian Consonni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.
#
# === INFO ===
# Scraping data from: 
# http://anagrafe.iccu.sbn.it/opencms/opencms/
# Even if the footer says:
# « È libera la riproduzione dei dati per uso personale e a scopo didattico 
# e di ricerca a condizione che sia citata la fonte.
# Ogni altra riproduzione integrale o parziale dei dati, mediante qualsiasi 
# procedimento, deve essere autorizzata dall'ICCU»
#
# Scraped data are open under CC0 1.0 Universal Public Domain Dedication
# {{it}} http://www.beniculturali.it/ \
#            mibac/export/MiBAC/sito-MiBAC/ \
#                MenuPrincipale/Trasparenza/Open-Data/index.html
#
#
# == ITALIANO == 
#
# === LICENZA ===
# Questo scraper è rilasciato con licenza GPL (v.sopra)
#
# === INFO ===
# Scraper dei dati da: 
# http://anagrafe.iccu.sbn.it/opencms/opencms/
# 
# Anche se il footer dice:
# «È libera la riproduzione dei dati per uso personale e a scopo didattico 
# e di ricerca a condizione che sia citata la fonte.
# Ogni altra riproduzione integrale o parziale dei dati, mediante qualsiasi 
# procedimento, deve essere autorizzata dall'ICCU»
#
# {{it}} http://www.beniculturali.it/ \
#            mibac/export/MiBAC/sito-MiBAC/ \
#                MenuPrincipale/Trasparenza/Open-Data/index.html
#
##############################################################################


import scraperwiki
import urllib2
from urlparse import urlparse, parse_qs
import re
import time
import lxml
import lxml.html as html

GIORNISETT = ['lunedì',
              'martedì',
              'mercoledì',
              'giovedì',
              'venerdì',
              'sabato',
              'domenica']

PERIODI = ['mattina',
           'pomeriggio',
           'sera']

COORDURL = 'http://anagrafe.iccu.sbn.it/opencms/markersgenerator?id_biblioteca='

MAXTRIES = 20
def get_page(url):
    fpage = None
    i=1
    while (not fpage) or (i > MAXTRIES):
        try:
            fpage = urllib2.urlopen(url)
        except Exception as e:
            print '%s' %str(e)
            fpage = None
            i=i+1

    return fpage

def save_data(biblio):
    ntry=1
    saveres = False
    while (not saveres) or (ntry > MAXTRIES):
        try:
            scraperwiki.sqlite.save(['isil'], biblio, table_name="biblioteche", verbose=2)
            saveres = True
        except Exception as e:
            print "Could not write on the database: %s" %str(e)
            saveres = False
            ntry += 1
            time.sleep(5)
    return saveres

def remove_br_tags(data,rmwith=''):
    p = re.compile(r'<br.*?>')
    return p.sub(rmwith, data)


BASEURL='http://anagrafe.iccu.sbn.it/opencms/opencms/ricerche/'

SEARCHURL='http://anagrafe.iccu.sbn.it/opencms/opencms/ricerche/risultati.html?monocampo=&regione=&provincia=&comune=&codice_isil=&ricerca_tipo=home&monocampo:tipo=AND&start={start}'

maxidd=-1

try:
    scraperwiki.sqlite.attach("swdata")
    data = scraperwiki.sqlite.select('max(idricerca) AS max FROM biblioteche')
    print data
    maxidd=data[0]['max']
except Exception as e:
    print "No table, starting from zero"

if maxidd < 1:
    maxidd=0

TOTBIBLIO=17243
for s in range(maxidd,TOTBIBLIO+1,40):
    searchurl = SEARCHURL.format(start=s)
    print 'SEARCHURL:', searchurl
    
    fpage=get_page(searchurl)
    assert fpage

    page = fpage.read()

    doc = html.document_fromstring(page)
    contenuto = doc.xpath("//div[@class='contenuto']")[0]
    lista=[(a,a.getchildren()) for a in contenuto.getchildren() if a.tag=='a']

    for a,riga in lista:
        link=a.values()[0]
        bibliourl=BASEURL+link
        par = parse_qs(urlparse(bibliourl).query)
        idd=int(par['start'][0])
        biblio = dict()
        biblio['bibliourl'] = bibliourl
        biblio['idricerca']=idd
        for el in riga:
            biblio[el.values()[0]]=el.text_content()

        print idd, 'BIBLIOURL:', bibliourl
        fpage = get_page(bibliourl)
        assert fpage

        page = fpage.read()

        doc = html.document_fromstring(page)
        contenutoleft = doc.xpath("//div[@class='content_left_dettaglio']")[0].getchildren()
        titolo=contenutoleft[0]
        othernames = dict()
        pagelist = page.split('\n')
        titolosource = pagelist[titolo.sourceline-1]
        titolosource = remove_br_tags(titolosource,rmwith='---substhere---')
        titolodoc = html.document_fromstring(titolosource)
        titolisecondari = titolodoc.xpath("//div[@class='titolo_secondario']")
        for el in titolisecondari:
            textlist = [t.encode('utf-8') for t in el.text_content().split('---substhere---')]
            #print textlist
            if textlist[0] == 'Anche':
                biblio['alternate_names'] = [t for t in textlist[1:] if t != '']
            elif textlist[0] == 'Già':
                biblio['old_names'] = [t for t in textlist[1:] if t != '']
        
        salvalink = titolodoc.xpath("//a[@class='non_salvato']")[0]
        salvalinkurl = salvalink.items()[1][1]
        idbiblio = int(parse_qs(urlparse(salvalinkurl).query)['id'][0])
        biblio['idbiblio'] = idbiblio
        coordpage = get_page(COORDURL+str(idbiblio))
        coordxml = lxml.etree.fromstring(coordpage.read())
        biblio['lat'] = coordxml.xpath("//lat")[0].text
        biblio['lon'] = coordxml.xpath("//lng")[0].text

        descr=contenutoleft[1]
        codici=descr[0]
        for ch in codici.getchildren():
            text = ch.text_content().split(':')
            name = text[0].lower().replace(' ','_')
            data = text[1]
            if name == 'codice_isil':
                continue
            biblio[name] = data

        schede=descr[1]
        titoli_schede=[a.values()[3] for a in schede if a.tag == 'a']
        for scheda in titoli_schede:
            biblio[scheda]=dict()
            schedadiv = [item for item in schede.get_element_by_id(scheda).getchildren() if item.tag == 'div']
            schedaa = [item.text for item in schede.get_element_by_id(scheda).getchildren() if item.tag == 'a']
            subschede = list()
            for div in schedadiv:
                for e in div.getchildren():
                    subscheda = dict()
                    if len(schedaa) > 0:
                        for el in e.getchildren():
                            element = el.getchildren()
                            subscheda[element[0].text_content()] = element[1].text_content()
                        subschede.append(subscheda)
                    else:
                        biblio[scheda][e[0].text_content()]=e[1].text_content()
            couples = zip(schedaa,subschede)
            #print schedaa, subschede
            #print couples
            for c in couples:
                biblio[scheda][c[0]] = c[1]

        contenutoright = doc.xpath("//div[@class='content_right_dettaglio']")[0]

        t = 0
        nexttitle = None
        isOrarioUfficiale = False
        isOrarioAltro = False
        for tag in contenutoright[0].getchildren():
            t += 1
            title = tag.values()[0]
            #print 'tag no. %d: %s' %(t,title)
            #print 'tag text: %s' %tag.text
            if isOrarioUfficiale:
                orari = tag.getchildren()[1].getchildren()[2:]
                orarilist = zip(GIORNISETT,orari)
                orarioapertura = dict()
                for o in orarilist:
                    giornosett = o[0]
                    oraris = [tag.text_content().encode('utf-8') for tag in o[1].getchildren()]
                    oraris = [None if x=='\xc2\xa0' else x for x in oraris]
                    
                    mattinotxt = ''
                    pomeriggiotxt = ''
                    seratxt = ''
                    if oraris[0] != None and oraris[1] != None:
                        mattinotxt = 'dalle %s alle %s'.encode('utf-8') %(oraris[0],oraris[1])
                    if oraris[2] != None and oraris[3] != None:
                        pomeriggiotxt = 'dalle %s alle %s'.encode('utf-8') %(oraris[2],oraris[3])
                    if oraris[4] != None and oraris[5] != None:
                        seratxt = 'dalle %s alle %s'.encode('utf-8') %(oraris[4],oraris[5])
                    orarioapertura[giornosett] = dict(zip(PERIODI,[mattinotxt,pomeriggiotxt,seratxt]))
                
                biblio[nexttitle] = orarioapertura
                orariapertura = dict()
                nexttitle = None
                isOrarioUfficiale = False

            if tag.text is not None:
                if title == 'orario_title':
                    if tag.text == 'Orario ufficiale:':
                        isOrarioUfficiale = True
                    else:
                        isOrarioAltro = True

                    nexttitle = tag.text.strip(':').lower().replace(' ','_')
                    #print 'Setting nexttitle: %s' %nexttitle

                elif (nexttitle is not None):
                    if isOrarioAltro:
                        #print 'Result - %s: %s' %(nexttitle,tag.text)
                        biblio[nexttitle] = tag.text
                        isOrarioAltro = False
                    else:
                        print 'CASO NON RICONOSCIUTO'
                        raise Exception
                    
                    nexttitle = None
            
            if title == 'indir':
                contatti = dict()
                for el in tag.getchildren():
                    if el.values()[0] == 'indirizzo':
                        biblio['indirizzo'] = el.text.encode('utf-8')
                    elif el.values()[0] == 'contatti':
                        contatto = el.getchildren()
                        tipo = contatto[0].text.lower().strip(':').strip('.')
                        val = contatto[1].text
                        infoval = None
                        #print val,infoval
                        if val is None:
                            for ch in contatto[1].getchildren():
                                if ch.tag == 'a':
                                    val = [item[1] for item in ch.items() if item[0]=='href'][0]
                                if ch.tag == 'img':
                                    infoval=[item[1] for item in ch.items() if item[0]=='title'][0]
                                    val = contatto[1].text_content()

                        contatti[tipo] = val
                        if infoval:
                            contatti[tipo+'_info'] = infoval

                biblio['contatti'] = contatti
                contatti = None

            if title == 'img':
                for ch in tag.getchildren():
                    if ch.tag == 'img':
                        biblio['image'] = dict(ch.items())

        saveres = save_data(biblio)
        assert saveres
        time.sleep(5)# -*- coding: UTF-8 -*-
#
##############################################################################
#
# == ENGLISH ==
# (italiano sotto)
#
# === LICENCE ===
# Copyright (C) 2013 Cristian Consonni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.
#
# === INFO ===
# Scraping data from: 
# http://anagrafe.iccu.sbn.it/opencms/opencms/
# Even if the footer says:
# « È libera la riproduzione dei dati per uso personale e a scopo didattico 
# e di ricerca a condizione che sia citata la fonte.
# Ogni altra riproduzione integrale o parziale dei dati, mediante qualsiasi 
# procedimento, deve essere autorizzata dall'ICCU»
#
# Scraped data are open under CC0 1.0 Universal Public Domain Dedication
# {{it}} http://www.beniculturali.it/ \
#            mibac/export/MiBAC/sito-MiBAC/ \
#                MenuPrincipale/Trasparenza/Open-Data/index.html
#
#
# == ITALIANO == 
#
# === LICENZA ===
# Questo scraper è rilasciato con licenza GPL (v.sopra)
#
# === INFO ===
# Scraper dei dati da: 
# http://anagrafe.iccu.sbn.it/opencms/opencms/
# 
# Anche se il footer dice:
# «È libera la riproduzione dei dati per uso personale e a scopo didattico 
# e di ricerca a condizione che sia citata la fonte.
# Ogni altra riproduzione integrale o parziale dei dati, mediante qualsiasi 
# procedimento, deve essere autorizzata dall'ICCU»
#
# {{it}} http://www.beniculturali.it/ \
#            mibac/export/MiBAC/sito-MiBAC/ \
#                MenuPrincipale/Trasparenza/Open-Data/index.html
#
##############################################################################


import scraperwiki
import urllib2
from urlparse import urlparse, parse_qs
import re
import time
import lxml
import lxml.html as html

GIORNISETT = ['lunedì',
              'martedì',
              'mercoledì',
              'giovedì',
              'venerdì',
              'sabato',
              'domenica']

PERIODI = ['mattina',
           'pomeriggio',
           'sera']

COORDURL = 'http://anagrafe.iccu.sbn.it/opencms/markersgenerator?id_biblioteca='

MAXTRIES = 20
def get_page(url):
    fpage = None
    i=1
    while (not fpage) or (i > MAXTRIES):
        try:
            fpage = urllib2.urlopen(url)
        except Exception as e:
            print '%s' %str(e)
            fpage = None
            i=i+1

    return fpage

def save_data(biblio):
    ntry=1
    saveres = False
    while (not saveres) or (ntry > MAXTRIES):
        try:
            scraperwiki.sqlite.save(['isil'], biblio, table_name="biblioteche", verbose=2)
            saveres = True
        except Exception as e:
            print "Could not write on the database: %s" %str(e)
            saveres = False
            ntry += 1
            time.sleep(5)
    return saveres

def remove_br_tags(data,rmwith=''):
    p = re.compile(r'<br.*?>')
    return p.sub(rmwith, data)


BASEURL='http://anagrafe.iccu.sbn.it/opencms/opencms/ricerche/'

SEARCHURL='http://anagrafe.iccu.sbn.it/opencms/opencms/ricerche/risultati.html?monocampo=&regione=&provincia=&comune=&codice_isil=&ricerca_tipo=home&monocampo:tipo=AND&start={start}'

maxidd=-1

try:
    scraperwiki.sqlite.attach("swdata")
    data = scraperwiki.sqlite.select('max(idricerca) AS max FROM biblioteche')
    print data
    maxidd=data[0]['max']
except Exception as e:
    print "No table, starting from zero"

if maxidd < 1:
    maxidd=0

TOTBIBLIO=17243
for s in range(maxidd,TOTBIBLIO+1,40):
    searchurl = SEARCHURL.format(start=s)
    print 'SEARCHURL:', searchurl
    
    fpage=get_page(searchurl)
    assert fpage

    page = fpage.read()

    doc = html.document_fromstring(page)
    contenuto = doc.xpath("//div[@class='contenuto']")[0]
    lista=[(a,a.getchildren()) for a in contenuto.getchildren() if a.tag=='a']

    for a,riga in lista:
        link=a.values()[0]
        bibliourl=BASEURL+link
        par = parse_qs(urlparse(bibliourl).query)
        idd=int(par['start'][0])
        biblio = dict()
        biblio['bibliourl'] = bibliourl
        biblio['idricerca']=idd
        for el in riga:
            biblio[el.values()[0]]=el.text_content()

        print idd, 'BIBLIOURL:', bibliourl
        fpage = get_page(bibliourl)
        assert fpage

        page = fpage.read()

        doc = html.document_fromstring(page)
        contenutoleft = doc.xpath("//div[@class='content_left_dettaglio']")[0].getchildren()
        titolo=contenutoleft[0]
        othernames = dict()
        pagelist = page.split('\n')
        titolosource = pagelist[titolo.sourceline-1]
        titolosource = remove_br_tags(titolosource,rmwith='---substhere---')
        titolodoc = html.document_fromstring(titolosource)
        titolisecondari = titolodoc.xpath("//div[@class='titolo_secondario']")
        for el in titolisecondari:
            textlist = [t.encode('utf-8') for t in el.text_content().split('---substhere---')]
            #print textlist
            if textlist[0] == 'Anche':
                biblio['alternate_names'] = [t for t in textlist[1:] if t != '']
            elif textlist[0] == 'Già':
                biblio['old_names'] = [t for t in textlist[1:] if t != '']
        
        salvalink = titolodoc.xpath("//a[@class='non_salvato']")[0]
        salvalinkurl = salvalink.items()[1][1]
        idbiblio = int(parse_qs(urlparse(salvalinkurl).query)['id'][0])
        biblio['idbiblio'] = idbiblio
        coordpage = get_page(COORDURL+str(idbiblio))
        coordxml = lxml.etree.fromstring(coordpage.read())
        biblio['lat'] = coordxml.xpath("//lat")[0].text
        biblio['lon'] = coordxml.xpath("//lng")[0].text

        descr=contenutoleft[1]
        codici=descr[0]
        for ch in codici.getchildren():
            text = ch.text_content().split(':')
            name = text[0].lower().replace(' ','_')
            data = text[1]
            if name == 'codice_isil':
                continue
            biblio[name] = data

        schede=descr[1]
        titoli_schede=[a.values()[3] for a in schede if a.tag == 'a']
        for scheda in titoli_schede:
            biblio[scheda]=dict()
            schedadiv = [item for item in schede.get_element_by_id(scheda).getchildren() if item.tag == 'div']
            schedaa = [item.text for item in schede.get_element_by_id(scheda).getchildren() if item.tag == 'a']
            subschede = list()
            for div in schedadiv:
                for e in div.getchildren():
                    subscheda = dict()
                    if len(schedaa) > 0:
                        for el in e.getchildren():
                            element = el.getchildren()
                            subscheda[element[0].text_content()] = element[1].text_content()
                        subschede.append(subscheda)
                    else:
                        biblio[scheda][e[0].text_content()]=e[1].text_content()
            couples = zip(schedaa,subschede)
            #print schedaa, subschede
            #print couples
            for c in couples:
                biblio[scheda][c[0]] = c[1]

        contenutoright = doc.xpath("//div[@class='content_right_dettaglio']")[0]

        t = 0
        nexttitle = None
        isOrarioUfficiale = False
        isOrarioAltro = False
        for tag in contenutoright[0].getchildren():
            t += 1
            title = tag.values()[0]
            #print 'tag no. %d: %s' %(t,title)
            #print 'tag text: %s' %tag.text
            if isOrarioUfficiale:
                orari = tag.getchildren()[1].getchildren()[2:]
                orarilist = zip(GIORNISETT,orari)
                orarioapertura = dict()
                for o in orarilist:
                    giornosett = o[0]
                    oraris = [tag.text_content().encode('utf-8') for tag in o[1].getchildren()]
                    oraris = [None if x=='\xc2\xa0' else x for x in oraris]
                    
                    mattinotxt = ''
                    pomeriggiotxt = ''
                    seratxt = ''
                    if oraris[0] != None and oraris[1] != None:
                        mattinotxt = 'dalle %s alle %s'.encode('utf-8') %(oraris[0],oraris[1])
                    if oraris[2] != None and oraris[3] != None:
                        pomeriggiotxt = 'dalle %s alle %s'.encode('utf-8') %(oraris[2],oraris[3])
                    if oraris[4] != None and oraris[5] != None:
                        seratxt = 'dalle %s alle %s'.encode('utf-8') %(oraris[4],oraris[5])
                    orarioapertura[giornosett] = dict(zip(PERIODI,[mattinotxt,pomeriggiotxt,seratxt]))
                
                biblio[nexttitle] = orarioapertura
                orariapertura = dict()
                nexttitle = None
                isOrarioUfficiale = False

            if tag.text is not None:
                if title == 'orario_title':
                    if tag.text == 'Orario ufficiale:':
                        isOrarioUfficiale = True
                    else:
                        isOrarioAltro = True

                    nexttitle = tag.text.strip(':').lower().replace(' ','_')
                    #print 'Setting nexttitle: %s' %nexttitle

                elif (nexttitle is not None):
                    if isOrarioAltro:
                        #print 'Result - %s: %s' %(nexttitle,tag.text)
                        biblio[nexttitle] = tag.text
                        isOrarioAltro = False
                    else:
                        print 'CASO NON RICONOSCIUTO'
                        raise Exception
                    
                    nexttitle = None
            
            if title == 'indir':
                contatti = dict()
                for el in tag.getchildren():
                    if el.values()[0] == 'indirizzo':
                        biblio['indirizzo'] = el.text.encode('utf-8')
                    elif el.values()[0] == 'contatti':
                        contatto = el.getchildren()
                        tipo = contatto[0].text.lower().strip(':').strip('.')
                        val = contatto[1].text
                        infoval = None
                        #print val,infoval
                        if val is None:
                            for ch in contatto[1].getchildren():
                                if ch.tag == 'a':
                                    val = [item[1] for item in ch.items() if item[0]=='href'][0]
                                if ch.tag == 'img':
                                    infoval=[item[1] for item in ch.items() if item[0]=='title'][0]
                                    val = contatto[1].text_content()

                        contatti[tipo] = val
                        if infoval:
                            contatti[tipo+'_info'] = infoval

                biblio['contatti'] = contatti
                contatti = None

            if title == 'img':
                for ch in tag.getchildren():
                    if ch.tag == 'img':
                        biblio['image'] = dict(ch.items())

        saveres = save_data(biblio)
        assert saveres
        time.sleep(5)