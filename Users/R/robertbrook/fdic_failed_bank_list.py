import scraperwiki
import csv

starting_url = 'http://www.fdic.gov/bank/individual/failed/banklist.csv'
csvfile = scraperwiki.scrape(starting_url)

reader = csv.reader(csvfile.encode('utf-8'), delimiter=",")

print reader

for rows in reader:
       print rows



