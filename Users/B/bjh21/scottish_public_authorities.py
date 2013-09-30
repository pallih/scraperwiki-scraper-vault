import scraperwiki
import csv
import codecs

fieldmap = {
    "Public Authority, with link to website where available": 'Name',
    "Schedule 1 Part No.": 'Schedule 1 Part',
    "Schedule 1 No.": 'Schedule 1 Paragraph'
}

uncp1252 = codecs.getdecoder('cp1252')

data = scraperwiki.scrape('http://www.itspublicknowledge.info/nmsruntime/logLink.asp?linkURL=http%3A%2F%2Fwww%2Eitspublicknowledge%2Einfo%2Fpdf%2Ephp%3Ftype%3Dcsv')
# scraperwiki.sqlite.execute('DELETE FROM swdata')
rdr = csv.DictReader(data.splitlines())
for row in rdr:
    newrow = { }
    for (key, val) in row.items():
        newrow[fieldmap.get(key, key)] = uncp1252(val)[0]
    scraperwiki.sqlite.save(['FK_ELEMENTID'], newrow)
import scraperwiki
import csv
import codecs

fieldmap = {
    "Public Authority, with link to website where available": 'Name',
    "Schedule 1 Part No.": 'Schedule 1 Part',
    "Schedule 1 No.": 'Schedule 1 Paragraph'
}

uncp1252 = codecs.getdecoder('cp1252')

data = scraperwiki.scrape('http://www.itspublicknowledge.info/nmsruntime/logLink.asp?linkURL=http%3A%2F%2Fwww%2Eitspublicknowledge%2Einfo%2Fpdf%2Ephp%3Ftype%3Dcsv')
# scraperwiki.sqlite.execute('DELETE FROM swdata')
rdr = csv.DictReader(data.splitlines())
for row in rdr:
    newrow = { }
    for (key, val) in row.items():
        newrow[fieldmap.get(key, key)] = uncp1252(val)[0]
    scraperwiki.sqlite.save(['FK_ELEMENTID'], newrow)
