import urllib2
from lxml.html import fromstring, tostring
import scraperwiki
import re, datetime


headers = ['Borrower', 'Date', 'Amount_of_Advance', 'Final_Maturity', 'Interest_Rate', "Interest_type"]

def parseTable(table, url, year):
    rows = table.cssselect('tr')
    cols0 = rows[0].cssselect('td, th')
    lheaders0 = [ th.text_content()  for th in cols0 ]
    assert lheaders0 == ['', '', 'Amount', 'Final', 'Interest']
    cols1 = rows[1].cssselect('td, th')
    lheaders1 = [ th.text_content().strip(" \n=20")  for th in cols1 ]
    assert lheaders1 == ['Borrower', 'Date', 'of Advance', 'Maturity', 'Rate'], lheaders1
    cols2 = rows[2].cssselect('td, th')
    assert len(cols2) == 0, cols2

    ldata = [ ]
    debttype = None
    department = None
    rowcount = 1
    for row in rows[3:]:
        cols = row.cssselect('td, th')
        if len(cols) == 1:
            if cols[0].tag == 'th':
                debttype = cols[0].text_content().strip()
                department = None
                assert debttype in [ 'AGENCY DEBT', 'GOVERNMENT-GUARANTEED LOANS'], [debttype]
            else:
                assert debttype
                department = cols[0].text_content().strip()
        elif len(cols) == 0:
            pass
        else:
            assert len(cols) == 6
            data = dict(zip(headers, [ td.text_content()  for td in cols ]))
            assert debttype and department
            data["department"] = department
            data["debttype"] = debttype
            data["url"] = url
            data["rowcount"] = rowcount
            rowcount += 1
            assert data["Amount_of_Advance"][0] == '$', data
            data["Amount_of_Advance"] = float(data["Amount_of_Advance"][1:].replace(",", ""))
            assert data["Interest_Rate"][-1] == "%", data
            data["Interest_Rate"] = float(data["Interest_Rate"][:-1])
            mdatem = re.match("(\d+)/(\d+)/(\d\d)", data["Final_Maturity"])
            assert mdatem, data
            y1 = int(mdatem.group(3))
            assert y1 < 90, data
            data["Final_Maturity"] = datetime.date(y1+2000, int(mdatem.group(1)), int(mdatem.group(2)))
            mdate = re.match("(\d+)/(\d+)$", data["Date"])
            assert mdate, data
            data["Date"] = datetime.date(year, int(mdate.group(1)), int(mdate.group(2)))
            if data["Borrower"][0] == '*':
                data["Borrower"] = data["Borrower"][1:]
            ldata.append(data)
    scraperwiki.sqlite.save(["url", "rowcount"], ldata, "borrowings")


for year in range(2008, 2012):
    for month in range(1, 13):
        url = "http://www.treasury.gov/ffb/press_releases/%d/%02d-%d.shtml" % (year, month, year)
        html = urllib2.urlopen(url).read()
        root = fromstring(html)
        tables = root.cssselect("table")
        ltable = None
        for table in tables:
            if table.cssselect("table table"):
                continue
            sth = " ".join([ th.text_content()  for th in table.cssselect("th") ])
            if "Amount Final Interest Borrower Date of Advance Maturity Rate" in sth and \
               "Net Change Net Change Program" not in sth:
                ltable = table
                print sth
                break
        try:
            parseTable(ltable, url, year)
        except Exception, e:
            print e








