#python

import mechanize
import re
from datetime import date, timedelta, datetime
import xlrd
import scraperwiki
#import sqlite3
#import pprint
#pp = pprint.PrettyPrinter()


committees = [12456, 15089] # smith, hales

keys = [
    "transaction_id",
    "original_id",
    "transaction_date",
    "transaction_status",
    "filer",
    "contributor_or_payee",
    "sub_type",
    "amount",
    "aggregate_amount",
    "payee_committe_id",
    "filer_id",
    "attest_by_name",
    "attest_date",
    "review_by_name",
    "review_date",
    "due_date",
    "occpn_ltr_date",
    "payment_schedule_txt",
    "purpose_description",
    "interest_rate",
    "check_number",
    "tran_stsfd_ind",
    "filed_by_name",
    "filed_date",
    "addr_book_agent_name",
    "book_type",
    "title_text",
    "occupation_text",
    "employer_name",
    "employer_city",
    "employer_state",
    "employer_ind",
    "self_employed",
    "addr_line_1",
    "addr_line_2",
    "city",
    "state",
    "zip",
    "zip_plus_4",
    "county",
    "purpose_codes",
    "exp_date"
    ]


agent = mechanize.Browser()
agent.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')]
agent.set_handle_robots(False)


# Fix date values
def prep(key, value):
    # return date in format closer to ISO 8601, which is more standard + easier for SQL searches
    if (key.endswith("_date") and len(value)):
        return datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
    else:
        return value


for committee_id in committees:

    transactions = []

    url = "https://secure.sos.state.or.us/orestar/cneSearch.do?cneSearchButtonName=search&cneSearchFilerCommitteeId=%d" % committee_id
    print "Visiting " + url
    agent.open(url)

    xls_link = agent.follow_link(text_regex=r"Export To Excel Format")
    sheet = xlrd.open_workbook(file_contents=xls_link.read()).sheet_by_index(0)
    #sheet = xlrd.open_workbook(file_contents= open('test-%d.xls' % committee_id).read()).sheet_by_index(0)

    #for row in range(1, 3):
    for row in range(1, sheet.nrows):
        transaction = dict ((k,v) for (k,v) in map(lambda x: (keys[x],prep(keys[x],sheet.cell(row,x).value)), range(len(keys))))
        transactions.append(transaction)

    #pp.pprint(transactions)
    scraperwiki.sqlite.save(["transaction_id"], transactions)
#python

import mechanize
import re
from datetime import date, timedelta, datetime
import xlrd
import scraperwiki
#import sqlite3
#import pprint
#pp = pprint.PrettyPrinter()


committees = [12456, 15089] # smith, hales

keys = [
    "transaction_id",
    "original_id",
    "transaction_date",
    "transaction_status",
    "filer",
    "contributor_or_payee",
    "sub_type",
    "amount",
    "aggregate_amount",
    "payee_committe_id",
    "filer_id",
    "attest_by_name",
    "attest_date",
    "review_by_name",
    "review_date",
    "due_date",
    "occpn_ltr_date",
    "payment_schedule_txt",
    "purpose_description",
    "interest_rate",
    "check_number",
    "tran_stsfd_ind",
    "filed_by_name",
    "filed_date",
    "addr_book_agent_name",
    "book_type",
    "title_text",
    "occupation_text",
    "employer_name",
    "employer_city",
    "employer_state",
    "employer_ind",
    "self_employed",
    "addr_line_1",
    "addr_line_2",
    "city",
    "state",
    "zip",
    "zip_plus_4",
    "county",
    "purpose_codes",
    "exp_date"
    ]


agent = mechanize.Browser()
agent.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))')]
agent.set_handle_robots(False)


# Fix date values
def prep(key, value):
    # return date in format closer to ISO 8601, which is more standard + easier for SQL searches
    if (key.endswith("_date") and len(value)):
        return datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
    else:
        return value


for committee_id in committees:

    transactions = []

    url = "https://secure.sos.state.or.us/orestar/cneSearch.do?cneSearchButtonName=search&cneSearchFilerCommitteeId=%d" % committee_id
    print "Visiting " + url
    agent.open(url)

    xls_link = agent.follow_link(text_regex=r"Export To Excel Format")
    sheet = xlrd.open_workbook(file_contents=xls_link.read()).sheet_by_index(0)
    #sheet = xlrd.open_workbook(file_contents= open('test-%d.xls' % committee_id).read()).sheet_by_index(0)

    #for row in range(1, 3):
    for row in range(1, sheet.nrows):
        transaction = dict ((k,v) for (k,v) in map(lambda x: (keys[x],prep(keys[x],sheet.cell(row,x).value)), range(len(keys))))
        transactions.append(transaction)

    #pp.pprint(transactions)
    scraperwiki.sqlite.save(["transaction_id"], transactions)
