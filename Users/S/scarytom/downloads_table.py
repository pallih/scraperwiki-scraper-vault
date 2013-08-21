# Blank Python

import scraperwiki
scraperwiki.sqlite.attach("ci-eye-downloads")
data = scraperwiki.sqlite.select( '''* from 'ci-eye-downloads'.swdata order by name desc''' )

print "<table>"
print "<tr><th>Title</th><th>URL</th>"

for d in data:
    print "<tr>"
    print "<td>", d["description"], "</td>"
    print "<td><a href='", d["html_url"], "'>", d["html_url"], "</a></td>"
    print "<td>", d["created_at"], "</td>"
    print "<td>", d["download_count"], "</td>"
    print "</tr>"

print "</table>"
