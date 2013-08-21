# Blank Python
sourcescraper = 'my test scraper'
print "This is a <em>generated view</em> of HTML from <span style='color: blue;'><strong>swdata</strong></span> table <br/>of <span style='color: blue;'><strong>school_life_expectancy_in_years</strong></span> DB."    
import scraperwiki
scraperwiki.sqlite.attach("school_life_expectancy_in_years")
data = scraperwiki.sqlite.select(           
    '''* from school_life_expectancy_in_years.swdata 
    order by years_in_school desc limit 10'''
)
#print data
print "<table>"           
print "<tr><th>Country</th><th>Last polls year</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"