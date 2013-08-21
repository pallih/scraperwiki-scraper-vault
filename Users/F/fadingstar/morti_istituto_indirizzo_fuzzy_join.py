import scraperwiki, string
import jellyfish
import pprint

# scraperwiki.sqlite.attach("detenuti_presenti_distribuiti_per_istituto_tipo_re", "numero_detenuti") 
scraperwiki.sqlite.attach("morti_ristretti_feb_2012_xls", "morti") 
scraperwiki.sqlite.attach("carceri", "carceri")

scraperwiki.sqlite.execute("drop table if exists morti_nelle_carceri_join")

istituti_morti = scraperwiki.sqlite.select("* from morti.decessi_per_istituto")

# estraggo tutto ciò che è "casa" (o di reclusione, o circondariale) 
# o ospedali psichiatrici 
# o sezioni distaccate
istituti_carceri = scraperwiki.sqlite.select("* from carceri.strutture_penitenziarie_italiane  where nome like 'Casa%' or nome like 'Sez%' or nome like 'Osp%'")

# Per facilitare l'incrocio con la tabella di Ristretti mappiamo
# i nomi delle carceri per come sono conosciuti nella tabella INDIRIZZI o risolvere casi di ambiguità.
# In fase di incrocio, sarà data priorità massima a questi corrispettivi (espliciti)
dictionary_aka = {

    u"Ascoli" :u"Casa circondariale - Casa di reclusione di ASCOLI PICENO",
      
    u"Genova Marassi":u"Casa circondariale di GENOVA",
    u"Genova Pontedecimo":u"Casa circondariale femminile di GENOVA",
    u"Genova":u"Casa circondariale di GENOVA",           # ?

    u"Gorgona (LI)":u"Casa di reclusione di GORGONA",

    u"Firenze Solliccianino" : u"Casa circondariale - Casa di reclusione di FIRENZE",
    u"Firenze Sollicciano" : u"Casa circondariale - Casa di reclusione di FIRENZE",

    u"Lamezia" : u"Casa circondariale di LAMEZIA TERME",
    u"Brucoli (SR)" : u"Casa circondariale di SIRACUSA",

    u"Bollate (MI)" : u"Seconda Casa di reclusione di MILANO",

    u"Cosenza" : u"Casa circondariale - Casa di reclusione di COSENZA",
    u"Caltanisssetta " : u"Casa circondariale - Casa di reclusione di CALTANISSETTA",
    u"Caserta": u"Ufficio esecuzione penale esterna di CASERTA",

    u"Castelfranco C.L.": "Casa di reclusione di CASTELFRANCO EMILIA",
    u"Castelfranco C.L. (Mo)": "Casa di reclusione di CASTELFRANCO EMILIA",

    u"Forl\xec" : u"Casa circondariale di FORLI&#39;",

    u"L\u2019Aquila":u"Casa circondariale di L&#39;AQUILA",
    
    u"Milano Opera":u"Casa circondariale - Casa di reclusione di MILANO",
    u"Opera (Mi)":u"Casa circondariale - Casa di reclusione di MILANO",
    u"Milano San Vittore":u"Casa circondariale di MILANO",
    u"San Vittore (Mi)":u"Casa circondariale di MILANO",

    u"Napoli":u"Casa circondariale  di NAPOLI",          # ?
    u"Napoli Poggioreale":u"Casa circondariale  di NAPOLI",
    u"Napoli Secondigliano":u"Centro penitenziario NAPOLI SECONDIGLIANO",
    u"Poggioreale (Na)":u"Casa circondariale  di NAPOLI",

    u"Santa Maria C.V. (Ce)":u"Casa circondariale di SANTA MARIA CAPUA VETERE",
    u"S.M. Capua Vetere (CE)":u"Casa circondariale di SANTA MARIA CAPUA VETERE",
    u"Opg Aversa":u"Ospedale psichiatrico giudiziario di AVERSA",
    u"Opg Aversa (CE)":u"Ospedale psichiatrico giudiziario di AVERSA",
    u"Opg Barcellona P.G. (ME)" : u"Ospedale psichiatrico giudiziario di BARCELLONA POZZO DI GOTTO",
    u"Opg Castiglione (MN)" : u"Ospedale psichiatrico giudiziario di CASTIGLIONE DELLE STIVIERE",
    u"Opg Montelupo (FI)" : u"Ospedale psichiatrico giudiziario di MONTELUPO FIORENTINO",
    u"Opg Reggio Emilia" : u"Ospedale psichiatrico giudiziario di REGGIO NELL&#39;EMILIA",
    u"Opg Napoli" : u"Ospedale psichiatrico giudiziario di NAPOLI",
    u"Viterbo (Osp. Belcolle)":u"Unità ospedaliera di medicina protetta  - Casa circondariale VITERBO",

    u"Massa Carrara":u"Casa circondariale - Casa di reclusione di MASSA",
    u"Mamone (CA)":u"Casa di reclusione della frazione di Mamone ONANI",

    u"Reggio Calabria": u"Casa circondariale di REGGIO DI CALABRIA",
    u"Reggio Emilia" : u"Casa circondariale di REGGIO NELL&#39;EMILIA", 
    u"Roma Rebibbia" : u"Casa circondariale di ROMA - &quot;Terza casa&quot;",
    u"Rebibbia (Ro)" : u"Casa circondariale di ROMA - &quot;Terza casa&quot;",
    u"Roma Regina Coeli" : u"Casa circondariale di ROMA",

    u"Firenze Ipm":u"Istituto Penale Minorenni di FIRENZE",

    u"Is Arenas (CA)":u"Casa di reclusione di Arbus &quot;Is Arenas&quot;",

    u"Padova C. Circ.":u"Casa circondariale di PADOVA",
    u"Padova C. Circondariale":u"Casa circondariale di PADOVA",
    u"Padova Reclusione":u"Casa di reclusione di PADOVA",

    u"Pagliarelli":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Pagliarelli (PA)":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Pagliarelli (Pa)":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Palermo Pagliarelli":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Palermo Ucciardone":u"Casa circondariale di PALERMO - Ucciardone",

    u"Ipm Casal del Marmo" : u"Istituto Penale Minorenni di ROMA",
    u"Ipm Casal del Marmo (RM)" : u"Istituto Penale Minorenni di ROMA",
    u"Ipm Casal Del Marmo (RM)" : u"Istituto Penale Minorenni di ROMA",

    u"Parma C.C.":u"Casa di reclusione di PARMA",

    u"Venezia S.M. Maggiore":u"Casa circondariale di VENEZIA",
    u"Venezia Giudecca":u"Casa circondariale di VENEZIA",
    u"Venezia":u"Casa circondariale di VENEZIA",

}

