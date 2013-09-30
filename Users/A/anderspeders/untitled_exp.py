import scraperwiki

import scraperwiki
html = scraperwiki.scrape("http://ec.europa.eu/transparency/regexpert/search_results_members.cfm")
print html


import lxml.html root = lxml.html.fromstring(html) 

for tr in root.cssselect("div[align='left'] tr.tcont"): tds = tr.cssselect("td") data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) } 

print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


print data
scraperwiki.sqlite.save(unique_keys=['country'], data=data)


import scraperwiki

import scraperwiki
html = scraperwiki.scrape("http://ec.europa.eu/transparency/regexpert/search_results_members.cfm")
print html


import lxml.html root = lxml.html.fromstring(html) 

for tr in root.cssselect("div[align='left'] tr.tcont"): tds = tr.cssselect("td") data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) } 

print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"


print data
scraperwiki.sqlite.save(unique_keys=['country'], data=data)


