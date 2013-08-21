import scraperwiki
data = scraperwiki.scrape("http://dl.dropbox.com/u/571015/Facebook%20by%20population%20-%20BY%20COUNTRY.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader:
    print " country %s user in %s population %s are %s percent" % (row[0], row[2], row[3], row[4])
reader = csv.DictReader(data.splitlines())
for row in reader:
    if row['population']:
        row['Percentage'] = float(row['Percentage'])
        scraperwiki.sqlite.save(unique_keys=['Country', 'users', 'population'], data=row)


