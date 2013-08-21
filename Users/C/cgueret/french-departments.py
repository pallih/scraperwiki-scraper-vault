import urllib
import csv
import scraperwiki

url = "http://www.blog.manit4c.com/wp-content/uploads/2010/05/departements.txt"

fin = urllib.urlopen(url)
lines = fin.readlines()
clist = list(csv.reader(lines, delimiter=';', quoting=csv.QUOTE_NONE))
print len(clist)

for row in clist:
    record = {}
    record['name'] = row[1][1:-1]
    record['number'] = row[2][1:-1]
    scraperwiki.datastore.save(['number'], record)