irrisolti = []

# carceri dismessi
dismessi = ["Barletta (BA)"]

for carcere_morto in istituti_morti:


    carcere_morto_nome_istituto = carcere_morto_nome_istituto_orig = carcere_morto["istituto"]
    #print carcere_morto_nome_istituto_orig

    # Priority LIST
    if carcere_morto_nome_istituto_orig in dismessi:
        continue

    if carcere_morto_nome_istituto_orig in dictionary_aka.keys():

        morto = {}

        morto["data_decesso"] = carcere_morto["data_decesso"]
        morto["nome"] = carcere_morto["nome"]
        morto["cognome"] = carcere_morto["cognome"]
        morto["eta"] = carcere_morto["eta"]
        morto["ragione_decesso"] = carcere_morto["ragione_decesso"]
        morto["istituto"] = carcere_morto["istituto"]
        morto["nome_istituto_join"] = dictionary_aka[carcere_morto_nome_istituto_orig]
    
        scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="morti_nelle_carceri_join", verbose=2) 

        continue

    # escludi CIE
    if "(cie)" in carcere_morto_nome_istituto_orig.lower() or " cie" in carcere_morto_nome_istituto_orig.lower() or " questura" in carcere_morto_nome_istituto_orig.lower() :
        continue

    # Parentesi
    parenthesis_index = carcere_morto_nome_istituto_orig.find("(")
    if parenthesis_index != -1:
        carcere_morto_nome_istituto = carcere_morto_nome_istituto_orig[0:parenthesis_index-1]

    carceri_substrings = []
    citta = ''

    for carcere_indirizzo in istituti_carceri:

        if carcere_indirizzo["citta"].lower() in carcere_morto_nome_istituto.lower():
            carceri_substrings.append(carcere_indirizzo["nome"])
            citta = carcere_indirizzo["citta"]

    if len(carceri_substrings) > 1:
        m = min = -1
        ottimale = 'NO'
        
        for c_substr in carceri_substrings:
            try:
                m = jellyfish.levenshtein_distance(c_substr,carcere_morto_nome_istituto)
            except: 
                continue;

            if (min == -1): 
                min = m

            if m <= min:
                min = m
                ottimale = c_substr
                
            dictionary_aka[carcere_morto_nome_istituto_orig] = ottimale


    elif len(carceri_substrings) == 1:
        dictionary_aka[carcere_morto_nome_istituto_orig] = carceri_substrings[0]

    elif len(carceri_substrings) == 0: 
        if carcere_morto_nome_istituto not in irrisolti:
            irrisolti.append(carcere_morto_nome_istituto_orig)
    
    morto = {}
    morto["data_decesso"] = carcere_morto["data_decesso"]
    morto["nome"] = carcere_morto["nome"]
    morto["cognome"] = carcere_morto["cognome"]
    morto["eta"] = carcere_morto["eta"] 
    morto["ragione_decesso"] = carcere_morto["ragione_decesso"]
    morto["istituto"] = carcere_morto["istituto"]
    morto["nome_istituto_join"] = dictionary_aka[carcere_morto_nome_istituto_orig]

    scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="morti_nelle_carceri_join", verbose=2)
    
