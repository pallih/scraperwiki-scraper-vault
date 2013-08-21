import scraperwiki           
scraperwiki.sqlite.attach("hertz-freerider")

data = scraperwiki.sqlite.select('''* from [hertz-freerider].swdata''')

print "<html><head><title>freerider-view</title></head>"
print "<body><table>"
for d in data:
    print "<tr>"
    #print "<td>", d["when"], "</td>"
    print "<td>", d["row"], "</td>"
    print "</tr>"
print "</table></body></html>"

