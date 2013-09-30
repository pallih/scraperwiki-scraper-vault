import scraperwiki
import csv

data = scraperwiki.scrape('https://docs.google.com/spreadsheet/pub?key=0AgvuL_V55IohdGZoWWprWl8wSlZzd0lQOURvMEZoTmc&output=csv')

reader = csv.DictReader(data.splitlines())

record = {}
for row in reader:
    print row
    print "Income: ", row['Income'],
    print "Expense: ", row['Expense'],
    print "Net: ", row['Net'],
    scraperwiki.sqlite.save(['Net'], row)
    
import scraperwiki
import csv

data = scraperwiki.scrape('https://docs.google.com/spreadsheet/pub?key=0AgvuL_V55IohdGZoWWprWl8wSlZzd0lQOURvMEZoTmc&output=csv')

reader = csv.DictReader(data.splitlines())

record = {}
for row in reader:
    print row
    print "Income: ", row['Income'],
    print "Expense: ", row['Expense'],
    print "Net: ", row['Net'],
    scraperwiki.sqlite.save(['Net'], row)
    