pprint.pprint( dictionary_aka )
pprint.pprint( irrisolti)




import scraperwiki, string
import jellyfish
import pprint

# scraperwiki.sqlite.attach("detenuti_presenti_distribuiti_per_istituto_tipo_re", "numero_detenuti") 
scraperwiki.sqlite.attach("morti_ristretti_feb_2012_xls", "morti") 
scraperwiki.sqlite.attach("carceri", "carceri")

scraperwiki.sqlite.execute("drop table if exists morti_nelle_carceri_join")

istituti_morti = scraperwiki.sqlite.select("* from morti.decessi_per_istituto")

# estraggo tutto ciò che è "casa" (o di reclusione, o circondariale) 
# o ospedali psichiatrici 
# o sezioni distaccate
istituti_carceri = scraperwiki.sqlite.select("* from carceri.strutture_penitenziarie_italiane  where nome like 'Casa%' or nome like 'Sez%' or nome like 'Osp%'")

# Per facilitare l'incrocio con la tabella di Ristretti mappiamo
# i nomi delle carceri per come sono conosciuti nella tabella INDIRIZZI o risolvere casi di ambiguità.
# In fase di incrocio, sarà data priorità massima a questi corrispettivi (espliciti)
dictionary_aka = {

    u"Ascoli" :u"Casa circondariale - Casa di reclusione di ASCOLI PICENO",
      
    u"Genova Marassi":u"Casa circondariale di GENOVA",
    u"Genova Pontedecimo":u"Casa circondariale femminile di GENOVA",
    u"Genova":u"Casa circondariale di GENOVA",           # ?

    u"Gorgona (LI)":u"Casa di reclusione di GORGONA",

    u"Firenze Solliccianino" : u"Casa circondariale - Casa di reclusione di FIRENZE",
    u"Firenze Sollicciano" : u"Casa circondariale - Casa di reclusione di FIRENZE",

    u"Lamezia" : u"Casa circondariale di LAMEZIA TERME",
    u"Brucoli (SR)" : u"Casa circondariale di SIRACUSA",

    u"Bollate (MI)" : u"Seconda Casa di reclusione di MILANO",

    u"Cosenza" : u"Casa circondariale - Casa di reclusione di COSENZA",
    u"Caltanisssetta " : u"Casa circondariale - Casa di reclusione di CALTANISSETTA",
    u"Caserta": u"Ufficio esecuzione penale esterna di CASERTA",

    u"Castelfranco C.L.": "Casa di reclusione di CASTELFRANCO EMILIA",
    u"Castelfranco C.L. (Mo)": "Casa di reclusione di CASTELFRANCO EMILIA",

    u"Forl\xec" : u"Casa circondariale di FORLI&#39;",

    u"L\u2019Aquila":u"Casa circondariale di L&#39;AQUILA",
    
    u"Milano Opera":u"Casa circondariale - Casa di reclusione di MILANO",
    u"Opera (Mi)":u"Casa circondariale - Casa di reclusione di MILANO",
    u"Milano San Vittore":u"Casa circondariale di MILANO",
    u"San Vittore (Mi)":u"Casa circondariale di MILANO",

    u"Napoli":u"Casa circondariale  di NAPOLI",          # ?
    u"Napoli Poggioreale":u"Casa circondariale  di NAPOLI",
    u"Napoli Secondigliano":u"Centro penitenziario NAPOLI SECONDIGLIANO",
    u"Poggioreale (Na)":u"Casa circondariale  di NAPOLI",

    u"Santa Maria C.V. (Ce)":u"Casa circondariale di SANTA MARIA CAPUA VETERE",
    u"S.M. Capua Vetere (CE)":u"Casa circondariale di SANTA MARIA CAPUA VETERE",
    u"Opg Aversa":u"Ospedale psichiatrico giudiziario di AVERSA",
    u"Opg Aversa (CE)":u"Ospedale psichiatrico giudiziario di AVERSA",
    u"Opg Barcellona P.G. (ME)" : u"Ospedale psichiatrico giudiziario di BARCELLONA POZZO DI GOTTO",
    u"Opg Castiglione (MN)" : u"Ospedale psichiatrico giudiziario di CASTIGLIONE DELLE STIVIERE",
    u"Opg Montelupo (FI)" : u"Ospedale psichiatrico giudiziario di MONTELUPO FIORENTINO",
    u"Opg Reggio Emilia" : u"Ospedale psichiatrico giudiziario di REGGIO NELL&#39;EMILIA",
    u"Opg Napoli" : u"Ospedale psichiatrico giudiziario di NAPOLI",
    u"Viterbo (Osp. Belcolle)":u"Unità ospedaliera di medicina protetta  - Casa circondariale VITERBO",

    u"Massa Carrara":u"Casa circondariale - Casa di reclusione di MASSA",
    u"Mamone (CA)":u"Casa di reclusione della frazione di Mamone ONANI",

    u"Reggio Calabria": u"Casa circondariale di REGGIO DI CALABRIA",
    u"Reggio Emilia" : u"Casa circondariale di REGGIO NELL&#39;EMILIA", 
    u"Roma Rebibbia" : u"Casa circondariale di ROMA - &quot;Terza casa&quot;",
    u"Rebibbia (Ro)" : u"Casa circondariale di ROMA - &quot;Terza casa&quot;",
    u"Roma Regina Coeli" : u"Casa circondariale di ROMA",

    u"Firenze Ipm":u"Istituto Penale Minorenni di FIRENZE",

    u"Is Arenas (CA)":u"Casa di reclusione di Arbus &quot;Is Arenas&quot;",

    u"Padova C. Circ.":u"Casa circondariale di PADOVA",
    u"Padova C. Circondariale":u"Casa circondariale di PADOVA",
    u"Padova Reclusione":u"Casa di reclusione di PADOVA",

    u"Pagliarelli":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Pagliarelli (PA)":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Pagliarelli (Pa)":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Palermo Pagliarelli":u"Casa circondariale di PALERMO - Pagliarelli",
    u"Palermo Ucciardone":u"Casa circondariale di PALERMO - Ucciardone",

    u"Ipm Casal del Marmo" : u"Istituto Penale Minorenni di ROMA",
    u"Ipm Casal del Marmo (RM)" : u"Istituto Penale Minorenni di ROMA",
    u"Ipm Casal Del Marmo (RM)" : u"Istituto Penale Minorenni di ROMA",

    u"Parma C.C.":u"Casa di reclusione di PARMA",

    u"Venezia S.M. Maggiore":u"Casa circondariale di VENEZIA",
    u"Venezia Giudecca":u"Casa circondariale di VENEZIA",
    u"Venezia":u"Casa circondariale di VENEZIA",

}

