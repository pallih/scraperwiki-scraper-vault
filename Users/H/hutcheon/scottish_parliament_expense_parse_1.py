import scraperwiki
import lxml.html
import datetime
import datetime
import re


#scraperwiki.sqlite.execute("drop table if exists swdata")

def ParseTransaction(transactionref, rows):
    if not (len(rows) == 2 and rows[0][0][0][0].tag == "table" and len(rows[1]) == 0):
        for tr in rows:
            print lxml.html.tostring(tr)
        print len(rows), rows[0][0][0].tag, len(rows[1])
        assert False
        return [ ]

    ttable = rows[0][0][0][0]
    headers = [ td[0].text  for td in ttable[0] ]
    if headers == [u'Additional\xc2\xa0Info']:
        for td in ttable[1:]:
            assert not ttable[1][0].text.strip(), [ lxml.html.tostring(ltd)  for ltd in ttable ]
        return [ ]
    assert headers == ['Date', 'Description', 'No. of Miles', 'Amount'], headers
    rows = ttable[1:]
    ltdata = [ ]
    i = 1
    while rows:
        #print lxml.html.tostring(rows[0])
        if len(rows[0]) != 4:
            #print lxml.html.tostring(rows[0])
            assert len(rows[0]) == 1  # continuation, these tables are pagenated!
            break
        tr = rows.pop(0)
        assert len(tr[0]) == 0
        values = [ tr[0].text ]
        for td in tr[1:]:
            assert td[0].tag == "span"
            values.append(td[0].text)
        data = dict(zip(headers, values))

        assert data["Amount"][:2] == u'\xc2\xa3'
        data["Amount"] = float(data["Amount"][2:])
        data["Number miles"] = int(data.pop("No. of Miles"))
        mdate = re.match("(\d+)/(\d+)/(\d+)", data["Date"])
        assert mdate
        data["Date"] = datetime.date(int(mdate.group(3)), int(mdate.group(1)), int(mdate.group(2)))
        data["rownumber"] = i
        data['Transaction Ref'] = transactionref
        ltdata.append(data)
        i += 1
    return ltdata

def ParsePage(memberpage):
    root = lxml.html.fromstring(memberpage)
    data = { }
    table = root.cssselect("table")[0]
    assert len(table[0]) == 1, lxml.html.tostring(root)
    rows = table[1:]
    while rows:
        tr = rows.pop(0)
        if len(tr) == 1:
            break
        assert len(tr) == 4, lxml.html.tostring(table)
        for i in [0, 2]:
            if len(tr[i]) == 1:
                assert type(tr[i][0]) == lxml.html.HtmlComment, lxml.html.tostring(tr)
                assert len(tr[i+1]) == 1 and type(tr[i+1][0]) == lxml.html.HtmlComment, lxml.html.tostring(tr)
                continue
            assert len(tr[i]) == 0, (type(tr[i][0]), type(tr[i].tag), type(tr[i][0].tag), tr[i][0].tag())
            key = re.sub(u"\xa0", " ", tr[i].text).strip()
            assert len(tr[i+1]) == 1 and tr[i+1][0].tag == "span" and len(tr[i+1][0]) == 0, lxml.html.tostring(tr)
            #print lxml.html.tostring(tr[i+1][0])
            val = (tr[i+1][0].text or "").strip()
            data[key] = val

    assert data.keys() == [u'Claim Month', u'Transaction Ref.', u'Member', 'Payee', 'Amount', u'Expenditure Type', u'Allowance Type'], data
    data["Transaction Ref"] = data.pop("Transaction Ref.")
    assert data["Amount"][:2] == u'\xc2\xa3'
    data["Amount"] = float(data["Amount"][2:].replace(",", ""))

    tdata = ParseTransaction(data["Transaction Ref"], rows)

    return data, tdata


scraperwiki.sqlite.attach("scottish_parliament_expense_scrape", "src")
count = scraperwiki.sqlite.select("count(*) as count from src.swdata")[0]["count"]
print count
limit = 100
for offset in range(0, count, limit):
    print offset, "of", count
    ldata = [ ]
    ltdata = [ ]
    for row in scraperwiki.sqlite.select("`Member Name`, memberpage from src.swdata where yearitem='2007' limit ? offset ?", (limit, offset)):
        data, tdata = ParsePage(row["memberpage"])
        ldata.append(data)
        ltdata.extend(tdata)
    scraperwiki.sqlite.save(['Transaction Ref'], data=ldata)
    scraperwiki.sqlite.save(['Transaction Ref', "rownumber"], data=ltdata, table_name="miles")
