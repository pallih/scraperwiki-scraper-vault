import scraperwiki
import csv
#more on csv library: http://docs.python.org/2/library/csv.html
#and https://scraperwiki.com/docs/python/python_csv_guide/

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

reader = csv.DictReader(data.splitlines())

record = {}

#the line below generates error: AttributeError: DictReader instance has no attribute 'items'
#reader = _decode_dict(reader)

#Accessing elements of a Python dictionary:
#http://stackoverflow.com/questions/5404665/accessing-elements-of-python-dictionary

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

#Googled how to remove the first X characters & found this:
#http://www.linuxquestions.org/questions/programming-9/python-removing-first-x-characters-516802/
for row in reader:
    print "Row item 3:", row[' Invoice Amount '][2:]
    for num in range(0,8):
        print "column %d : " % num, type(row.keys()[num]) 
    row[' Invoice Amount '] = row[' Invoice Amount '][2:]
    print row['Doc Number']
    scraperwiki.sqlite.save(['Doc Number'], row)

import scraperwiki
import csv
#more on csv library: http://docs.python.org/2/library/csv.html
#and https://scraperwiki.com/docs/python/python_csv_guide/

data = scraperwiki.scrape('http://www.birmingham.gov.uk/cs/Satellite?blobcol=urldata&blobheader=application%2Fvnd.ms-excel&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223518937294&ssbinary=true&blobheadervalue1=attachment%3B+filename%3D300627Payments_over_%C2%A3500_October_2012.csv')

reader = csv.DictReader(data.splitlines())

record = {}

#the line below generates error: AttributeError: DictReader instance has no attribute 'items'
#reader = _decode_dict(reader)

#Accessing elements of a Python dictionary:
#http://stackoverflow.com/questions/5404665/accessing-elements-of-python-dictionary

#Some code that decodes UTF-8
#http://yosaito.co.uk/scraperlibs/python/scraperwiki/sqlite.py

#Googled how to remove the first X characters & found this:
#http://www.linuxquestions.org/questions/programming-9/python-removing-first-x-characters-516802/
for row in reader:
    print "Row item 3:", row[' Invoice Amount '][2:]
    for num in range(0,8):
        print "column %d : " % num, type(row.keys()[num]) 
    row[' Invoice Amount '] = row[' Invoice Amount '][2:]
    print row['Doc Number']
    scraperwiki.sqlite.save(['Doc Number'], row)

