import scraperwiki           
import lxml.html
import csv
import re
import dateutil.parser

html = scraperwiki.scrape("http://www.birmingham.gov.uk/payment-data")
          
root = lxml.html.fromstring(html)
link = root.find_class('fileicon')

for a in link:
    if link.index(a)%2:
        print a[0].get('href')
        data = scraperwiki.scrape("http://www.birmingham.gov.uk/" + a[0].get('href'))  
        reader = csv.DictReader(data.splitlines())
        for row in reader:
            if row.has_key(' Invoice Am '):
            #deal with April 2011 headers in csv
                if row.has_key(None):
                #deal with data with no heading
                    del row[None]   
                if row['Doc Number']:
                    row['Doc Number'] = int(row['Doc Number'])
                    row['Invoice Amount'] = float(re.sub(r"[^\w.]", "", row[' Invoice Am ']))
                    del row[' Invoice Am ']
                    row['Payment Date'] = dateutil.parser.parse(row['Pay.Due Da'], dayfirst=True).date()
                    del row['Pay.Due Da']
                    row['Vendor Name'] = row['Vendor Nam']
                    del row['Vendor Nam']
                    scraperwiki.sqlite.save(unique_keys=['Doc Number'], data=row)  
            else:
            #all other months
                if row.has_key(None):
                    #deal with data with no heading in January 2012 CSV
                    del row[None]   
                if row['Doc Number']:
                    del row['']
                    row['Doc Number'] = int(row['Doc Number'])
                    row['Invoice Amount'] = float(re.sub(r"[^\w.]", "", row[' Invoice Amount ']))
                    del row[' Invoice Amount ']
                    row['Payment Date'] = dateutil.parser.parse(row['Payment Date'], dayfirst=True).date()
                    #row['Vendor Number'] = int(row['Vendor Number']) -> this name varies in each csv, ignore for now
                    scraperwiki.sqlite.save(unique_keys=['Doc Number'], data=row)                import scraperwiki           
import lxml.html
import csv
import re
import dateutil.parser

html = scraperwiki.scrape("http://www.birmingham.gov.uk/payment-data")
          
root = lxml.html.fromstring(html)
link = root.find_class('fileicon')

for a in link:
    if link.index(a)%2:
        print a[0].get('href')
        data = scraperwiki.scrape("http://www.birmingham.gov.uk/" + a[0].get('href'))  
        reader = csv.DictReader(data.splitlines())
        for row in reader:
            if row.has_key(' Invoice Am '):
            #deal with April 2011 headers in csv
                if row.has_key(None):
                #deal with data with no heading
                    del row[None]   
                if row['Doc Number']:
                    row['Doc Number'] = int(row['Doc Number'])
                    row['Invoice Amount'] = float(re.sub(r"[^\w.]", "", row[' Invoice Am ']))
                    del row[' Invoice Am ']
                    row['Payment Date'] = dateutil.parser.parse(row['Pay.Due Da'], dayfirst=True).date()
                    del row['Pay.Due Da']
                    row['Vendor Name'] = row['Vendor Nam']
                    del row['Vendor Nam']
                    scraperwiki.sqlite.save(unique_keys=['Doc Number'], data=row)  
            else:
            #all other months
                if row.has_key(None):
                    #deal with data with no heading in January 2012 CSV
                    del row[None]   
                if row['Doc Number']:
                    del row['']
                    row['Doc Number'] = int(row['Doc Number'])
                    row['Invoice Amount'] = float(re.sub(r"[^\w.]", "", row[' Invoice Amount ']))
                    del row[' Invoice Amount ']
                    row['Payment Date'] = dateutil.parser.parse(row['Payment Date'], dayfirst=True).date()
                    #row['Vendor Number'] = int(row['Vendor Number']) -> this name varies in each csv, ignore for now
                    scraperwiki.sqlite.save(unique_keys=['Doc Number'], data=row)                