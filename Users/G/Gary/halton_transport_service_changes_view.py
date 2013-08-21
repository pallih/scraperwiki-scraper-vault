import scraperwiki
import re

scraperwiki.sqlite.attach('halton_transport_service_changes') 

blocks = scraperwiki.sqlite.select('* from `halton_transport_service_changes`.swdata')

print "<table style='border:2px solid grey; '>"

for block in blocks:
    if blocks.index(block) == 0:
        continue;
    else:
        result = re.findall('"><FONT SIZE="(.*?)"', block['block'])
        #print result[0]
        if result[0] == "4":
            print "<tr style='background-color:maroon; border:2px solid grey;'>"
            print "<td style='border:2px solid grey;'>" + block['block'] + "</td>"
            print "</tr>"
        elif result[0] == "3":
            print "<tr style='background-color:white; border:2px solid grey;'>"
            print "<td style='border:2px solid grey;'>" + block['block'] + "</td>"
            print "</tr>"

print "</table>"