# Blank Python
sourcescraper = 'fernsehserien_sendetermine_himym_7'
import scraperwiki
scraperwiki.sqlite.attach("fernsehserien_sendetermine_himym_7")
data = scraperwiki.sqlite.select(
    ''' * from fernsehserien_sendetermine_himym_7.swdata
    WHERE Uhrzeit LIKE '22%' OR Uhrzeit LIKE '21%'
    ORDER BY NUMMER DESC
    LIMIT 11'''
)
print "<table>"
#print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Nummer"], "</td>"
    print "<td>", d["Titel"], "</td>"
    print "<td>", d["Uhrzeit"], "</td>"
    print "<td>", d["Datum"], "</td>"
    uhrzeit=d["Uhrzeit"].split("-")[0].replace(":","-")
    dd,mm,yy= d['Datum'].split(".")
    otrlink ="".join(["<a href=\"http://otrkeyfinder.com/?search=","How_I_Met_Your_Mother_",yy , ".", mm , ".", dd,"_",uhrzeit,"+hq"+"&search.x=0&search.y=0&order=odn\">otr hq</a> "])
    print "<td>",  otrlink,  "</td>"
    print "</tr>"
print "</table>"

# Blank Python
sourcescraper = 'fernsehserien_sendetermine_himym_7'
import scraperwiki
scraperwiki.sqlite.attach("fernsehserien_sendetermine_himym_7")
data = scraperwiki.sqlite.select(
    ''' * from fernsehserien_sendetermine_himym_7.swdata
    WHERE Uhrzeit LIKE '22%' OR Uhrzeit LIKE '21%'
    ORDER BY NUMMER DESC
    LIMIT 11'''
)
print "<table>"
#print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["Nummer"], "</td>"
    print "<td>", d["Titel"], "</td>"
    print "<td>", d["Uhrzeit"], "</td>"
    print "<td>", d["Datum"], "</td>"
    uhrzeit=d["Uhrzeit"].split("-")[0].replace(":","-")
    dd,mm,yy= d['Datum'].split(".")
    otrlink ="".join(["<a href=\"http://otrkeyfinder.com/?search=","How_I_Met_Your_Mother_",yy , ".", mm , ".", dd,"_",uhrzeit,"+hq"+"&search.x=0&search.y=0&order=odn\">otr hq</a> "])
    print "<td>",  otrlink,  "</td>"
    print "</tr>"
print "</table>"