irrisolti = []

# carceri dismessi
dismessi = ["Barletta (BA)"]

for carcere_morto in istituti_morti:


    carcere_morto_nome_istituto = carcere_morto_nome_istituto_orig = carcere_morto["istituto"]
    #print carcere_morto_nome_istituto_orig

    # Priority LIST
    if carcere_morto_nome_istituto_orig in dismessi:
        continue

    if carcere_morto_nome_istituto_orig in dictionary_aka.keys():

        morto = {}

        morto["data_decesso"] = carcere_morto["data_decesso"]
        morto["nome"] = carcere_morto["nome"]
        morto["cognome"] = carcere_morto["cognome"]
        morto["eta"] = carcere_morto["eta"]
        morto["ragione_decesso"] = carcere_morto["ragione_decesso"]
        morto["istituto"] = carcere_morto["istituto"]
        morto["nome_istituto_join"] = dictionary_aka[carcere_morto_nome_istituto_orig]
    
        scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="morti_nelle_carceri_join", verbose=2) 

        continue

    # escludi CIE
    if "(cie)" in carcere_morto_nome_istituto_orig.lower() or " cie" in carcere_morto_nome_istituto_orig.lower() or " questura" in carcere_morto_nome_istituto_orig.lower() :
        continue

    # Parentesi
    parenthesis_index = carcere_morto_nome_istituto_orig.find("(")
    if parenthesis_index != -1:
        carcere_morto_nome_istituto = carcere_morto_nome_istituto_orig[0:parenthesis_index-1]

    carceri_substrings = []
    citta = ''

    for carcere_indirizzo in istituti_carceri:

        if carcere_indirizzo["citta"].lower() in carcere_morto_nome_istituto.lower():
            carceri_substrings.append(carcere_indirizzo["nome"])
            citta = carcere_indirizzo["citta"]

    if len(carceri_substrings) > 1:
        m = min = -1
        ottimale = 'NO'
        
        for c_substr in carceri_substrings:
            try:
                m = jellyfish.levenshtein_distance(c_substr,carcere_morto_nome_istituto)
            except: 
                continue;

            if (min == -1): 
                min = m

            if m <= min:
                min = m
                ottimale = c_substr
                
            dictionary_aka[carcere_morto_nome_istituto_orig] = ottimale


    elif len(carceri_substrings) == 1:
        dictionary_aka[carcere_morto_nome_istituto_orig] = carceri_substrings[0]

    elif len(carceri_substrings) == 0: 
        if carcere_morto_nome_istituto not in irrisolti:
            irrisolti.append(carcere_morto_nome_istituto_orig)
    
    morto = {}
    morto["data_decesso"] = carcere_morto["data_decesso"]
    morto["nome"] = carcere_morto["nome"]
    morto["cognome"] = carcere_morto["cognome"]
    morto["eta"] = carcere_morto["eta"] 
    morto["ragione_decesso"] = carcere_morto["ragione_decesso"]
    morto["istituto"] = carcere_morto["istituto"]
    morto["nome_istituto_join"] = dictionary_aka[carcere_morto_nome_istituto_orig]

    scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="morti_nelle_carceri_join", verbose=2)
    
pprint.pprint( dictionary_aka )
pprint.pprint( irrisolti)




