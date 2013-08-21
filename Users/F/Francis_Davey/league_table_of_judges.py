# Blank Python
import scraperwiki

sourcescraper = 'uk-supreme-court-cases'
scraperwiki.sqlite.attach(sourcescraper)

data = scraperwiki.sqlite.select('''judge, count(case_id) as ncases from 'uk-supreme-court-cases'.normalized_judges group by judge order by ncases desc''')
print('''
<p>This table shows the number of cases listed against a judge's name at <a href="http://www.supremecourt.gov.uk/current-cases/index.html">the Supreme Court list of decided cases</a>.</p>''')

print('''<table>''')
for row in data:
    print('''<tr><td>{judge}</td><td>{ncases}</td></tr>'''.format(**row))
print('''</table>''')