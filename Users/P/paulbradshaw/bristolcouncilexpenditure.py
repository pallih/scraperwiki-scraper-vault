import scraperwiki
import csv

#page with links: http://www.birmingham.gov.uk/payment-data
#typical link: http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv
#typical HTML containing link: <p class="fileicon"><a>

data = scraperwiki.scrape('http://www.bristol.gov.uk/968/500/2012/11/')

reader = csv.DictReader(data.splitlines())

record = {}
for row in reader:
#    if row['Invoice Amount']:
    print row
#    row['Amount'] = float(row['Doc Number'])
 #       row['vendor code'] = row[0]
  #      row['vendor name'] = row[1]
 #   print row['Doc Number']
  #  scraperwiki.sqlite.save(['Vendor Name'], row)
    
import scraperwiki
import csv

#page with links: http://www.birmingham.gov.uk/payment-data
#typical link: http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv
#typical HTML containing link: <p class="fileicon"><a>

data = scraperwiki.scrape('http://www.bristol.gov.uk/968/500/2012/11/')

reader = csv.DictReader(data.splitlines())

record = {}
for row in reader:
#    if row['Invoice Amount']:
    print row
#    row['Amount'] = float(row['Doc Number'])
 #       row['vendor code'] = row[0]
  #      row['vendor name'] = row[1]
 #   print row['Doc Number']
  #  scraperwiki.sqlite.save(['Vendor Name'], row)
    
