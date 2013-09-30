import scraperwiki
from datetime import datetime, timedelta

# Blank Python
sourcescraper = 'tab_testing'
scraperwiki.sqlite.attach(sourcescraper)
query = "SELECT race_type, meeting_code, racing_code, race_number, race_time FROM {0}.swdata WHERE date = '{1}' ORDER BY race_time".format(sourcescraper,datetime.strftime(datetime.now() + timedelta(hours=11),format="%Y-%m-%d"))
data = scraperwiki.sqlite.execute(query)

print "<table>"           
print "<tr><th>Race Type</th><th>Meeting Code</th><th>Racing Code</th><th>Race Number</th><th>Race Time</th></tr>"
for d in data['data']:
    print "<tr>"
    for i in range(len(d)):
        print "<td>", d[i], "</td>"
    print "</tr>"
print "</table>"import scraperwiki
from datetime import datetime, timedelta

# Blank Python
sourcescraper = 'tab_testing'
scraperwiki.sqlite.attach(sourcescraper)
query = "SELECT race_type, meeting_code, racing_code, race_number, race_time FROM {0}.swdata WHERE date = '{1}' ORDER BY race_time".format(sourcescraper,datetime.strftime(datetime.now() + timedelta(hours=11),format="%Y-%m-%d"))
data = scraperwiki.sqlite.execute(query)

print "<table>"           
print "<tr><th>Race Type</th><th>Meeting Code</th><th>Racing Code</th><th>Race Number</th><th>Race Time</th></tr>"
for d in data['data']:
    print "<tr>"
    for i in range(len(d)):
        print "<td>", d[i], "</td>"
    print "</tr>"
print "</table>"