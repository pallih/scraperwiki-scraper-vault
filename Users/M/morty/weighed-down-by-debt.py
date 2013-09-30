import scraperwiki
import itertools

employed_population_data = list(scraperwiki.datastore.getData('historic-populations'))
balance_data = list(scraperwiki.datastore.getData('balance-sheets'))
obesity_data = list(scraperwiki.datastore.getData('who-obesity-data'))

countries = set(x['country'] for x in employed_population_data) & set(x['country'] for x in balance_data) & set(x['country'] for x in obesity_data)

year_list  = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008']

print """
<html>
<head>
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.flot.js"></script>
<script type="text/javascript">

var ticks = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008'];
"""

for c in sorted(countries):
    print "var %s_debt = new Array();" % c
    print "var %s_obesity = new Array();" % c

for country, years in itertools.groupby(balance_data, lambda x: x['country']):
    print "country = %s" % country
    print list(years)
    if country not in countries:
        continue
    for year in years:
        print "%s_debt.push([%s, %s]);" % (country, year_list.index(year['year']), year['balance'])

import sys
sys.exit()

for c in sorted(countries):
    print """
        $.plot($("#%s-graph"), [
        {
            data: %s_debt, 
            label: 'Debt',
            lines: { show: true },
            points: { show: true }
        },
        {
            data: %s_obesity, 
            label: 'obesity',
            lines: { show: true },
            points: { show: true }
        }],
        {
          xaxis: {
              ticks: ticks
          }
        });
    """ % (c.lower(), c, c)

print """
</script>
</head>
<body>
"""

for c in sorted(countries):
    print "<h1>%s</h1>" % c
    print "<div id='%s-graph'/>" % c.lower()

print """
</body>
</html>
"""
import scraperwiki
import itertools

employed_population_data = list(scraperwiki.datastore.getData('historic-populations'))
balance_data = list(scraperwiki.datastore.getData('balance-sheets'))
obesity_data = list(scraperwiki.datastore.getData('who-obesity-data'))

countries = set(x['country'] for x in employed_population_data) & set(x['country'] for x in balance_data) & set(x['country'] for x in obesity_data)

year_list  = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008']

print """
<html>
<head>
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.flot.js"></script>
<script type="text/javascript">

var ticks = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008'];
"""

for c in sorted(countries):
    print "var %s_debt = new Array();" % c
    print "var %s_obesity = new Array();" % c

for country, years in itertools.groupby(balance_data, lambda x: x['country']):
    print "country = %s" % country
    print list(years)
    if country not in countries:
        continue
    for year in years:
        print "%s_debt.push([%s, %s]);" % (country, year_list.index(year['year']), year['balance'])

import sys
sys.exit()

for c in sorted(countries):
    print """
        $.plot($("#%s-graph"), [
        {
            data: %s_debt, 
            label: 'Debt',
            lines: { show: true },
            points: { show: true }
        },
        {
            data: %s_obesity, 
            label: 'obesity',
            lines: { show: true },
            points: { show: true }
        }],
        {
          xaxis: {
              ticks: ticks
          }
        });
    """ % (c.lower(), c, c)

print """
</script>
</head>
<body>
"""

for c in sorted(countries):
    print "<h1>%s</h1>" % c
    print "<div id='%s-graph'/>" % c.lower()

print """
</body>
</html>
"""
