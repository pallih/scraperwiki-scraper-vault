import scraperwiki
import urllib
import csv
import re
import datetime

def cleandict(headers, row):
    data = { }
    for key, value in zip(headers, row):
        if key in ["Amount in Sterling", "Amount"]:
            value = re.sub("[,\s]", "", value.strip())
            if value[0] == "£":
                value = value[1:]
            value = float(value)
        elif key in ["Date", "Date Paid"]:
            mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)", value)
            assert mdate, value
            value = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
        else:
            value = value.strip()
        data[key] = value
    return data


def AttemptCSVdataGet(name, rurl, rows):
        # find longest section 
    rowgroups = [ ]
    for r, row in enumerate(rows):
        if rowgroups and rowgroups[-1]["rowleng"] == len(row):
            rowgroups[-1]["last"] = r
        else:
            rowgroups.append({"rowleng":len(row), "first":r, "last":r})
    rowgroups.sort(key=lambda x: x["last"]-x["first"], reverse=True)
    if not rowgroups or len(rowgroups[0]) < 2:
        print "Skipping", name
        return

    s0, s1 = rowgroups[0]["first"], rowgroups[0]["last"]+1
    if rows[s0][-1] == "":
        s0 += 1
    if s0 and len(rows[s0-1]) >= 5 and "Amount" in rows[s0]:
        s0 -= 1
    headers = [ x.strip()  for x in rows[s0] ]
    ldata = [ ]
    for i in range(s0+1, s1):
        row = rows[i]
        data = cleandict(headers, row)
        data["i"] = i
        data["rurl"] = rurl
        ldata.append(data)
    try:
        scraperwiki.sqlite.save(["i", "rurl"], ldata, name)
    except scraperwiki.sqlite.SqliteError:
        print "bad data"
        print rowgroups


scraperwiki.sqlite.attach("datagov_links_health")
sql = "Name, rurl, `Published via` as publisher from resources left join dataset on dataset.sourceurl=resources.sourceurl limit ? offset ?"

limit = 10
for n in range(100):
    if n < 21:
        continue
    print "Working on:", n
    recs = scraperwiki.sqlite.select(sql, (limit, n*limit))
    for rec in recs:
        txt = urllib.urlopen(rec["rurl"]).read()
        if re.search("(?i)<html", txt[:300]):
            print "skipping html link", rec
            continue
        if re.match("%PDF", txt[:100]):
            print "skipping pdf link", rec
            continue 

        try:
            AttemptCSVdataGet(rec["Name"], rec["rurl"], list(csv.reader(txt.split("\n"))))
        except Exception, e:
            print e
            print txt

import scraperwiki
import urllib
import csv
import re
import datetime

def cleandict(headers, row):
    data = { }
    for key, value in zip(headers, row):
        if key in ["Amount in Sterling", "Amount"]:
            value = re.sub("[,\s]", "", value.strip())
            if value[0] == "£":
                value = value[1:]
            value = float(value)
        elif key in ["Date", "Date Paid"]:
            mdate = re.match("(\d\d)/(\d\d)/(\d\d\d\d)", value)
            assert mdate, value
            value = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
        else:
            value = value.strip()
        data[key] = value
    return data


def AttemptCSVdataGet(name, rurl, rows):
        # find longest section 
    rowgroups = [ ]
    for r, row in enumerate(rows):
        if rowgroups and rowgroups[-1]["rowleng"] == len(row):
            rowgroups[-1]["last"] = r
        else:
            rowgroups.append({"rowleng":len(row), "first":r, "last":r})
    rowgroups.sort(key=lambda x: x["last"]-x["first"], reverse=True)
    if not rowgroups or len(rowgroups[0]) < 2:
        print "Skipping", name
        return

    s0, s1 = rowgroups[0]["first"], rowgroups[0]["last"]+1
    if rows[s0][-1] == "":
        s0 += 1
    if s0 and len(rows[s0-1]) >= 5 and "Amount" in rows[s0]:
        s0 -= 1
    headers = [ x.strip()  for x in rows[s0] ]
    ldata = [ ]
    for i in range(s0+1, s1):
        row = rows[i]
        data = cleandict(headers, row)
        data["i"] = i
        data["rurl"] = rurl
        ldata.append(data)
    try:
        scraperwiki.sqlite.save(["i", "rurl"], ldata, name)
    except scraperwiki.sqlite.SqliteError:
        print "bad data"
        print rowgroups


scraperwiki.sqlite.attach("datagov_links_health")
sql = "Name, rurl, `Published via` as publisher from resources left join dataset on dataset.sourceurl=resources.sourceurl limit ? offset ?"

limit = 10
for n in range(100):
    if n < 21:
        continue
    print "Working on:", n
    recs = scraperwiki.sqlite.select(sql, (limit, n*limit))
    for rec in recs:
        txt = urllib.urlopen(rec["rurl"]).read()
        if re.search("(?i)<html", txt[:300]):
            print "skipping html link", rec
            continue
        if re.match("%PDF", txt[:100]):
            print "skipping pdf link", rec
            continue 

        try:
            AttemptCSVdataGet(rec["Name"], rec["rurl"], list(csv.reader(txt.split("\n"))))
        except Exception, e:
            print e
            print txt

