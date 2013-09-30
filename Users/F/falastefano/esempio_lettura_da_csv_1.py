import scraperwiki
import csv

# 1. Reading rows
# ---------------

# Download the CSV file first.
# (If there are quirks in the input file, you might at this point want to preprocess the data using, for example, the .replace function)
data = scraperwiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")

# Load it into the standard Python CSV reader. It needs to be a list of lines.
reader = csv.reader(data.splitlines())

# You can then loop through the rows as if they were a list.
for row in reader:
    print "£%s spent on %s" % (row[7], row[3])


# 2. Saving to the datastore
# --------------------------

# Conventionally the first line gives the names for the columns. You can get the standard reader 
# to load in each row as a dictionary, where the keys are those names.
reader = csv.DictReader(data.splitlines())

# This makes it easy to save the data. By default everything comes out as strings. 
# We convert the 'Amount' row to a number type, so that it can then be added and sorted.
for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)


import scraperwiki
import csv

# 1. Reading rows
# ---------------

# Download the CSV file first.
# (If there are quirks in the input file, you might at this point want to preprocess the data using, for example, the .replace function)
data = scraperwiki.scrape("http://s3-eu-west-1.amazonaws.com/ukhmgdata-cabinetoffice/Spend-data-2010-11-01/Spend-Transactions-with-descriptions-HMT-09-Sep-2010.csv")

# Load it into the standard Python CSV reader. It needs to be a list of lines.
reader = csv.reader(data.splitlines())

# You can then loop through the rows as if they were a list.
for row in reader:
    print "£%s spent on %s" % (row[7], row[3])


# 2. Saving to the datastore
# --------------------------

# Conventionally the first line gives the names for the columns. You can get the standard reader 
# to load in each row as a dictionary, where the keys are those names.
reader = csv.DictReader(data.splitlines())

# This makes it easy to save the data. By default everything comes out as strings. 
# We convert the 'Amount' row to a number type, so that it can then be added and sorted.
for row in reader:
    if row['Transaction Number']:
        row['Amount'] = float(row['Amount'])
        scraperwiki.sqlite.save(unique_keys=['Transaction Number', 'Expense Type', 'Expense Area'], data=row)


