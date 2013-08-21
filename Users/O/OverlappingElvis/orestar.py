import scraperwiki
import mechanize
import re
from datetime import date, timedelta, datetime
import xlrd

currentdate = date.today()

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)

for i in range(0,3):
    data = []
    url = 'https://secure.sos.state.or.us/orestar/gotoPublicTransactionSearchResults.do?cneSearchButtonName=search&cneSearchFilerCommitteeId=*&cneSearchTranEndDate=' + date.strftime(currentdate, '%m/%d/%Y') + '&cneSearchTranStartDate=' + date.strftime(currentdate - timedelta(days=7), '%m/%d/%Y')
    print url
    br.open(url)
    xlsLink = br.follow_link(text_regex=r"Export To Excel Format")
    book = xlrd.open_workbook(file_contents=xlsLink.read())
    filings = book.sheet_by_index(0)
    for row in range(1, filings.nrows):
        datum = {
            "transaction_id" : filings.cell(row, 0).value,
            "original_id" : filings.cell(row, 1).value,
            "tran_date" : filings.cell(row, 2).value,
            "tran_status" : filings.cell(row, 3).value,
            "filer" : filings.cell(row, 4).value,
            "payee" : filings.cell(row, 5).value,
            "sub_type" : filings.cell(row, 6).value,
            "amount" : filings.cell(row, 7).value,
            "aggregate_amount" : filings.cell(row, 8).value,
            "payee_committe" : filings.cell(row, 9).value,
            "filer_id" : filings.cell(row, 10).value,
            "attest_by_name" : filings.cell(row, 11).value,
            "attest_date" : filings.cell(row, 12).value,
            "review_by_name" : filings.cell(row, 13).value,
            "review_date" : filings.cell(row, 14).value,
            "due_date" : filings.cell(row, 15).value,
            "occpn_ltr_date" : filings.cell(row, 16).value,
            "pymt_sched_txt" : filings.cell(row, 17).value,
            "purpose_description" : filings.cell(row, 18).value,
            "interest_rate" : filings.cell(row, 19).value,
            "check_number" : filings.cell(row, 20).value,
            "tran_stsfd_ind" : filings.cell(row, 21).value,
            "filed_by_name" : filings.cell(row, 22).value,
            "filed_date" : filings.cell(row, 23).value,
            "addr_book_agent_name" : filings.cell(row, 24).value,
            "book_type" : filings.cell(row, 25).value,
            "title_text" : filings.cell(row, 26).value,
            "occupation_text" : filings.cell(row, 27).value,
            "employer_name" : filings.cell(row, 28).value,
            "employer_city" : filings.cell(row, 29).value,
            "employer_state" : filings.cell(row, 30).value,
            "employer_ind" : filings.cell(row, 31).value,
            "self_employed" : filings.cell(row, 32).value,
            "addr_line_1" : filings.cell(row, 33).value,
            "addr_line_2" : filings.cell(row, 34).value,
            "city" : filings.cell(row, 35).value,
            "state" : filings.cell(row, 36).value,
            "zip" : filings.cell(row, 37).value,
            "zip_plus_4" : filings.cell(row, 38).value,
            "county" : filings.cell(row, 39).value,
            "purpose_codes" : filings.cell(row, 40).value,
            "exp_date" : filings.cell(row, 41).value
        }
        data.append(datum)
    currentdate = currentdate - timedelta(days=7)
    scraperwiki.sqlite.save(["transaction_id"], data)