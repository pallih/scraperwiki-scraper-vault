import scraperwiki
import csv
#for the previous installment see https://scraperwiki.com/scrapers/birminghamcouncilexpenditure/

#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

#first attempt generated an error: "SqliteError: Binary strings must be utf-8 encoded"
#So we need to trace which part of our data is responsible. We're going to 

reader = csv.reader(data.splitlines())

record = {}

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

for row in reader:
    print type(row[0])
    print type(row[1])
    print type(row[2])
    print type(row[3])
    print type(row[4])
    print type(row[5])
    print type(row[6])
    print type(row[7])
    record['Vendor'] = row[0].decode("utf-8")
    record['Vendor Name'] = row[1].decode("utf-8")
    record[' Invoice Amount '] = row[2].decode("latin-1")
    record['Payment Date'] = row[3].decode("utf-8")
    record['Doc Number'] = row[4].decode("utf-8")
    record['Invoice Ref'] = row[5].decode("utf-8")
    record['Cost Cente'] = row[6].decode("utf-8")
    record['Directorate'] = row[7].decode("utf-8")
    print record
    scraperwiki.sqlite.save(['Invoice Ref'], record)

import scraperwiki
import csv
#for the previous installment see https://scraperwiki.com/scrapers/birminghamcouncilexpenditure/

#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

#first attempt generated an error: "SqliteError: Binary strings must be utf-8 encoded"
#So we need to trace which part of our data is responsible. We're going to 

reader = csv.reader(data.splitlines())

record = {}

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

for row in reader:
    print type(row[0])
    print type(row[1])
    print type(row[2])
    print type(row[3])
    print type(row[4])
    print type(row[5])
    print type(row[6])
    print type(row[7])
    record['Vendor'] = row[0].decode("utf-8")
    record['Vendor Name'] = row[1].decode("utf-8")
    record[' Invoice Amount '] = row[2].decode("latin-1")
    record['Payment Date'] = row[3].decode("utf-8")
    record['Doc Number'] = row[4].decode("utf-8")
    record['Invoice Ref'] = row[5].decode("utf-8")
    record['Cost Cente'] = row[6].decode("utf-8")
    record['Directorate'] = row[7].decode("utf-8")
    print record
    scraperwiki.sqlite.save(['Invoice Ref'], record)

import scraperwiki
import csv
#for the previous installment see https://scraperwiki.com/scrapers/birminghamcouncilexpenditure/

#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

#first attempt generated an error: "SqliteError: Binary strings must be utf-8 encoded"
#So we need to trace which part of our data is responsible. We're going to 

reader = csv.reader(data.splitlines())

record = {}

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

for row in reader:
    print type(row[0])
    print type(row[1])
    print type(row[2])
    print type(row[3])
    print type(row[4])
    print type(row[5])
    print type(row[6])
    print type(row[7])
    record['Vendor'] = row[0].decode("utf-8")
    record['Vendor Name'] = row[1].decode("utf-8")
    record[' Invoice Amount '] = row[2].decode("latin-1")
    record['Payment Date'] = row[3].decode("utf-8")
    record['Doc Number'] = row[4].decode("utf-8")
    record['Invoice Ref'] = row[5].decode("utf-8")
    record['Cost Cente'] = row[6].decode("utf-8")
    record['Directorate'] = row[7].decode("utf-8")
    print record
    scraperwiki.sqlite.save(['Invoice Ref'], record)

import scraperwiki
import csv
#for the previous installment see https://scraperwiki.com/scrapers/birminghamcouncilexpenditure/

#more on csv library: https://scraperwiki.com/docs/python/python_csv_guide/

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

#first attempt generated an error: "SqliteError: Binary strings must be utf-8 encoded"
#So we need to trace which part of our data is responsible. We're going to 

reader = csv.reader(data.splitlines())

record = {}

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

for row in reader:
    print type(row[0])
    print type(row[1])
    print type(row[2])
    print type(row[3])
    print type(row[4])
    print type(row[5])
    print type(row[6])
    print type(row[7])
    record['Vendor'] = row[0].decode("utf-8")
    record['Vendor Name'] = row[1].decode("utf-8")
    record[' Invoice Amount '] = row[2].decode("latin-1")
    record['Payment Date'] = row[3].decode("utf-8")
    record['Doc Number'] = row[4].decode("utf-8")
    record['Invoice Ref'] = row[5].decode("utf-8")
    record['Cost Cente'] = row[6].decode("utf-8")
    record['Directorate'] = row[7].decode("utf-8")
    print record
    scraperwiki.sqlite.save(['Invoice Ref'], record)

