import scraperwiki



# Blank Python

data = scraperwiki.scrape("http://dl.dropbox.com/u/41726627/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader:
    print "£%s spent on %s" % (row[0], row[0])

reader = csv.DictReader(data.splitlines())
for row in reader:           
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)import scraperwiki



# Blank Python

data = scraperwiki.scrape("http://dl.dropbox.com/u/41726627/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")
import csv
reader = csv.reader(data.splitlines())
for row in reader:
    print "£%s spent on %s" % (row[0], row[0])

reader = csv.DictReader(data.splitlines())
for row in reader:           
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)