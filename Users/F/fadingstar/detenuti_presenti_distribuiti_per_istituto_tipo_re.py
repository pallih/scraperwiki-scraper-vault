import scraperwiki
import urllib2
import lxml.etree
import difflib as d


url = "http://www.datajournalist.it/carceri/detenuti_01_2012.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def chunk_nome_tipo_regione(r):

    regioni = ["Valle D\'Aosta", "Piemonte", "Liguria", "Lombardia", "Veneto", "Trentino Alto-Adige", "Friuli Venezia Giulia", "Emilia Romagna", "Toscana", "Marche", "Umbria", "Lazio", "Campania", "Abruzzo","Puglia", "Basilicata", "Calabria", "Sicilia", "Sardegna"]

    regioni = map(str.upper,regioni)

    tipi = ["CC","CR","OPG","CCF", "CRF", "CL"]
    
    nome_tipo_regione = ['','','']

    r[0] = r[0].strip()
    r[1] = r[1].strip()
    r[2] = r[2].strip()

    # tre item, normalissimo
    if len(r) == 13:        
        nome_tipo_regione = [r[0].replace("  ", " "), r[1].replace("  ", " "), r[2].replace("  ", " ")]

    # o nome e tipo fusi, o tipo e regione fusi
    elif len(r) == 12:

        for tipo in tipi:
            if r[0].endswith(tipo):
                nome_tipo_regione[1] = tipo
                r[0]=r[0].replace(tipo, "")
                nome_tipo_regione[0] = r[0].strip()
                nome_tipo_regione[2] = r[1].strip()
                #print 'estratto: ',nome_tipo_regione
                return nome_tipo_regione
                
        for regione in regioni:
            if r[1].endswith(regione):
                nome_tipo_regione[2] = regione
                r[1]=r[1].replace(regione, "")
                nome_tipo_regione[0] = r[0].strip()
                nome_tipo_regione[1] = r[1].strip()
                #print 'estratto: ',nome_tipo_regione
                return nome_tipo_regione

    # tutti e tre fusi
    elif len(r) == 11:

        for regione in regioni:
            if r[0].endswith(regione):
                nome_tipo_regione[2] = regione
                r[0]=r[0].replace(regione, "")
                r[0] = r[0].strip()

        for tipo in tipi:
            if r[0].endswith(tipo):
                nome_tipo_regione[1] = tipo 
                r[0]=r[0].replace(tipo, "")
                nome_tipo_regione[0] = r[0].strip()


    return nome_tipo_regione

    

def process_record(r):
    
    print r
    
    record = {}
    r[0] = r[0].replace("  ", " ")

    first_item = chunk_nome_tipo_regione(r)
    print first_item

    record["nome_istituto"] = first_item[0].strip()
    record["tipo"] =  first_item[1].strip()
    record["regione"] =  first_item[2].strip()

    record["capienza_donne"] = r[-10].strip()
    record["capienza_uomini"] = r[-9].strip()
    record["capienza_totale"] = r[-8].strip()
    record["detenuti_donne"] = r[-7].strip()
    record["detenuti_uomini"] = r[-6].strip()
    record["detenuti_totale"] = r[-5].strip()
    record["detenuti_stranieri_donne"] = r[-4].strip()
    record["detenuti_stranieri_uomini"] = r[-3].strip()
    record["detenuti_stranieri_totale"] = r[-2].strip()
    record["percentuale_stranieri"] = r[-1].strip()
    return record
    
    

# True if testo, False if ciphers
flipper = True 
record_stack = []

for i in range (28, 33): # fino a pag. 33
    for el in list(pages[i]):    
        if el.tag == "text" and el.attrib.get("font") == '5':
            

            #print el.text[0], flipper, el.text, el.text[0].isdigit(), el.text[0].isalpha()

            # dai numeri di nuovo le lettere? fine record
            if (flipper == False and el.text[0].isalpha()):
                # dalla riga estratta, ricava un dizionario che sarà il record
                r = process_record(record_stack)
                # salva record
                scraperwiki.sqlite.save(["nome_istituto"], r, table_name="detenuti_per_istituto", verbose=2)
                # flipper torna testo
                flipper = True
                # pronti per una nuova riga della tabella
                record_stack = []
                record_stack.append(el.text)
                continue


            # numeri
            if el.text[0].isdigit() == True:
                record_stack.append(el.text)
                flipper = False

            # testo 
            if el.text[0].isalpha() == True:
                record_stack.append(el.text)

    # processa ultimo record
    r = process_record(record_stack)
    # salva ultimo record
    scraperwiki.sqlite.save(["nome_istituto"], r, table_name="detenuti_per_istituto", verbose=2)


