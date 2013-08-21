import scraperwiki.sqlite

SOURCESCRAPER = "hacker_news_management_summary"
LIMIT = 30

class HnRow(object):
    def __init__(self, author, num_comments, age, title, points, link, discussion):
        self.title = unicode(title)
        self.author = unicode(author)
        self.link = unicode(link)
        self.disclink = unicode(discussion)
        self.points = int(points)
        self.numcomments = num_comments
        self.age = unicode(age)

    def __str__(self):
        return """
            <tr>
                <td>%d</td>
                <td>%s</td>
                <td><a href='%s'>%s</a></td>
                <td><a href='%s'>%s comments</a></td>
                <td>%s</td>
            </td>
        """ % (self.points, self.author, self.link, self.title, self.disclink, self.numcomments, self.age)


scraperwiki.sqlite.attach(SOURCESCRAPER, "src")

sdata = scraperwiki.sqlite.execute("select * from src.swdata order by points desc limit ?", (LIMIT))
keys = sdata.get("keys")
rows = sdata.get("data")

headings = ["points", "author", "title", "comments", "age"]

print '<h2>%s (TOP %d)</h2>' % (SOURCESCRAPER.replace('_', ' ').upper(), LIMIT)
print '<table border="1" style="border-collapse:collapse;">'

# column headings
print "<tr>\n" + '\n'.join(["<th>%s</th>" % h for h in headings]) + "\n</tr>"

# rows
for row in rows:
    print unicode(HnRow(*row))

print "</table>\n<br />"
