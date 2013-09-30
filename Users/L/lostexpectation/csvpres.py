import scraperwiki
import scraperwiki
data = scraperwiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")


import csv
reader = csv.reader(data.splitlines())


for row in reader:
    print "£%s spent on %s" % (row[7], row[3])


reader = csv.DictReader(data.splitlines())


for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)
import scraperwiki
import scraperwiki
data = scraperwiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")


import csv
reader = csv.reader(data.splitlines())


for row in reader:
    print "£%s spent on %s" % (row[7], row[3])


reader = csv.DictReader(data.splitlines())


for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)
import scraperwiki
import scraperwiki
data = scraperwiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")


import csv
reader = csv.reader(data.splitlines())


for row in reader:
    print "£%s spent on %s" % (row[7], row[3])


reader = csv.DictReader(data.splitlines())


for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)
import scraperwiki
import scraperwiki
data = scraperwiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")


import csv
reader = csv.reader(data.splitlines())


for row in reader:
    print "£%s spent on %s" % (row[7], row[3])


reader = csv.DictReader(data.splitlines())


for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)
