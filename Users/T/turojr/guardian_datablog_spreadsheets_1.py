import scraperwiki
from collections import defaultdict

sourcescraper = 'guardian_datablog_posts'

print """
<html>
<head>
<title>Guardian Datablog Spreadsheets</title>
<style type="text/css">
#spreadsheets ul {
    list-style-type: none;
}
#spreadsheets ul, #spreadsheets li {
    margin: 0;
    padding: 0;
}
table {
    border-collapse:collapse;
}
table,th, td {
    border: 1px solid black;
}
td {
    padding: 0 2px;
}
</style>
</head>
<body>
<h1>Guardian Datablog Spreadsheets</h1>
<p>Google Spreadsheets from the <a href="http://www.guardian.co.uk/news/datablog">Guardian Datablog</a>, and posts which mention them.</p>
<h2>Notes</h2>
<ol>
<li>Some spreadsheets have a date of 'None' and a title of '(Unknown title)', because they were not accessible programmatically via the key used in the link.</li>
<li>The list of posts excludes the <a href="http://www.guardian.co.uk/news/datablog/2011/jan/27/data-store-office-for-national-statistics">list of all spreadsheets</a>. (I consider that spreadsheet less useful than this data, because it is both less clean and not up-to-date.)</li>
<li>Some spreadsheets have not been picked up because they were hidden behind a URL shortener.</li>
</ol>
<h2>Data</h2>
<table id="spreadsheets">
<tr>
<th style="width: 10%">Last Updated</th>
<th>Spreadsheet</th>
<th>Related Posts</th>
</tr>
"""

scraperwiki.sqlite.attach(sourcescraper)

posts = defaultdict(list)
titles = {}

data = scraperwiki.sqlite.select("* from posts")
for row in data:
    titles[row["url"]] = row["title"]

data = scraperwiki.sqlite.select('* from p_s where post_url != "http://www.guardian.co.uk/news/datablog/2011/jan/27/data-store-office-for-national-statistics"')
for row in data:
    posts[row["spreadsheet_key"]].append(row["post_url"])

data = scraperwiki.sqlite.select("date(updated) as updated_date, url, title, key from spreadsheets order by updated desc")
for row in data:
    output = """<tr><td>%s</td><td><a href="%s">%s</a></td><td><ul>""" % (row["updated_date"], row["url"], row["title"] or "(Unknown title)")

    for post in posts[row["key"]]:
        output += """<li><a href="%s">%s</a></li>""" % (post, titles[post])

    output += "</ul></td></tr>"
    print output

print """
</table>
</body>
</html>
"""