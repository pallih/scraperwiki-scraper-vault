#This scraper uses Paul Bradshaw's CSV tutorial for the ebook Scraping for Journalists
import scraperwiki
import csv
#guidance on csv library at https://scraperwiki.com/docs/python/python_csv_guide/

#scrape the csv file into new variable 'data'
data = scraperwiki.scrape('http://www.stoke.gov.uk/ccm/cms-service/download/asset/?asset_id=401486')

#use .reader function and .splitlines() method to put 'data' into csv object 'reader'
reader = csv.reader(data.splitlines())
print reader

record = {}


for row in reader:
    
    record['Body Name'] = row[0]
    record['Code2'] = row[1]
    record[' Service Label '] = row[2]
    record['Exp code'] = row[3]
    record['Exp cat'] = row[4]
    record['Date'] = row[5]
    record['Trans Number'] = row[6]
    record['Amount'] = row[7]
    record['Supplier'] = row[8]
    print record
    scraperwiki.sqlite.save(['Trans Number'], record)


