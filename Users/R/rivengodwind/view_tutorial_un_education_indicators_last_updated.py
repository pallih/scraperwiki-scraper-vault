# View Tutorial for Scraperwiki, second of the series
sourcescraper = ''

import scraperwiki

# Attach data store
scraperwiki.sqlite.attach("un_education_indicators_years_of_schooling")

# Perform an SQLite query
data = scraperwiki.sqlite.select(           
    '''* from un_education_indicators_years_of_schooling.swdata 
    order by years_in_school desc limit 10'''
)

# Output HTML
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"
# View Tutorial for Scraperwiki, second of the series
sourcescraper = ''

import scraperwiki

# Attach data store
scraperwiki.sqlite.attach("un_education_indicators_years_of_schooling")

# Perform an SQLite query
data = scraperwiki.sqlite.select(           
    '''* from un_education_indicators_years_of_schooling.swdata 
    order by years_in_school desc limit 10'''
)

# Output HTML
print "<table>"
print "<tr><th>Country</th><th>Years in school</th>"
for d in data:
    print "<tr>"
    print "<td>", d["country"], "</td>"
    print "<td>", d["years_in_school"], "</td>"
    print "</tr>"
print "</table>"
