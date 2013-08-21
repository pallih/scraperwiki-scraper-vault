# coding: utf-8

import scraperwiki
import lxml.html
import re
import time
import dateutil.parser

mesi = {"gennaio":"jan","febbraio":"feb","marzo":"mar","aprile":"apr","maggio":"may","giugno":"jun","luglio":"jul","agosto":"aug",
"settembre":"sep","ottobre":"oct","novembre":"nov","dicembre":"dec"}
SITE_ROOT = 'http://www.senato.it'
LEGISL = '17'
BASE_URL = "%s/leg/%s/BGT/Schede_v3/Attsen/" %(SITE_ROOT,LEGISL)
DEBUG = 1
RESUME = 0
targets = ["29196"]

def format_date(d):
    for i in mesi:
        if i in d:
            d = d.replace(i, mesi[i]).replace(u"\xb0", "")
            return dateutil.parser.parse(d).date()

def scrape_bio(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) 

    id = re.match(".*?&id=([0-9]+)", url).group(1)
    if DEBUG == 1: print "id:", re.escape(id)

    t = root.cssselect('div.sxSmall h1')[0].text 
    matchObj = re.match("(?P<nome>([A-Z][a-z'\- ]+)+) (?P<cognome>[A-Z'\- ]+)", t)
    nome = matchObj.group('nome')
    cognome = matchObj.group('cognome')
    if DEBUG == 1:
        print "nome:", re.escape(nome)
        print "cognome:", re.escape(cognome)

    foto = SITE_ROOT + root.cssselect('table.anagrafico img.foto')[0].attrib['src']
    if DEBUG == 1: print "foto:", foto

    dati = root.cssselect('table.anagrafico td p')

    t = dati[0].text_content().encode('latin1').split('\n')
    professione = "" # Qualche timidone non la mette
    residenza = ""   # La Mangili 
    for i in t:
        if 'Senatore di diritto e a vita' in i:
            regione = "Senatore di diritto e a vita"
        elif 'Senatore a vita' in i:
            regione = "Senatore a vita"
        elif 'Regione di elezione:' in i:
            matchObj = re.match("Regione di elezione: (?P<regione>[\w\s\-]+(?!\sCollegio))\s(- Collegio: (?P<collegio>[\w ()']+)\s)?", i)
            regione = matchObj.group('regione')
            if matchObj.group('collegio'):
                regione = regione + " / " + matchObj.group('collegio')
        elif 'Circoscrizione estera' in i:
            regione = i.replace("Circoscrizione estera di elezione: ", "").strip()
        elif 'Residente a' in i:
            residenza = re.match("Residente a\s+([\w\- ()']+)\s?", i).group(1)
        elif re.match("Nat[oa]\s+(il |l')\d{1,2}\W? [a-z]+ \d{4} a [\w\- ()']+\s", i):
            matchObj = re.match("Nat(?P<sesso>[oa])\s+(il |l')(?P<data>\d{1,2}\W? [a-z]+ \d{4}) a (?P<luogo>[\w\- ()']+)\s", i)
            data_n = format_date(matchObj.group('data'))
            luogo_n = matchObj.group('luogo')
            if matchObj.group('sesso') == 'o':
                sesso = "M"
            else:
                sesso = "F"
        elif 'Professione:' in i:
            t = " ".join(t[t.index(i)+1:len(t)]).strip()
            professione = " ".join(t.split())
    if DEBUG == 1: 
        print "regione:", re.escape(regione)
        print "residenza:", re.escape(residenza)
        print "data di nascita:", data_n
        print "luogo di nascita:", re.escape(luogo_n)
        print "sesso:", sesso            
        print "professione:", professione

    elezione = format_date(dati[1].cssselect('strong')[0].text)
    proclamazione = format_date(dati[1].cssselect('strong')[1].text)
    if DEBUG == 1:
        print "elezione:", elezione
        print "proclamazione:", proclamazione

    gruppo = ""
    for i in root.cssselect('table.anagrafico td p strong a'):
        if 'tipodoc=sgrp' in i.attrib['href']:
                gruppo = i.text
                break
    if DEBUG == 1: print "gruppo:", re.escape(gruppo)

    li = root.cssselect('ul.composizione li strong')
    man_t = []
    for i in li:
        man_t.append(i.text.replace("Legislatura ", "").strip())
    mandati = ', '.join(man_t)
    mandati_n = len(li)    
    if DEBUG == 1:
        print "mandati:", re.escape(mandati)
        print "mandati(n):", mandati_n    

    email = ""
    js = root.cssselect('ul.composizione script')
    matchObj = re.match(u".*?'([\w.-]+@\w+\.[A-z]{2,3})'", js[0].text, re.S)
    if matchObj:
        email = matchObj.group(1)
    if DEBUG == 1: print "email:", re.escape(email)

    t = root.cssselect('a.cnt_website')
    if t:
        website = t[0].attrib['href']
    else:
        website = ""
    if DEBUG == 1: print "website:", re.escape(website)

    t = root.cssselect('a.cnt_twitter')
    if t:
        twitter= t[0].attrib['href']
    else:
        twitter= ""
    if DEBUG == 1: print "twitter:", re.escape(twitter)

    t = root.cssselect('a.cnt_facebook')
    if t:
        facebook = t[0].attrib['href']
    else:
        facebook = ""
    if DEBUG == 1: print "facebook:", re.escape(facebook)

    if DEBUG != 1:
        record = {
            "id" : id,
            "nome" : nome,
            "cognome" : cognome,
            "gruppo" : gruppo,
            "foto" : foto,
            "data di nascita" : data_n,
            "luogo di nascita" : luogo_n,
            "residenza" : residenza,
            "regione" : regione,
            "elezione" : elezione,
            "proclamazione" : proclamazione,
            "scheda" : url,
            "sesso" : sesso,
            "email" : email,
            "website" : website,
            "twitter" : twitter,
            "facebook" : facebook,
            "mandati" : mandati,
            "n mandati": mandati_n, 
            "professione" : professione,
        }
        scraperwiki.sqlite.save(unique_keys=["id"], data=record)


