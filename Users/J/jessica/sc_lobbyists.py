import scraperwiki
data = scraperwiki.scrape("http://www.jessicafsparks.com/SCLobbyistsbyPrincipals.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader: 
    file1 = (row[0], row [1], row [2], row [3], row[4], row [5], row [6], row [7])

data = scraperwiki.scrape("http://multimedia.blufftontoday.com/media/pdfs/SCLobbyExpendituresbyPrincipal.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader:
    file2 = (row[0], row[36])

c=1

for lineA in file1:
    print "Record "+str(c)
    print lineA,
    lineB = file2.readline()
    if lineB == '':
        print "--"
    else:
        print lineB
    c = c + 1

