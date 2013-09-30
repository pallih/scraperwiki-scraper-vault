import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html
scraperwiki.sqlite.saveimport scraperwiki           
scraperwiki.sqlite.attach("school_life_expectancy_in_years")
data = scraperwiki.sqlite.select(           
    '''* from school_life_expectancy_in_years.swdata 
    order by years_in_school desc limit 10'''
)
print data
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"








import scraperwiki
html = scraperwiki.scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html
scraperwiki.sqlite.saveimport scraperwiki           
scraperwiki.sqlite.attach("school_life_expectancy_in_years")
data = scraperwiki.sqlite.select(           
    '''* from school_life_expectancy_in_years.swdata 
    order by years_in_school desc limit 10'''
)
print data
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"








