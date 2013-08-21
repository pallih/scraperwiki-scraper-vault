import scraperwiki
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

sourcescraper = 'zeilboot_marktplaats'
database = "marktplaats"
scraperwiki.sqlite.attach(sourcescraper)
data = scraperwiki.sqlite.select("* from {0}.{1} where timestamp = (select max(timestamp) from {0}.{1})".format(sourcescraper, database) ) 
print("<html><body><table>")
for line in data:
    print("<tr><td><h1><a href='{4}'>{0}</a></h1><p>{1}</p></td><td>{2}</td><td><img src='{3}'/></td></tr>".format(line["title"], line["description"], line["price"], line["thumblink"], line["link"]))

print("</table></body></html>")
