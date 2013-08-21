import scraperwiki

# Blank Python


# print scraperwiki.sqlite.execute(sql)   

try:
    scraperwiki.sqlite.execute("drop table A")           
except Exception, err:
    pass
try:
    scraperwiki.sqlite.execute("drop table B")           
except Exception, err:
    pass
try:
    scraperwiki.sqlite.execute("drop table C")           
except Exception, err:
    print ('ERROR: %s\n' % str(err))

    scraperwiki.sqlite.execute("create table A ('URL' string, `Nome` string)")           
    scraperwiki.sqlite.execute("create table B ('URL' string, `Nome` string)")           
    scraperwiki.sqlite.execute("create table C ('URL' string, `Nome` string)")           


scraperwiki.sqlite.attach("cancellami")
dataA = scraperwiki.sqlite.select(           
    '''* from Cancellami.swdata 
   '''
)

scraperwiki.sqlite.save(unique_keys=['URL'], data=dataA,table_name="A", verbose=2)

scraperwiki.sqlite.attach("getkompassdata")
dataB = scraperwiki.sqlite.select(           
    '''URL,Nome from GetKompassData.swdata 
   '''
)

scraperwiki.sqlite.save(unique_keys=['URL'], data=dataB,table_name="B", verbose=2)

print  scraperwiki.sqlite.execute("select count (*) from A")           
print  scraperwiki.sqlite.execute("select count (*) from B")    

sql = "SELECT A.URL, A.Nome"
sql = " A.URL, A.Nome"
sql = sql + " FROM A LEFT JOIN B ON A.[Nome] = B.[Nome]"
sql = sql + " WHERE (((B.Nome) Is Null)); "       

missing = scraperwiki.sqlite.select(sql)  

scraperwiki.sqlite.save(unique_keys=['URL'], data=missing,table_name="C", verbose=2)

print  scraperwiki.sqlite.execute("select count (*) from C") 




