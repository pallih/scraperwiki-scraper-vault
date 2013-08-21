import scraperwiki
import csv,urllib

url='http://www.dh.gov.uk/prod_consum_dh/groups/dh_digitalassets/@dh/@en/@ps/@sta/@perf/documents/digitalasset/dh_134165.csv'
f = urllib.urlopen(url)
f.readline()
f.readline()
f.readline()
f.readline()
reader = csv.DictReader(f)

for row in reader:
    data={}
    for item in row:
        item2=item.replace('&',' and ')
        item2=item2.replace('(','')
        item2=item2.replace(')','')
        data[item2]=row[item]
    scraperwiki.sqlite.save(unique_keys=[], table_name='march12', data=data)

