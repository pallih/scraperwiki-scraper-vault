#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import smtplib

sender = 'baga1014@mit.edu'
receivers = ['haowei@mit.edu']

message = """From: From Person <haowei@mit.edu>
To: To Person <b94901129@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
    smtpObj = smtplib.SMTP('hinet.net')
    smtpObj.sendmail(sender, receivers, message)         
    print "Successfully sent email"
except:
    print "fail"

sourcescraper = "uk_party_political_donations_parsecollector"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(keys))
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in rows:
    print "<tr>",
    for value in row:
        print "<td>%s</td>" % value,
    print "</tr>"
    
print "</table>"
#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki.sqlite
import smtplib

sender = 'baga1014@mit.edu'
receivers = ['haowei@mit.edu']

message = """From: From Person <haowei@mit.edu>
To: To Person <b94901129@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
    smtpObj = smtplib.SMTP('hinet.net')
    smtpObj.sendmail(sender, receivers, message)         
    print "Successfully sent email"
except:
    print "fail"

sourcescraper = "uk_party_political_donations_parsecollector"
limit = 20
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata limit ? offset ?", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

print '<h2>Some data from scraper: %s  (%d columns)</h2>' % (sourcescraper, len(keys))
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>",
for key in keys:
    print "<th>%s</th>" % key,
print "</tr>"

# rows
for row in rows:
    print "<tr>",
    for value in row:
        print "<td>%s</td>" % value,
    print "</tr>"
    
print "</table>"
