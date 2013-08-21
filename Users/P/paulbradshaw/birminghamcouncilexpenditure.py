import scraperwiki
import csv
#guidance on csv library at https://scraperwiki.com/docs/python/python_csv_guide/

#scrape the csv file into new variable 'data'
data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

#use .reader function and .splitlines() method to put 'data' into csv object 'reader'
reader = csv.reader(data.splitlines())
print reader

record = {}

for row in reader:
    record['Vendor'] = row[0]
    record['Vendor Name'] = row[1]
    record[' Invoice Amount '] = row[2]
    record['Payment Date'] = row[3]
    record['Doc Number'] = row[4]
    record['Invoice Ref'] = row[5]
    record['Cost Cente'] = row[6]
    record['Directorate'] = row[7]
    print record
    scraperwiki.sqlite.save(['Doc Number'], record)

#After first (header) row, this will generate an error with this data:
#SqliteError: Binary strings must be utf-8 encoded

#To see what happens next, go to: https://scraperwiki.com/scrapers/birminghamcouncilexpenditure_2nd/
