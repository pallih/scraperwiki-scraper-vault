import scraperwiki
import csv

cabinet_csv = "https://docs.google.com/spreadsheet/pub?key=0ApL1zT2P00q5dFlIa0k3bUZFSVA4NVc5akZIZ3hkRlE&output=csv"

table_list =[]
data = scraperwiki.scrape(cabinet_csv)
data_table = csv.DictReader(data.splitlines())

for row in data_table:
    print row
    scraperwiki.sqlite.save(unique_keys=['Councillor'], data=row)import scraperwiki
import csv

cabinet_csv = "https://docs.google.com/spreadsheet/pub?key=0ApL1zT2P00q5dFlIa0k3bUZFSVA4NVc5akZIZ3hkRlE&output=csv"

table_list =[]
data = scraperwiki.scrape(cabinet_csv)
data_table = csv.DictReader(data.splitlines())

for row in data_table:
    print row
    scraperwiki.sqlite.save(unique_keys=['Councillor'], data=row)