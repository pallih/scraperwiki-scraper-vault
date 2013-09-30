import scraperwiki

sourcescraper = 'uk_government_business_plans'
scraperwiki.sqlite.attach("uk_government_business_plans")

count = scraperwiki.sqlite.select('''count(subaction_id) as ActionCount,datetime from Actions group by datetime ''')

print "<table>"
for rownum in count:
    print "<tr>"
    print "<td>" + rownum['datetime'] + '\t',
    print "<td>" + str(rownum['ActionCount'])

import scraperwiki

sourcescraper = 'uk_government_business_plans'
scraperwiki.sqlite.attach("uk_government_business_plans")

count = scraperwiki.sqlite.select('''count(subaction_id) as ActionCount,datetime from Actions group by datetime ''')

print "<table>"
for rownum in count:
    print "<tr>"
    print "<td>" + rownum['datetime'] + '\t',
    print "<td>" + str(rownum['ActionCount'])

