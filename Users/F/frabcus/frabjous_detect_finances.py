import scraperwiki
import re

scraperwiki.sqlite.attach("frabjous_pdf_to_database", "src")

v = [ ]
offset = 0
offsetstep = 1500
while True:
    tdata = scraperwiki.sqlite.execute("select text, hid from line limit %d offset %d" % (offsetstep, offset))["data"]
    ldata = [ ]
    print offset, tdata[:1]
    for text, hid in tdata:
        for m in re.finditer("(\xa3\s*)?(\d[\d\,\.]+)([mk]?)", text):
            data = { "hid":hid, "start":m.start(0), "end":m.end(0) }
            if m.group(1):
                data["currency"] = "pounds"
            try:
                data["value"] = float(m.group(2).replace(",", ""))
            except ValueError:
                print text
                continue
            if m.group(3) == "m":
                data["units"] = 1000000
            if m.group(3) == "k":
                data["units"] = 1000
            ldata.append(data)
    scraperwiki.sqlite.save(["hid", "start"], ldata)
    
    if len(tdata) != offsetstep:
        break
    offset += offsetstep
    
#[u'pdfurl', u'text', u'top', u'height', u'width', u'hid', u'page', u'fontid', u'left']
import scraperwiki
import re

scraperwiki.sqlite.attach("frabjous_pdf_to_database", "src")

v = [ ]
offset = 0
offsetstep = 1500
while True:
    tdata = scraperwiki.sqlite.execute("select text, hid from line limit %d offset %d" % (offsetstep, offset))["data"]
    ldata = [ ]
    print offset, tdata[:1]
    for text, hid in tdata:
        for m in re.finditer("(\xa3\s*)?(\d[\d\,\.]+)([mk]?)", text):
            data = { "hid":hid, "start":m.start(0), "end":m.end(0) }
            if m.group(1):
                data["currency"] = "pounds"
            try:
                data["value"] = float(m.group(2).replace(",", ""))
            except ValueError:
                print text
                continue
            if m.group(3) == "m":
                data["units"] = 1000000
            if m.group(3) == "k":
                data["units"] = 1000
            ldata.append(data)
    scraperwiki.sqlite.save(["hid", "start"], ldata)
    
    if len(tdata) != offsetstep:
        break
    offset += offsetstep
    
#[u'pdfurl', u'text', u'top', u'height', u'width', u'hid', u'page', u'fontid', u'left']
