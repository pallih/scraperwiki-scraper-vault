import scraperwiki
import xlrd 

#correntemente il file originale ha un problema di date (18-lug.11)
#xlbin = scraperwiki.scrape("http://www.ristretti.it/areestudio/disagio/ricerca/2010/morti_carcere.xls")

xlbin = scraperwiki.scrape("http://www.datajournalist.it/carceri/morti_18_04_2012.xls")
book = xlrd.open_workbook(file_contents=xlbin)

sheet = book.sheet_by_index(0) 
for i in range( 4, sheet.nrows ):

    #print sheet.row_values(i)
    
    morto = {}

    morto["nome"] = sheet.row_values(i)[0]
    morto["cognome"] = sheet.row_values(i)[1]
    morto["eta"] = sheet.row_values(i)[2].replace(" anni","")
    morto["ragione_decesso"] =  sheet.row_values(i)[4]
    morto["istituto"] =  sheet.row_values(i)[5]
    
    # datetime
    datetime = list(xlrd.xldate_as_tuple(sheet.row_values(i )[3], 0)[0:3])
    datetime.reverse()
    datetime = '/'.join(str(i) for i in datetime)

    morto["data_decesso"] = datetime

    
    scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="decessi_per_istituto", verbose=2)
    

import scraperwiki
import xlrd 

#correntemente il file originale ha un problema di date (18-lug.11)
#xlbin = scraperwiki.scrape("http://www.ristretti.it/areestudio/disagio/ricerca/2010/morti_carcere.xls")

xlbin = scraperwiki.scrape("http://www.datajournalist.it/carceri/morti_18_04_2012.xls")
book = xlrd.open_workbook(file_contents=xlbin)

sheet = book.sheet_by_index(0) 
for i in range( 4, sheet.nrows ):

    #print sheet.row_values(i)
    
    morto = {}

    morto["nome"] = sheet.row_values(i)[0]
    morto["cognome"] = sheet.row_values(i)[1]
    morto["eta"] = sheet.row_values(i)[2].replace(" anni","")
    morto["ragione_decesso"] =  sheet.row_values(i)[4]
    morto["istituto"] =  sheet.row_values(i)[5]
    
    # datetime
    datetime = list(xlrd.xldate_as_tuple(sheet.row_values(i )[3], 0)[0:3])
    datetime.reverse()
    datetime = '/'.join(str(i) for i in datetime)

    morto["data_decesso"] = datetime

    
    scraperwiki.sqlite.save(["data_decesso","nome","cognome"], morto, table_name="decessi_per_istituto", verbose=2)
    

