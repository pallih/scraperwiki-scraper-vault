import scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import traceback

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'


# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())

# take last n_id a make it int
scraperwiki.sqlite.attach("ristretti", "ristretti")

"""
if scraperwiki.sqlite.show_tables() == {}:
    n = sheet.nrows-4
else: 
    last_n_id_query = "n_id from ristretti.decessi_per_istituto ORDER BY n_id DESC limit 1"
    n = int(scraperwiki.sqlite.select(last_n_id_query)[0]['n_id'])
"""

# parse Excel dossier
xlbin = scraperwiki.scrape("http://ristretti.it/areestudio/disagio/ricerca/2010/morti_carcere.xls")


book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0) 

n = sheet.nrows-4

for i in range( 4, sheet.nrows ):

    try:

        morto = {}
    
        # id
        n = n - 1
        
        morto["n_id"] = n
        morto["nome"] = sheet.row_values(i)[0].strip()
        morto["cognome"] = sheet.row_values(i)[1].strip()
        morto["eta"] = sheet.row_values(i)[2].replace(" anni","").strip()
        morto["ragione_decesso"] =  sheet.row_values(i)[4].strip()
        morto["istituto"] =  sheet.row_values(i)[5].strip()
        
        morto["current_date"] = current_date    
    
        datetime = list(xlrd.xldate_as_tuple(sheet.row_values(i )[3], 0)[0:3])
        datetime.reverse()
        
    
        dt = []
        for i in datetime:
            if (len(str(i)) == 1):
                i = '0'+str(i)
            dt.append(i)
    
        datetime = str(dt[0])+'/'+str(dt[1])+'/'+str(dt[2])
    
        morto["data_decesso"] = datetime
    
    
        nome_cognome = ''
    
        if morto["nome"].lower() == 'detenuto':
            nome_cognome = morto["cognome"]
    
        if morto["cognome"].lower() == 'detenuto':
            nome_cognome = morto["nome"]
            
    
        if nome_cognome == '':
            nome_cognome = morto["nome"]+' '+morto["cognome"]
    
        # Tweet
        morto["titolo_xml"] = morto["data_decesso"]+": " + nome_cognome +", "+ morto["eta"]+ " anni, muore nel carcere di "+morto["istituto"]+ ". Causa: "+morto["ragione_decesso"].upper()+". "+hashtag
        
        scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="decessi_per_istituto", verbose=2)
        #print morto["titolo_xml"]

    except Exception, e:
        traceback.print_exc()
        continueimport scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import traceback

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'


# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())

# take last n_id a make it int
scraperwiki.sqlite.attach("ristretti", "ristretti")

"""
if scraperwiki.sqlite.show_tables() == {}:
    n = sheet.nrows-4
else: 
    last_n_id_query = "n_id from ristretti.decessi_per_istituto ORDER BY n_id DESC limit 1"
    n = int(scraperwiki.sqlite.select(last_n_id_query)[0]['n_id'])
"""

# parse Excel dossier
xlbin = scraperwiki.scrape("http://ristretti.it/areestudio/disagio/ricerca/2010/morti_carcere.xls")


book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0) 

n = sheet.nrows-4

for i in range( 4, sheet.nrows ):

    try:

        morto = {}
    
        # id
        n = n - 1
        
        morto["n_id"] = n
        morto["nome"] = sheet.row_values(i)[0].strip()
        morto["cognome"] = sheet.row_values(i)[1].strip()
        morto["eta"] = sheet.row_values(i)[2].replace(" anni","").strip()
        morto["ragione_decesso"] =  sheet.row_values(i)[4].strip()
        morto["istituto"] =  sheet.row_values(i)[5].strip()
        
        morto["current_date"] = current_date    
    
        datetime = list(xlrd.xldate_as_tuple(sheet.row_values(i )[3], 0)[0:3])
        datetime.reverse()
        
    
        dt = []
        for i in datetime:
            if (len(str(i)) == 1):
                i = '0'+str(i)
            dt.append(i)
    
        datetime = str(dt[0])+'/'+str(dt[1])+'/'+str(dt[2])
    
        morto["data_decesso"] = datetime
    
    
        nome_cognome = ''
    
        if morto["nome"].lower() == 'detenuto':
            nome_cognome = morto["cognome"]
    
        if morto["cognome"].lower() == 'detenuto':
            nome_cognome = morto["nome"]
            
    
        if nome_cognome == '':
            nome_cognome = morto["nome"]+' '+morto["cognome"]
    
        # Tweet
        morto["titolo_xml"] = morto["data_decesso"]+": " + nome_cognome +", "+ morto["eta"]+ " anni, muore nel carcere di "+morto["istituto"]+ ". Causa: "+morto["ragione_decesso"].upper()+". "+hashtag
        
        scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="decessi_per_istituto", verbose=2)
        #print morto["titolo_xml"]

    except Exception, e:
        traceback.print_exc()
        continueimport scraperwiki
import xlrd 
from time import gmtime, strftime
import random
import traceback

hashtag = 'via @Fai_Notizia #DetenutoIgnoto'


# take current time compatible to RSS2 pubDate format
current_date = strftime("%a, %d %m %Y %H:%M:%S +0000", gmtime())

# take last n_id a make it int
scraperwiki.sqlite.attach("ristretti", "ristretti")

"""
if scraperwiki.sqlite.show_tables() == {}:
    n = sheet.nrows-4
else: 
    last_n_id_query = "n_id from ristretti.decessi_per_istituto ORDER BY n_id DESC limit 1"
    n = int(scraperwiki.sqlite.select(last_n_id_query)[0]['n_id'])
"""

# parse Excel dossier
xlbin = scraperwiki.scrape("http://ristretti.it/areestudio/disagio/ricerca/2010/morti_carcere.xls")


book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0) 

n = sheet.nrows-4

for i in range( 4, sheet.nrows ):

    try:

        morto = {}
    
        # id
        n = n - 1
        
        morto["n_id"] = n
        morto["nome"] = sheet.row_values(i)[0].strip()
        morto["cognome"] = sheet.row_values(i)[1].strip()
        morto["eta"] = sheet.row_values(i)[2].replace(" anni","").strip()
        morto["ragione_decesso"] =  sheet.row_values(i)[4].strip()
        morto["istituto"] =  sheet.row_values(i)[5].strip()
        
        morto["current_date"] = current_date    
    
        datetime = list(xlrd.xldate_as_tuple(sheet.row_values(i )[3], 0)[0:3])
        datetime.reverse()
        
    
        dt = []
        for i in datetime:
            if (len(str(i)) == 1):
                i = '0'+str(i)
            dt.append(i)
    
        datetime = str(dt[0])+'/'+str(dt[1])+'/'+str(dt[2])
    
        morto["data_decesso"] = datetime
    
    
        nome_cognome = ''
    
        if morto["nome"].lower() == 'detenuto':
            nome_cognome = morto["cognome"]
    
        if morto["cognome"].lower() == 'detenuto':
            nome_cognome = morto["nome"]
            
    
        if nome_cognome == '':
            nome_cognome = morto["nome"]+' '+morto["cognome"]
    
        # Tweet
        morto["titolo_xml"] = morto["data_decesso"]+": " + nome_cognome +", "+ morto["eta"]+ " anni, muore nel carcere di "+morto["istituto"]+ ". Causa: "+morto["ragione_decesso"].upper()+". "+hashtag
        
        scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="decessi_per_istituto", verbose=2)
        #print morto["titolo_xml"]

    except Exception, e:
        traceback.print_exc()
        continue