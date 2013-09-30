import scraperwiki

# Blank Python

try:
    scraperwiki.sqlite.execute("drop table swdata")           
except Exception, err:
    pass

scraperwiki.sqlite.attach('cancellami','a')
scraperwiki.sqlite.attach('getkompassdata','b')

# sql = "SELECT A.URL, A.Nome "
  
sql = " a.swdata.URL"
sql = sql + " FROM a.swdata LEFT JOIN b.swdata ON a.swdata.[Nome] = b.swdata.[Nome]"
sql = sql + " WHERE (((b.swdata.Nome) Is Null)); "       

data= scraperwiki.scrape("http://www.ammcomputer.com/temp/Mancanti.txt")

missing = data.splitlines()
p = range (1,10)
for i in p:
    print missing[i]


import csv          

missing = csv.reader(data.splitlines())


#print str(missing)

#http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")

#missing = scraperwiki.sqlite.select(sql)  
#scraperwiki.sqlite.save(unique_keys=['URL'], data=missing,table_name="swdata")
import scraperwiki

# Blank Python

try:
    scraperwiki.sqlite.execute("drop table swdata")           
except Exception, err:
    pass

scraperwiki.sqlite.attach('cancellami','a')
scraperwiki.sqlite.attach('getkompassdata','b')

# sql = "SELECT A.URL, A.Nome "
  
sql = " a.swdata.URL"
sql = sql + " FROM a.swdata LEFT JOIN b.swdata ON a.swdata.[Nome] = b.swdata.[Nome]"
sql = sql + " WHERE (((b.swdata.Nome) Is Null)); "       

data= scraperwiki.scrape("http://www.ammcomputer.com/temp/Mancanti.txt")

missing = data.splitlines()
p = range (1,10)
for i in p:
    print missing[i]


import csv          

missing = csv.reader(data.splitlines())


#print str(missing)

#http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")

#missing = scraperwiki.sqlite.select(sql)  
#scraperwiki.sqlite.save(unique_keys=['URL'], data=missing,table_name="swdata")
