"""This scraper is a work in progress and I've only spent 5 minutes thusfar working on it! I aim to complete it over the coming days"""

import scraperwiki
import csv
import urllib2

# latest data - http://www.parliamentary-standards.org.uk/Files/DataDownload_Latest.csv
# 2012 - 2013 - http://www.parliamentary-standards.org.uk/Files/DataDownload_2012.csv
# 2011 - 2012 - http://www.parliamentary-standards.org.uk/Files/DataDownload_2011.csv
# 2010 - 2011 - http://www.parliamentary-standards.org.uk/Files/DataDownload_2010.csv

# Headers in CSVs
"""Year     Date     Claim No.     MP's Name     MP's Constituency     Category     Expense Type     Short Description     Details     Journey Type     From     To     Travel     Nights     Mileage     Amount Claimed     Amount Paid     Amount Not Paid     Amount Repaid     Status     Reason If Not Paid"""


# Blank Python

d = {}
d['Year'] = []
d['Date'] = []
d['Claim Ref'] = []
d['MPs Name'] = []
d['MPs Constituency'] = []
d['Category'] = []
d['Expense Type'] = []
d['Short Description'] = []
d['Details'] = []
d['Journey Type'] = []
d['Journey From'] = []
d['Journey To'] = []
d['Travel'] = []
d['Nights'] = []
d['Mileage'] = []
d['Amount Claimed'] = []
d['Amount Paid'] = []
d['Amount Not Paid'] = []
d['Amount Repaid'] = []
d['Status'] = []
d['Reason If Not Paid'] = []

response = urllib2.urlopen("http://www.parliamentary-standards.org.uk/Files/DataDownload_Latest.csv")
html = response.read()
dictReader = csv.DictReader(open(html, 'rb'), fieldnames = ['Year', 'Date', 'Claim Ref', 'MPs Name', 'MPs Constituency', 'Category',
                                                            'Expense Type', 'Short Description', 'Details', 'Journey Type', 'Journey From',
                                                            'Journey To', 'Travel', 'Nights', 'Mileage', 'Amount Claimed', 'Amount Paid',
                                                            'Amount Not Paid', 'Amount Repaid', 'Status', 'Reason If Not Paid'], delimiter = ',', quotechar = '"')

for row in dictReader:
    for key in row:
        d[key].append(row[key])
        print d
"""This scraper is a work in progress and I've only spent 5 minutes thusfar working on it! I aim to complete it over the coming days"""

import scraperwiki
import csv
import urllib2

# latest data - http://www.parliamentary-standards.org.uk/Files/DataDownload_Latest.csv
# 2012 - 2013 - http://www.parliamentary-standards.org.uk/Files/DataDownload_2012.csv
# 2011 - 2012 - http://www.parliamentary-standards.org.uk/Files/DataDownload_2011.csv
# 2010 - 2011 - http://www.parliamentary-standards.org.uk/Files/DataDownload_2010.csv

# Headers in CSVs
"""Year     Date     Claim No.     MP's Name     MP's Constituency     Category     Expense Type     Short Description     Details     Journey Type     From     To     Travel     Nights     Mileage     Amount Claimed     Amount Paid     Amount Not Paid     Amount Repaid     Status     Reason If Not Paid"""


# Blank Python

d = {}
d['Year'] = []
d['Date'] = []
d['Claim Ref'] = []
d['MPs Name'] = []
d['MPs Constituency'] = []
d['Category'] = []
d['Expense Type'] = []
d['Short Description'] = []
d['Details'] = []
d['Journey Type'] = []
d['Journey From'] = []
d['Journey To'] = []
d['Travel'] = []
d['Nights'] = []
d['Mileage'] = []
d['Amount Claimed'] = []
d['Amount Paid'] = []
d['Amount Not Paid'] = []
d['Amount Repaid'] = []
d['Status'] = []
d['Reason If Not Paid'] = []

response = urllib2.urlopen("http://www.parliamentary-standards.org.uk/Files/DataDownload_Latest.csv")
html = response.read()
dictReader = csv.DictReader(open(html, 'rb'), fieldnames = ['Year', 'Date', 'Claim Ref', 'MPs Name', 'MPs Constituency', 'Category',
                                                            'Expense Type', 'Short Description', 'Details', 'Journey Type', 'Journey From',
                                                            'Journey To', 'Travel', 'Nights', 'Mileage', 'Amount Claimed', 'Amount Paid',
                                                            'Amount Not Paid', 'Amount Repaid', 'Status', 'Reason If Not Paid'], delimiter = ',', quotechar = '"')

for row in dictReader:
    for key in row:
        d[key].append(row[key])
        print d
