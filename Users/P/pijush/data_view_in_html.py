import scraperwiki

# Blank Python

#print "This is a <em>fragment</em> of HTML."
import scraperwiki
scraperwiki.sqlite.attach("read_html_by_xml")
data = scraperwiki.sqlite.select(
    '''* from read_html_by_xml.swdata 
    order by Year desc limit 10'''
)
#print data
 data1=scraperwiki.sqlite.show_tables("read_html_by_xml")
print data1
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["Year"], "</td>"
    print "</tr>"
print "</table>"
