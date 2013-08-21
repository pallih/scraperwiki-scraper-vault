import scraperwiki
import lxml.html
import re
import time
import dateutil.parser


DEBUG = 1
RESUME = 0
# targets = ["302856", "306018", "305690", "301069", "300304"]
targets = ["302780"]


mesi = {"gennaio":"jan","febbraio":"feb","marzo":"mar","aprile":"apr","maggio":"may","giugno":"jun","luglio":"jul","agosto":"aug",
"settembre":"sep","ottobre":"oct","novembre":"nov","dicembre":"dec"}

def format_date(d):
    for i in mesi:
        if i in d:
            d = d.replace(i, mesi[i]).replace(u"\xb0", "")
            return dateutil.parser.parse(d).date()

def scrape_bio(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    id = re.match(".*idPersona=([0-9]+)", url).group(1)
    if DEBUG == 1: 
        print "***************************************"
        print "id:", id

    t = root.cssselect('div.nominativo')[0].text
    t = ' '.join(t.split())
    if DEBUG == 1: print "STRING:", re.escape(t)
    matchObj = re.match("(?P<cognome>[A-Z ']+) (?P<nome>([A-Z][a-z-']+(\s(?!-))?)+)( - (?P<gruppo>\w+))?", t)
    cognome = matchObj.group('cognome')
    nome = matchObj.group('nome')
    gruppo = matchObj.group('gruppo')
    if DEBUG == 1:
        print "nome:", re.escape(nome)
        print "cognome:", re.escape(cognome)
        print "gruppo:", gruppo

    foto = root.cssselect('img.fotoDep')[0].attrib['src']

    dati_bio = root.cssselect('div.datibiografici h4')
    if "Nato" in dati_bio[0].text:
        sesso = "M"
    else:
        sesso = "F"
    if DEBUG == 1: print "sesso:", sesso

    matchObj = re.match("(?P<luogo>.+),\s+(il |l')(?P<data>\d{1,2}\W? [a-z]+ \d{4})", dati_bio[0].tail)
    luogo_n = matchObj.group('luogo')
    data_n = format_date(matchObj.group('data'))
    if DEBUG == 1:
        print "data di nascita:", data_n
        print "luogo di nascita:", re.escape(luogo_n)

    cv = root.cssselect('div.datibiografici div.spazioVuoto')[0].tail.strip()    
    if DEBUG == 1: print "professione:", re.escape(cv)

    cessazione = ""
    for i in root.cssselect('div.datielettoriali div h4'):
        if "circoscrizione" in i.text:
            circoscrizione = i.tail.strip()
        elif "Collegio" in i.text:
            collegio = i.tail.strip()
        elif "Lista" in i.text or "Simbolo" in i.text:
            lista = i.tail.strip()
            if DEBUG == 1: print "lista:", lista
        elif "Proclamat" in  i.text:
            t = re.match("(il |l')(?P<data>\d{1,2}\W? [a-z]+ \d{4})", i.tail).group('data')
            proclamazione = format_date(t)
            if DEBUG == 1: print "proclamazione:", proclamazione
        elif "Cessat" in  i.text:
            t = re.match("(il |l')(\d{1,2}\W? [a-z]+ \d{4})", i.tail).group(2)
            cessazione = format_date(t)
            if DEBUG == 1: print "cessazione:", cessazione

    if 'collegio' in locals():
        circoscrizione = circoscrizione + " / " + collegio
    if DEBUG == 1: print "circoscrizione:", circoscrizione

    legisl = ""
    legisl_n = "0"
    for i in root.cssselect('div.datiDeputato div h4 a'):
        if 'storia.camera.it' in i.attrib['href']:
            legisl_n = len(i.getparent().tail.split(','))
            legisl = i.getparent().tail.strip()
            break
    if DEBUG == 1:
        print "altre leg.(n):", legisl_n
        print "altre leg.:", legisl

    email = ""
    t = root.cssselect('div[class="buttonAttivita buttonPersonale buttonMail"] a')
    if t:
        matchObj = re.match(".*&email=([\w-]+@[\w-]+\.\w+)", t[0].attrib['href'].strip())
        if matchObj:
            email = matchObj.group(1)
    if DEBUG == 1: print "email:", email
    else:
        record = {
            "id" : id,
            "nome" : nome,
            "cognome" : cognome,
            "gruppo" : gruppo,
            "foto" : foto,
            "data di nascita" : data_n,
            "luogo di nascita" : luogo_n,
            "lista" : lista,
            "circoscrizione" : circoscrizione,
            "scheda" : url,
            "sesso" : sesso,
            "email" : email,
            "altre leg" : legisl,
            "n altre leg" : legisl_n,
            "professione" : cv,
            "proclamazione" : proclamazione,
            "cessazione" : cessazione,
        }
        scraperwiki.sqlite.save(unique_keys=["id"], data=record)
    
    
if 'targets' in locals():
    for i in targets:
        scrape_bio("http://documenti.camera.it/apps/commonServices/getDocumento.ashx?sezione=deputati&tipoDoc=schedaDeputato&idlegislatura=17&idPersona=" + i)

elif RESUME == 1:
    q = scraperwiki.sqlite.select("id,cognome from swdata order by cognome desc limit 1")
    last_id = q[0]['id']
    last_lett = q[0]['cognome'][0]
    html = scraperwiki.scrape('http://www.camera.it/leg17/28')
    root = lxml.html.fromstring(html)
    for i in root.cssselect('div[id="composizioneOrgano"] div[class="letteredeputati"] ul li a'):
        if last_lett == i.text:
            fle = 1
        if 'fle' in locals():
            html = scraperwiki.scrape(i.attrib['href'])
            root = lxml.html.fromstring(html)
            for l in root.cssselect('ul.list_wrapper_ul div.fn a'):
                if "&idPersona="+last_id in l.attrib['href']:
                    fid = 1
                elif 'fid' in locals():
                    scrape_bio(l.attrib['href'])
                    time.sleep(2)  # be gentle, don't rush!
                    
else:
    html = scraperwiki.scrape('http://www.camera.it/leg17/28')
    root = lxml.html.fromstring(html)
    for i in root.cssselect('div[id="composizioneOrgano"] div[class="letteredeputati"] ul li a'):
        html = scraperwiki.scrape(i.attrib['href'])
        root = lxml.html.fromstring(html)
        for l in root.cssselect('ul.list_wrapper_ul div.fn a'):
            scrape_bio(l.attrib['href'])
            time.sleep(2)  # be gentle, don't rush!
            