import scraperwiki
import urllib2
import lxml.etree
import difflib as d


url = "http://www.datajournalist.it/carceri/detenuti_01_2012.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def chunk_nome_tipo_regione(r):

    regioni = ["Valle D\'Aosta", "Piemonte", "Liguria", "Lombardia", "Veneto", "Trentino Alto-Adige", "Friuli Venezia Giulia", "Emilia Romagna", "Toscana", "Marche", "Umbria", "Lazio", "Campania", "Abruzzo","Puglia", "Basilicata", "Calabria", "Sicilia", "Sardegna"]

    regioni = map(str.upper,regioni)

    tipi = ["CC","CR","OPG","CCF", "CRF", "CL"]
    
    nome_tipo_regione = ['','','']

    r[0] = r[0].strip()
    r[1] = r[1].strip()
    r[2] = r[2].strip()

    # tre item, normalissimo
    if len(r) == 13:        
        nome_tipo_regione = [r[0].replace("  ", " "), r[1].replace("  ", " "), r[2].replace("  ", " ")]

    # o nome e tipo fusi, o tipo e regione fusi
    elif len(r) == 12:

        for tipo in tipi:
            if r[0].endswith(tipo):
                nome_tipo_regione[1] = tipo
                r[0]=r[0].replace(tipo, "")
                nome_tipo_regione[0] = r[0].strip()
                nome_tipo_regione[2] = r[1].strip()
                #print 'estratto: ',nome_tipo_regione
                return nome_tipo_regione
                
        for regione in regioni:
            if r[1].endswith(regione):
                nome_tipo_regione[2] = regione
                r[1]=r[1].replace(regione, "")
                nome_tipo_regione[0] = r[0].strip()
                nome_tipo_regione[1] = r[1].strip()
                #print 'estratto: ',nome_tipo_regione
                return nome_tipo_regione

    # tutti e tre fusi
    elif len(r) == 11:

        for regione in regioni:
            if r[0].endswith(regione):
                nome_tipo_regione[2] = regione
                r[0]=r[0].replace(regione, "")
                r[0] = r[0].strip()

        for tipo in tipi:
            if r[0].endswith(tipo):
                nome_tipo_regione[1] = tipo 
                r[0]=r[0].replace(tipo, "")
                nome_tipo_regione[0] = r[0].strip()


    return nome_tipo_regione

    

def process_record(r):
    
    print r
    
    record = {}
    r[0] = r[0].replace("  ", " ")

    first_item = chunk_nome_tipo_regione(r)
    print first_item

    record["nome_istituto"] = first_item[0].strip()
    record["tipo"] =  first_item[1].strip()
    record["regione"] =  first_item[2].strip()

    record["capienza_donne"] = r[-10].strip()
    record["capienza_uomini"] = r[-9].strip()
    record["capienza_totale"] = r[-8].strip()
    record["detenuti_donne"] = r[-7].strip()
    record["detenuti_uomini"] = r[-6].strip()
    record["detenuti_totale"] = r[-5].strip()
    record["detenuti_stranieri_donne"] = r[-4].strip()
    record["detenuti_stranieri_uomini"] = r[-3].strip()
    record["detenuti_stranieri_totale"] = r[-2].strip()
    record["percentuale_stranieri"] = r[-1].strip()
    return record
    
    

# True if testo, False if ciphers
flipper = True 
record_stack = []

for i in range (28, 33): # fino a pag. 33
    for el in list(pages[i]):    
        if el.tag == "text" and el.attrib.get("font") == '5':
            

            #print el.text[0], flipper, el.text, el.text[0].isdigit(), el.text[0].isalpha()

            # dai numeri di nuovo le lettere? fine record
            if (flipper == False and el.text[0].isalpha()):
                # dalla riga estratta, ricava un dizionario che sarà il record
                r = process_record(record_stack)
                # salva record
                scraperwiki.sqlite.save(["nome_istituto"], r, table_name="detenuti_per_istituto", verbose=2)
                # flipper torna testo
                flipper = True
                # pronti per una nuova riga della tabella
                record_stack = []
                record_stack.append(el.text)
                continue


            # numeri
            if el.text[0].isdigit() == True:
                record_stack.append(el.text)
                flipper = False

            # testo 
            if el.text[0].isalpha() == True:
                record_stack.append(el.text)

    # processa ultimo record
    r = process_record(record_stack)
    # salva ultimo record
    scraperwiki.sqlite.save(["nome_istituto"], r, table_name="detenuti_per_istituto", verbose=2)


