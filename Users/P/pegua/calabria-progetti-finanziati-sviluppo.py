import scraperwiki
import csv


#http://it.ckan.net/dataset/calabria-progetti-finanziati-sviluppo
#using a dump,as the original website is down

csvfile = "http://ph34r.altervista.org/export_head.csv"

data =  scraperwiki.scrape(csvfile)

#wrong headers
reader = csv.DictReader(data.splitlines(),delimiter=';')

for row in reader:
    print row
    del row[""]       
    for k in row.keys():
        if row[k] is None :
            row[k] = ""
        row[k] = unicode(row[k],"iso8859_15")
    scraperwiki.sqlite.save(unique_keys=['col01'],data=row);
                                               
import scraperwiki
import csv


#http://it.ckan.net/dataset/calabria-progetti-finanziati-sviluppo
#using a dump,as the original website is down

csvfile = "http://ph34r.altervista.org/export_head.csv"

data =  scraperwiki.scrape(csvfile)

#wrong headers
reader = csv.DictReader(data.splitlines(),delimiter=';')

for row in reader:
    print row
    del row[""]       
    for k in row.keys():
        if row[k] is None :
            row[k] = ""
        row[k] = unicode(row[k],"iso8859_15")
    scraperwiki.sqlite.save(unique_keys=['col01'],data=row);
                                               