if 'targets' in locals():
    for i in targets:
        scrape_bio("http://www.senato.it/loc/link.asp?tipodoc=sattsen&leg=17&id=" + i)
        time.sleep(2)
elif RESUME == 1:
    q = scraperwiki.sqlite.select("id,cognome from swdata order by cognome desc limit 1")
    last_id = q[0]['id']
    last_lett = q[0]['cognome'][0]
    html = scraperwiki.scrape(BASE_URL + 'Sena.html')
    root = lxml.html.fromstring(html)
    for i in root.cssselect('.divNavOrizS li a'):
        if last_lett == i.text:
            fle = 1
        if 'fle' in locals():
            html = scraperwiki.scrape(BASE_URL + i.attrib['href'])
            root = lxml.html.fromstring(html)
            for l in root.cssselect('ul.composizione li a'):
                if "sattsen" in l.attrib['href']:
                    if "&id="+last_id in l.attrib['href']:
                        fid = 1
                    elif 'fid' in locals():
                        scrape_bio(SITE_ROOT + l.attrib['href'])
                        time.sleep(2)  # be gentle, don't rush! 
else:    
    html = scraperwiki.scrape(BASE_URL + 'Sena.html')
    root = lxml.html.fromstring(html)
    for l in root.cssselect('ul.composizione li a'):
        if "sattsen" in l.attrib['href']:
            scrape_bio(SITE_ROOT + l.attrib['href'])
            # be gentle, don't rush!
            time.sleep(2)
    for i in root.cssselect('.divNavOrizS li a'):
        html = scraperwiki.scrape(BASE_URL + i.attrib['href'])
        root = lxml.html.fromstring(html)
        for l in root.cssselect('ul.composizione li a'):
            if "sattsen" in l.attrib['href']:
                scrape_bio(SITE_ROOT + l.attrib['href'])
                # be gentle, don't rush!
                time.sleep(2)