import scraperwiki
import urllib2
import lxml.etree
import difflib as d


url = "http://www.datajournalist.it/carceri/detenuti_01_2012.pdf"

pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

root = lxml.etree.fromstring(xmldata)
pages = list(root)

print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res)

def chunk_nome_tipo_regione(r):

    regioni = ["Valle D\'Aosta", "Piemonte", "Liguria", "Lombardia", "Veneto", "Trentino Alto-Adige", "Friuli Venezia Giulia", "Emilia Romagna", "Toscana", "Marche", "Umbria", "Lazio", "Campania", "Abruzzo","Puglia", "Basilicata", "Calabria", "Sicilia", "Sardegna"]

    regioni = map(str.upper,regioni)

    tipi = ["CC","CR","OPG","CCF", "CRF", "CL"]
    
    nome_tipo_regione = ['','','']

    r[0] = r[0].strip()
    r[1] = r[1].strip()
    r[2] = r[2].strip()

    # tre item, normalissimo
    if len(r) == 13:        
        nome_tipo_regione = [r[0].replace("  ", " "), r[1].replace("  ", " "), r[2].replace("  ", " ")]

    # o nome e tipo fusi, o tipo e regione fusi
    elif len(r) == 12:

        for tipo in tipi:
            if r[0].endswith(tipo):
                nome_tipo_regione[1] = tipo
                r[0]=r[0].replace(tipo, "")
                nome_tipo_regione[0] = r[0].strip()
                nome_tipo_regione[2] = r[1].strip()
                #print 'estratto: ',nome_tipo_regione
                return nome_tipo_regione
                
        for regione in regioni:
            if r[1].endswith(regione):
                nome_tipo_regione[2] = regione
                r[1]=r[1].replace(regione, "")
                nome_tipo_regione[0] = r[0].strip()
                nome_tipo_regione[1] = r[1].strip()
                #print 'estratto: ',nome_tipo_regione
                return nome_tipo_regione

    # tutti e tre fusi
    elif len(r) == 11:

        for regione in regioni:
            if r[0].endswith(regione):
                nome_tipo_regione[2] = regione
                r[0]=r[0].replace(regione, "")
                r[0] = r[0].strip()

        for tipo in tipi:
            if r[0].endswith(tipo):
                nome_tipo_regione[1] = tipo 
                r[0]=r[0].replace(tipo, "")
                nome_tipo_regione[0] = r[0].strip()


    return nome_tipo_regione

    

def process_record(r):
    
    print r
    
    record = {}
    r[0] = r[0].replace("  ", " ")

    first_item = chunk_nome_tipo_regione(r)
    print first_item

    record["nome_istituto"] = first_item[0].strip()
    record["tipo"] =  first_item[1].strip()
    record["regione"] =  first_item[2].strip()

    record["capienza_donne"] = r[-10].strip()
    record["capienza_uomini"] = r[-9].strip()
    record["capienza_totale"] = r[-8].strip()
    record["detenuti_donne"] = r[-7].strip()
    record["detenuti_uomini"] = r[-6].strip()
    record["detenuti_totale"] = r[-5].strip()
    record["detenuti_stranieri_donne"] = r[-4].strip()
    record["detenuti_stranieri_uomini"] = r[-3].strip()
    record["detenuti_stranieri_totale"] = r[-2].strip()
    record["percentuale_stranieri"] = r[-1].strip()
    return record
    
    

# True if testo, False if ciphers
flipper = True 
record_stack = []

for i in range (28, 33): # fino a pag. 33
    for el in list(pages[i]):    
        if el.tag == "text" and el.attrib.get("font") == '5':
            

            #print el.text[0], flipper, el.text, el.text[0].isdigit(), el.text[0].isalpha()

            # dai numeri di nuovo le lettere? fine record
            if (flipper == False and el.text[0].isalpha()):
                # dalla riga estratta, ricava un dizionario che sarà il record
                r = process_record(record_stack)
                # salva record
                scraperwiki.sqlite.save(["nome_istituto"], r, table_name="detenuti_per_istituto", verbose=2)
                # flipper torna testo
                flipper = True
                # pronti per una nuova riga della tabella
                record_stack = []
                record_stack.append(el.text)
                continue


            # numeri
            if el.text[0].isdigit() == True:
                record_stack.append(el.text)
                flipper = False

            # testo 
            if el.text[0].isalpha() == True:
                record_stack.append(el.text)

    # processa ultimo record
    r = process_record(record_stack)
    # salva ultimo record
    scraperwiki.sqlite.save(["nome_istituto"], r, table_name="detenuti_per_istituto", verbose=2)


