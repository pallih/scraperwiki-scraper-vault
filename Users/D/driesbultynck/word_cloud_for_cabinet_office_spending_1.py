import scraperwiki
import string
import math

sourcescraper = 'cabinet_office_spend_data'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET()
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT sum(Amount) FROM src.Refined WHERE Date >= '%s' and Date < '%s'" % (start, end)).get("data")[0][0]
c = '{:20,}'.format(int(totdata))
print "<h2>Total: &pound;%s</h2>" % c

sdata = scraperwiki.sqlite.execute("SELECT Supplier, sum(Amount) FROM src.Refined WHERE Date >= '%s' and Date < '%s' GROUP BY Supplier" % (start, end) ) 
#print sdata
keys = sdata.get("keys")
rows = sdata.get("data")

#print rows
for row in rows:
    try:
        print "<font size='%s' title='&pound;%s'>%s,</font>" % (math.log(row[1], 10), "{:20,.2f}".format(row[1]), row[0])
    except Exception, ex:
        print "Error", eximport scraperwiki
import string
import math

sourcescraper = 'cabinet_office_spend_data'
scraperwiki.sqlite.attach(sourcescraper, "src")

params = scraperwiki.utils.GET()
start = params.get("start", "0000-00-00")
end = params.get("end", "9999-99-99")

totdata = scraperwiki.sqlite.execute("SELECT sum(Amount) FROM src.Refined WHERE Date >= '%s' and Date < '%s'" % (start, end)).get("data")[0][0]
c = '{:20,}'.format(int(totdata))
print "<h2>Total: &pound;%s</h2>" % c

sdata = scraperwiki.sqlite.execute("SELECT Supplier, sum(Amount) FROM src.Refined WHERE Date >= '%s' and Date < '%s' GROUP BY Supplier" % (start, end) ) 
#print sdata
keys = sdata.get("keys")
rows = sdata.get("data")

#print rows
for row in rows:
    try:
        print "<font size='%s' title='&pound;%s'>%s,</font>" % (math.log(row[1], 10), "{:20,.2f}".format(row[1]), row[0])
    except Exception, ex:
        print "Error", ex