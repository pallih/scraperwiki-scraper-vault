# Blank Python
sourcescraper = 'surf-scheveningen'

import scraperwiki    
import datetime
import dateutil.parser           
       
scraperwiki.sqlite.attach("surf-scheveningen")

data = scraperwiki.sqlite.select(
    '''* FROM "swdata" 
    WHERE waveheight>0.6
    AND pctswell>70
    AND dayLight=1
    ORDER BY datetime'''
)

if data:
    print "Mogelijke surfuurtjes binnenkort:"
    print '''<table width="100%" cellpadding="1">'''
    print '''<tr align="left"><th>Datum</th><th>Tijd</th><th>Pct Swell</th><th>Golfhoogte</th><th>Wind (bft)</th></tr>'''
    for d in data:
        print "<tr>"
        print "<td>", dateutil.parser.parse(d["datetime"]).date(), "</td>"
        print "<td>", dateutil.parser.parse(d["datetime"]).time(), "</td>"
        print "<td>", d["pctswell"], "</td>"
        print "<td>", d["waveheight"], "</td>"
        print "<td>", d["Bft"], "</td>"
        print "</tr>"
    print "</table>"
else:
    print "Helaas geen surf in de komende 3 dagen.... :-("