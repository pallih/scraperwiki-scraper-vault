#sourcescraper = ''
import scraperwiki as sw

sw.sqlite.attach('school_life_expectancy_in_years')

data = sw.sqlite.select('''* from school_life_expectancy_in_years.swdata order by years_in_school desc limit 10''')
print data

print '<table>'
print '<tr><th>Country</th><th>Years in School</th>'
for d in data:
    print 