import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




import scraperwiki
import json
import os

query_string = os.getenv("URLQUERY")

scraperwiki.sqlite.attach("outer_space_objects_parsecollector", "src")

sel = "State__Organization, count(1) as c, sum(CASE WHEN UN_Registered='No' THEN 1 ELSE 0 END) as nr"
res = scraperwiki.sqlite.execute("select %s from src.osobjects group by State__Organization order by c desc" % sel)

if query_string == "json":
    print json.dumps(res["data"])

else:
    print "<table>"
    print "<tr><th>Country</th><th>Number of objects</th><th>Number of not registered</th></tr>"
    print "\n".join(["<tr><td>%s</td><td>%d</td><td>%d</td></tr>" % tuple(cc)  for cc in res["data"]])
    print "</table>"




