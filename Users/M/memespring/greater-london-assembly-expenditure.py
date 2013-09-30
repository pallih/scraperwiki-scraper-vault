# <Rant>Clearly, these CSV's are produced by hand to an inconsistent standard!</Rant>

import urllib2,re,csv,urllib 
from BeautifulSoup import BeautifulSoup
from scraperwiki import sqlite
import scraperwiki.metadata
import pygooglechart
from collections import defaultdict
from datetime import datetime

def findHeaderLine(lines):
    for count, line in enumerate(lines):
        if 'Supplier,' in line or 'Vendor,' in line or 'Vendor ID,' in line:
            return count
    return None

def fixAmount(amount):
    currency = 'GBP'
    if not amount or amount == 'Amount Paid':
        return (0, currency)
    
    # rgrp 2010-12-23 we are assuming that '$' is not a typo but genuine
    # may be worth checking this
    if '$' in amount:
        currency = 'USD'
        
    amount = amount.replace(",", "")
    # rgrp 2010-12-22 - occasionally have ? e.g. ?3723997.02
    # for time being we just strip it (could add to description (or notes field)
    amount = amount.replace('?', '')
    # \xa3 is £ sign
    amount = amount.replace('\xa3', '')
    amount = amount.replace('$', '')
    if len(amount)>0 and amount[0] == '(' and amount[-1] == ')':
        fixedAmount = '-%s' % amount[1:-1]
        #print "Converting %s to %s" % (amount,fixedAmount)
        amount = fixedAmount
    return (float(amount), currency)

def fixDate(date):
    if date:
        try:
            return datetime.strptime(date, '%d %b %Y')
        except:
            return None
    return None

def tryGetColumn(row,column):
    try:
        return row[column].strip()
    except KeyError:
        return None

def Main():
    page = urllib2.urlopen("http://www.london.gov.uk/who-runs-london/greater-london-authority/expenditure-over-1000")
    soup = BeautifulSoup(page)
    for link in soup.html.body.findAll('a',{'href': re.compile(r'(csv)$')}):
        quotedLink = link['href'].replace(' ','%20')
        report = urllib2.urlopen(quotedLink).readlines()
        headerLine = findHeaderLine(report)
        reader = csv.DictReader(report[headerLine:])
    
        for rowNumber, row in enumerate(reader):
            #print row
            amount, currency = fixAmount(tryGetColumn(row,'Amount') or tryGetColumn(row,'Amount £') or tryGetColumn(row,'Amount Paid') or tryGetColumn(row, 'Amount\n\xa3') or tryGetColumn(row, 'Amount\n\x9c'))
            data = {
                    'link'        : quotedLink,
                    'rowNumber'   : rowNumber,
                    'supplier'    : tryGetColumn(row,'Supplier') or tryGetColumn(row,'Vendor') or tryGetColumn(row,'Vendor Name'),
                    'amount'      : amount,
                    'currency'    : currency,
                    'description' : tryGetColumn(row,'Expense Description') or tryGetColumn(row,'Expenditure Account Code Description'),
                    'docType'     : tryGetColumn(row,'Doc Type'),
                    'docNumber'   : tryGetColumn(row,'Doc No') or tryGetColumn(row,'SAP\nDocument No'),
                    'date'        : fixDate(tryGetColumn(row,'Date') or tryGetColumn(row,'Clearing \nDate'))
                    }
        
            if data['supplier'] and data['amount'] and data['description'] and data['amount']!='Amount Paid':
                sqlite.save(['link','date', 'amount', 'supplier'],data, date=data['date'])
            #else:
            #    print "Invalid row: %s" % row
Main()# <Rant>Clearly, these CSV's are produced by hand to an inconsistent standard!</Rant>

import urllib2,re,csv,urllib 
from BeautifulSoup import BeautifulSoup
from scraperwiki import sqlite
import scraperwiki.metadata
import pygooglechart
from collections import defaultdict
from datetime import datetime

def findHeaderLine(lines):
    for count, line in enumerate(lines):
        if 'Supplier,' in line or 'Vendor,' in line or 'Vendor ID,' in line:
            return count
    return None

def fixAmount(amount):
    currency = 'GBP'
    if not amount or amount == 'Amount Paid':
        return (0, currency)
    
    # rgrp 2010-12-23 we are assuming that '$' is not a typo but genuine
    # may be worth checking this
    if '$' in amount:
        currency = 'USD'
        
    amount = amount.replace(",", "")
    # rgrp 2010-12-22 - occasionally have ? e.g. ?3723997.02
    # for time being we just strip it (could add to description (or notes field)
    amount = amount.replace('?', '')
    # \xa3 is £ sign
    amount = amount.replace('\xa3', '')
    amount = amount.replace('$', '')
    if len(amount)>0 and amount[0] == '(' and amount[-1] == ')':
        fixedAmount = '-%s' % amount[1:-1]
        #print "Converting %s to %s" % (amount,fixedAmount)
        amount = fixedAmount
    return (float(amount), currency)

def fixDate(date):
    if date:
        try:
            return datetime.strptime(date, '%d %b %Y')
        except:
            return None
    return None

def tryGetColumn(row,column):
    try:
        return row[column].strip()
    except KeyError:
        return None

def Main():
    page = urllib2.urlopen("http://www.london.gov.uk/who-runs-london/greater-london-authority/expenditure-over-1000")
    soup = BeautifulSoup(page)
    for link in soup.html.body.findAll('a',{'href': re.compile(r'(csv)$')}):
        quotedLink = link['href'].replace(' ','%20')
        report = urllib2.urlopen(quotedLink).readlines()
        headerLine = findHeaderLine(report)
        reader = csv.DictReader(report[headerLine:])
    
        for rowNumber, row in enumerate(reader):
            #print row
            amount, currency = fixAmount(tryGetColumn(row,'Amount') or tryGetColumn(row,'Amount £') or tryGetColumn(row,'Amount Paid') or tryGetColumn(row, 'Amount\n\xa3') or tryGetColumn(row, 'Amount\n\x9c'))
            data = {
                    'link'        : quotedLink,
                    'rowNumber'   : rowNumber,
                    'supplier'    : tryGetColumn(row,'Supplier') or tryGetColumn(row,'Vendor') or tryGetColumn(row,'Vendor Name'),
                    'amount'      : amount,
                    'currency'    : currency,
                    'description' : tryGetColumn(row,'Expense Description') or tryGetColumn(row,'Expenditure Account Code Description'),
                    'docType'     : tryGetColumn(row,'Doc Type'),
                    'docNumber'   : tryGetColumn(row,'Doc No') or tryGetColumn(row,'SAP\nDocument No'),
                    'date'        : fixDate(tryGetColumn(row,'Date') or tryGetColumn(row,'Clearing \nDate'))
                    }
        
            if data['supplier'] and data['amount'] and data['description'] and data['amount']!='Amount Paid':
                sqlite.save(['link','date', 'amount', 'supplier'],data, date=data['date'])
            #else:
            #    print "Invalid row: %s" % row
Main()