import scraperwiki
import csv

#page with links: http://www.bolton.gov.uk/website/pages/Councilprocurementexpenditure.aspx
#typical link: 
#typical HTML containing link: 

data = scraperwiki.scrape('http://www.bolton.gov.uk/sites/DocumentCentre/Documents/Expenditure%20over%20%C2%A3500%20for%20April%202011.csv')

reader = csv.DictReader(data.splitlines())

for row in reader:
#    if row['Invoice Amount']:
    print row
#    row['Amount'] = float(row['Doc Number'])
 #       row['vendor code'] = row[0]
  #      row['vendor name'] = row[1]
    print row['Invoice ID']
    scraperwiki.sqlite.save(['Invoice ID'], row)
    
import scraperwiki
import csv

#page with links: http://www.bolton.gov.uk/website/pages/Councilprocurementexpenditure.aspx
#typical link: 
#typical HTML containing link: 

data = scraperwiki.scrape('http://www.bolton.gov.uk/sites/DocumentCentre/Documents/Expenditure%20over%20%C2%A3500%20for%20April%202011.csv')

reader = csv.DictReader(data.splitlines())

for row in reader:
#    if row['Invoice Amount']:
    print row
#    row['Amount'] = float(row['Doc Number'])
 #       row['vendor code'] = row[0]
  #      row['vendor name'] = row[1]
    print row['Invoice ID']
    scraperwiki.sqlite.save(['Invoice ID'], row)
    
import scraperwiki
import csv

#page with links: http://www.bolton.gov.uk/website/pages/Councilprocurementexpenditure.aspx
#typical link: 
#typical HTML containing link: 

data = scraperwiki.scrape('http://www.bolton.gov.uk/sites/DocumentCentre/Documents/Expenditure%20over%20%C2%A3500%20for%20April%202011.csv')

reader = csv.DictReader(data.splitlines())

for row in reader:
#    if row['Invoice Amount']:
    print row
#    row['Amount'] = float(row['Doc Number'])
 #       row['vendor code'] = row[0]
  #      row['vendor name'] = row[1]
    print row['Invoice ID']
    scraperwiki.sqlite.save(['Invoice ID'], row)
    
import scraperwiki
import csv

#page with links: http://www.bolton.gov.uk/website/pages/Councilprocurementexpenditure.aspx
#typical link: 
#typical HTML containing link: 

data = scraperwiki.scrape('http://www.bolton.gov.uk/sites/DocumentCentre/Documents/Expenditure%20over%20%C2%A3500%20for%20April%202011.csv')

reader = csv.DictReader(data.splitlines())

for row in reader:
#    if row['Invoice Amount']:
    print row
#    row['Amount'] = float(row['Doc Number'])
 #       row['vendor code'] = row[0]
  #      row['vendor name'] = row[1]
    print row['Invoice ID']
    scraperwiki.sqlite.save(['Invoice ID'], row)
    
