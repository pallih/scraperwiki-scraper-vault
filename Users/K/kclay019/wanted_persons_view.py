import scraperwiki 
scraperwiki.sqlite.attach("wanted_persons")
from lxml.etree import tostring
import StringIO

data = scraperwiki.sqlite.select( 
    '''* from wanted_persons.swdata desc limit 10'''
) 

print "<table>" 
print "<tr><th>Name</th><th>Alias</th></tr>"
print "<td>" 
for d in data:    
    print "<tr>" 
    print "<td>", d["name"], "</td>"
    print "<td>", d["alias"], "</td>" 
    print "</tr>"
print "</table>"


import scraperwiki 
scraperwiki.sqlite.attach("wanted_persons")
from lxml.etree import tostring
import StringIO

data = scraperwiki.sqlite.select( 
    '''* from wanted_persons.swdata desc limit 10'''
) 

print "<table>" 
print "<tr><th>Name</th><th>Alias</th></tr>"
print "<td>" 
for d in data:    
    print "<tr>" 
    print "<td>", d["name"], "</td>"
    print "<td>", d["alias"], "</td>" 
    print "</tr>"
print "</table>"


