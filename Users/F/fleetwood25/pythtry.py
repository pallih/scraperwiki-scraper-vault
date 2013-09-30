# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki
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
# Blank Python
import scraperwiki
html = scraperwiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
print html
import lxml.html
root = lxml.html.fromstring(html)
for tr in root.cssselect("table[align='left'] tr.tcont"):
    tds = tr.cssselect("td")
    data = {
      'country' : tds[0].text_content(),
      'years_in_school' : int(tds[4].text_content())
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
import scraperwiki
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
