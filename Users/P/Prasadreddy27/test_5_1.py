# Blank Python
sourcescraper = 'Prasad / Test for Scrapper'

print "This is a <em>100 Scientists who shaped worlds history</em> of HTML."
import scraperwiki
#attaching the database to the scrper
scraperwiki.sqlite.attach("testtest_10")
#Query t retireve the data from table
#retrieves sno, name and investigated item to the data list
data = scraperwiki.sqlite.select(
    '''sno, name, investigated from testtest_10.swdata '''
)
# printing the data for testing
print data
#Creating the table to make a table format
#This table can be used in HTML page and can be printed
#table element
print "<table>"
#Table Column Headrers
print "<tr><th>sno</th><th>name</th><th>Investigated</th>"
#Looping for each row
for d in data:
  print "<tr>"
#serial number column data
  print "<td>", d["sno"], "</td>"
#name column data
  print "<td>", d["name"], "</td>"
#invetigation column data
  print "<td>", d["investigated"], "</td>"
#End of row
  print "</tr>"
#End of table
print "</table>"
