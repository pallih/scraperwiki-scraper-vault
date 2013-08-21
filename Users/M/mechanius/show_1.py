# Blank Python

#episode` text, `sender` text, `datum` text, `episodeguideurl` text, `start` text, `ende` text, `wochentag` text, `titel` text)
sourcescraper = 'fernsehserien_sendetermine_2'
import scraperwiki
scraperwiki.sqlite.attach("fernsehserien_sendetermine_2")
data = scraperwiki.sqlite.select(
    ''' * from fernsehserien_sendetermine_2.swdata
    ORDER BY episode DESC
    LIMIT 204'''
)
print "<table>"
#print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["episode"], "</td>"
    print "<td>", d["titel"], "</td>"
    print "<td>", d["start"],"-",d["ende"], "</td>"
    print "<td>", d["datum"], "</td>"
    uhrzeit=d["start"].replace(":","-")
    dd,mm,yy= d['datum'].split(".")
    yy = yy[2:]
    otrlink ="".join(["<a href=\"http://otrkeyfinder.com/?search=","The_Big_Bang_Theory_",yy , ".", mm , ".", dd,"_",uhrzeit,"+hq"+"&search.x=0&search.y=0&order=odn\">otr hq</a> "])
    print "<td>",  otrlink,  "</td>"
    print "</tr>"
print "</table>"

