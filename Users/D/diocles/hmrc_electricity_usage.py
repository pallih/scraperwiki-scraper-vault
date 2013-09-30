import scraperwiki
import lxml.html
import urllib
import csv
import StringIO

def process(url):
    # FIXME: Is this UTF-8 encoding?
    data = urllib.urlopen(url).read()
    csv_file = StringIO.StringIO(data)
    doc = csv.reader(csv_file)

    # Discard headers
    for i in range(0,4):
        doc.next()

    # Assume the times given are GMT rather than BST.
    times = doc.next()

    for line in doc:
        date = line[3]
        print "Processing: %s" % date

        for i in range(4,52):
            record = {
                "datetime": "%s %s" % (date, times[i]),
                "usage": line[i],
            }

            scraperwiki.sqlite.save(unique_keys=['datetime'],data=record)

data_url = "http://data.carbonculture.net/orgs/hmrc/100-parliament-street/reports/elec00.csv"
process(data_url)
import scraperwiki
import lxml.html
import urllib
import csv
import StringIO

def process(url):
    # FIXME: Is this UTF-8 encoding?
    data = urllib.urlopen(url).read()
    csv_file = StringIO.StringIO(data)
    doc = csv.reader(csv_file)

    # Discard headers
    for i in range(0,4):
        doc.next()

    # Assume the times given are GMT rather than BST.
    times = doc.next()

    for line in doc:
        date = line[3]
        print "Processing: %s" % date

        for i in range(4,52):
            record = {
                "datetime": "%s %s" % (date, times[i]),
                "usage": line[i],
            }

            scraperwiki.sqlite.save(unique_keys=['datetime'],data=record)

data_url = "http://data.carbonculture.net/orgs/hmrc/100-parliament-street/reports/elec00.csv"
process(data_url)
