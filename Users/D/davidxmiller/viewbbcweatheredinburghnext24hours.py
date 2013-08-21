import scraperwiki
scraperwiki.sqlite.attach("test_83")

data = scraperwiki.sqlite.select(
    '''time as time, summary as summary, temp_max_c as temp_max_c, winddir as winddir, windspeed as windspeed from swdata ORDER BY id'''
)

print "<table>"
print "<tr><th>Time</th><th>Summary</th><th>Wind Direction</th><th>Wind Speed</th>"
for d in data:
    print "<tr>"
    print "<td>", d["time"], "</td>"
    print "<td>", d["summary"], "</td>"
    print "<td>", d["winddir"], "</td>"
    print "<td>", d["windspeed"], "</td>"
    print "</tr>"
print "</table>"
