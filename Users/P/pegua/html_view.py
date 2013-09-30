sourcescraper = 'augusto_raw'

import scraperwiki            

scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select('''* from swdata''' ) 

print "<table>"            
print "<tr><th>Complete Address</th><tr>" 
for d in data:     
    print "<tr>"     
    print "<td> <a href=\"", d["complete_address"], "\">",d["complete_address"]  , "</a> </td>"     
    print "</tr>" 
print "</table>"
sourcescraper = 'augusto_raw'

import scraperwiki            

scraperwiki.sqlite.attach(sourcescraper)


data = scraperwiki.sqlite.select('''* from swdata''' ) 

print "<table>"            
print "<tr><th>Complete Address</th><tr>" 
for d in data:     
    print "<tr>"     
    print "<td> <a href=\"", d["complete_address"], "\">",d["complete_address"]  , "</a> </td>"     
    print "</tr>" 
print "</table>"
