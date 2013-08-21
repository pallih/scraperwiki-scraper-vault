import scraperwiki           
html = scraperwiki.scrape(https://bulk.resource.org/irs.gov/eo/2013_02_PF/htaccess.2013_02_PF.txt")

import csv           
reader = csv.reader(data.splitlines())

for row in reader:           
    print "£%s name on %s" % (row[7], row[3])
        
reader = csv.DictReader(data.splitlines())    

for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)




