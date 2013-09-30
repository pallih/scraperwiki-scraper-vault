import scraperwiki

# Blank Python

import csv
import requests

scraperwiki.sqlite.execute("drop table if exists climdata")
scraperwiki.sqlite.execute("create table climdata (GCM string, var string)")           
#scraperwiki.sqlite.execute("insert into ttt values (?,?)", (9, 'hello'))
#
#r = requests.get('http://vote.wa.gov/results/current/export/MediaResults.txt') 

#data = open('data/MediaResults.txt', 'r')
#reader = csv.reader(data, delimiter='\t')
#reader = csv.DictReader(data.splitlines(), delimiter='\t')


#http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python


#1. works - saves to file
#r = requests.get('http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/pr/1980/1999/ZAF.csv')
#data = r.text

#reader = csv.DictReader(data.splitlines(), delimiter=',')
#for row in reader:  
#    #print row["var"]
#    print row
#    for k,v in row.items():
#        print k,v
#        data = {
#                 k:v
#                }
#        #scraperwiki.sqlite.save(unique_keys=['GCM'], data=row)
         

#2. 
r = requests.get('http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/pr/1980/1999/ZAF.csv')
data = r.text
#reader = csv.reader(data.splitlines(), delimiter='\t')
reader = csv.DictReader(data.splitlines(), delimiter=',')
for row in reader:  
    #print row["var"]
    print row
    data = {
                 'GCM':row["GCM"],
                 'var':row["var"],
                 'from_year':row["from_year"],
                 'to_year':row["to_year"],
                 'annual':row["annual"] 
            }
    scraperwiki.sqlite.execute("insert into climdata values (:GCM, :var)", {"GCM":row["GCM"], "var":row["var"]})
scraperwiki.sqlite.commit()    
    #scraperwiki.sqlite.save(unique_keys=['GCM'], data=data)
    #for k,v in row.items():
    #    print k,v
        


#r = requests.get('http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/pr/1980/1999/ZAF.csv')
#data = r.text
#reader = csv.reader(data.splitlines(), delimiter='\t')
#reader = csv.DictReader(data.splitlines(), delimiter=',')
#for row in reader:  
#    print row
#    data = {
#            'GCM' : tds[0].text_content(),
#            'annual' : int(tds[4].text_content())
#            }
#    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

import scraperwiki

# Blank Python

import csv
import requests

scraperwiki.sqlite.execute("drop table if exists climdata")
scraperwiki.sqlite.execute("create table climdata (GCM string, var string)")           
#scraperwiki.sqlite.execute("insert into ttt values (?,?)", (9, 'hello'))
#
#r = requests.get('http://vote.wa.gov/results/current/export/MediaResults.txt') 

#data = open('data/MediaResults.txt', 'r')
#reader = csv.reader(data, delimiter='\t')
#reader = csv.DictReader(data.splitlines(), delimiter='\t')


#http://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python


#1. works - saves to file
#r = requests.get('http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/pr/1980/1999/ZAF.csv')
#data = r.text

#reader = csv.DictReader(data.splitlines(), delimiter=',')
#for row in reader:  
#    #print row["var"]
#    print row
#    for k,v in row.items():
#        print k,v
#        data = {
#                 k:v
#                }
#        #scraperwiki.sqlite.save(unique_keys=['GCM'], data=row)
         

#2. 
r = requests.get('http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/pr/1980/1999/ZAF.csv')
data = r.text
#reader = csv.reader(data.splitlines(), delimiter='\t')
reader = csv.DictReader(data.splitlines(), delimiter=',')
for row in reader:  
    #print row["var"]
    print row
    data = {
                 'GCM':row["GCM"],
                 'var':row["var"],
                 'from_year':row["from_year"],
                 'to_year':row["to_year"],
                 'annual':row["annual"] 
            }
    scraperwiki.sqlite.execute("insert into climdata values (:GCM, :var)", {"GCM":row["GCM"], "var":row["var"]})
scraperwiki.sqlite.commit()    
    #scraperwiki.sqlite.save(unique_keys=['GCM'], data=data)
    #for k,v in row.items():
    #    print k,v
        


#r = requests.get('http://climatedataapi.worldbank.org/climateweb/rest/v1/country/annualavg/pr/1980/1999/ZAF.csv')
#data = r.text
#reader = csv.reader(data.splitlines(), delimiter='\t')
#reader = csv.DictReader(data.splitlines(), delimiter=',')
#for row in reader:  
#    print row
#    data = {
#            'GCM' : tds[0].text_content(),
#            'annual' : int(tds[4].text_content())
#            }
#    scraperwiki.sqlite.save(unique_keys=['country'], data=data)

