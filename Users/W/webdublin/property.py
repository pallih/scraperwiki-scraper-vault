import scraperwiki           
import csv           

data = scraperwiki.scrape("http://dublinparacon.com/PPR-2012-Dublin.csv")
reader = csv.reader(data.splitlines())
i = 0

for row in reader: 
    date = row[0]
    address = row[1]
    price = row[4]
    price.encode('utf-8')
    address.encode('utf_8')
    #price.encode('iso-8859-15')
    scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address.encode('utf_8'), "price":price, "date":date})         
import scraperwiki           
import csv           

data = scraperwiki.scrape("http://dublinparacon.com/PPR-2012-Dublin.csv")
reader = csv.reader(data.splitlines())
i = 0

for row in reader: 
    date = row[0]
    address = row[1]
    price = row[4]
    price.encode('utf-8')
    address.encode('utf_8')
    #price.encode('iso-8859-15')
    scraperwiki.sqlite.save(unique_keys=["address"], data={"address":address.encode('utf_8'), "price":price, "date":date})         
