import scraperwiki
import csv

# http://airnowgateway.org/assets/Hourly%20Data%20Fact%20Sheet.pdf

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield dict([(key, utf(value)) for key, value in row.iteritems()])

def utf(value):
    try:
        return unicode(value, 'ISO-8859-1')
    except:
        return "X"

data = scraperwiki.scrape("ftp://ftp.airnowgateway.org/HourlyData/2013020316.dat")
     
reader = UnicodeDictReader(data.splitlines(), fieldnames=[u"date", u"time", u"aqsid", u"site", u"offset", u"param", u"units", u"value", u"source"], delimiter="|")

i=0
for row in reader:
    #print row
    scraperwiki.sqlite.save(unique_keys=[u"date", u"time", u"aqsid", u"param"], data=row)
    i=i+1
    if i>10:
        break