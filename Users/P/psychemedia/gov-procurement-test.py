import scraperwiki
import csv,urllib

url='http://assets.businesslink.gov.uk/transparency/TenderSummary.csv'
f = urllib.urlopen(url)
f.readline()
data = csv.DictReader(f)

 
currTender=''
for d in data:
    if currTender==d['Organisation tender reference']: 
        #DEDUPLICATION ON TENDER ORDER NUMBER
        pass
    else:
        record={}
        for item in d:
            record[item.decode('latin1').encode('utf-8')]=d[item].decode('latin1').encode('utf-8')
        print record
        currTender=d['Organisation tender reference']
        scraperwiki.datastore.save(['Organisation tender reference'], record)
import scraperwiki
import csv,urllib

url='http://assets.businesslink.gov.uk/transparency/TenderSummary.csv'
f = urllib.urlopen(url)
f.readline()
data = csv.DictReader(f)

 
currTender=''
for d in data:
    if currTender==d['Organisation tender reference']: 
        #DEDUPLICATION ON TENDER ORDER NUMBER
        pass
    else:
        record={}
        for item in d:
            record[item.decode('latin1').encode('utf-8')]=d[item].decode('latin1').encode('utf-8')
        print record
        currTender=d['Organisation tender reference']
        scraperwiki.datastore.save(['Organisation tender reference'], record)
