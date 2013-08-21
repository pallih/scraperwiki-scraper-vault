import scraperwiki
import csv
#more on csv library: http://docs.python.org/2/library/csv.html
#and https://scraperwiki.com/docs/python/python_csv_guide/

#Have asked for ucsv library to be incorporated: http://stackoverflow.com/questions/1846135/python-csv-library-with-unicode-utf-8-support-that-just-works

#page with links: http://www.birmingham.gov.uk/payment-data
#typical link: http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv
#typical HTML containing link: <p class="fileicon"><a>

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

reader = csv.DictReader(data.splitlines())

record = {}

#Accessing elements of a Python dictionary:
#http://stackoverflow.com/questions/5404665/accessing-elements-of-python-dictionary

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

#Googled how to remove the first X characters & found this:
#http://www.linuxquestions.org/questions/programming-9/python-removing-first-x-characters-516802/
for row in reader:
    print "Row item 3:", row[' Invoice Amount '][2:]
    print type(row.keys()[0])
    print type(row.keys()[1])
    print type(row.keys()[2])
    print type(row.keys()[3])
    print type(row.keys()[4])
    print type(row.keys()[5])
    print type(row.keys()[6])
    print type(row.keys()[7])
    row['Vendor'] = row['Vendor']
    row['Vendor Name'] = row['Vendor Name'].decode("utf-8")
    row[' Invoice Amount '] = row[' Invoice Amount '][2:]
    row['Payment Date'] = row['Payment Date'].decode("utf-8")
    row['Doc Number'] = row['Doc Number'].decode("utf-8")
    row['Invoice Ref'] = row['Invoice Ref'].decode("utf-8")
    row['Cost Cente'] = row['Cost Cente'].decode("utf-8")
    row['Directorate'] = row['Directorate'].decode("utf-8")
    print row['Doc Number']
    scraperwiki.sqlite.save(['Invoice Ref'], row)

