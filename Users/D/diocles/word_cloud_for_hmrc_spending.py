import scraperwiki
import string
import math
import locale

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT sum(Amount) FROM src.Refined WHERE Date >= ? and Date < ?", (start, end)).get("data")[0][0]
print "<h2>Total: &pound;%s</h2>" % locale.format('%d', int(totdata), True)

sdata = scraperwiki.sqlite.execute("SELECT Supplier, sum(Amount) FROM src.Refined WHERE Date >= ? and Date < ? GROUP BY Supplier", (start, end) ) 
#print sdata
keys = sdata.get("keys")
rows = sdata.get("data")

#print rows
for row in rows:
    try:
        print "<font size='%s' title='&pound;%s'>%s,</font>" % (math.log(row[1], 10), locale.format('%d', row[1], True), row[0])
    except Exception, ex:
        print "Error", eximport scraperwiki
import string
import math
import locale

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

sourcescraper = 'hmrc_spending'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET( )
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT sum(Amount) FROM src.Refined WHERE Date >= ? and Date < ?", (start, end)).get("data")[0][0]
print "<h2>Total: &pound;%s</h2>" % locale.format('%d', int(totdata), True)

sdata = scraperwiki.sqlite.execute("SELECT Supplier, sum(Amount) FROM src.Refined WHERE Date >= ? and Date < ? GROUP BY Supplier", (start, end) ) 
#print sdata
keys = sdata.get("keys")
rows = sdata.get("data")

#print rows
for row in rows:
    try:
        print "<font size='%s' title='&pound;%s'>%s,</font>" % (math.log(row[1], 10), locale.format('%d', row[1], True), row[0])
    except Exception, ex:
        print "Error", ex