#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "european-community-fishing-fleet-register-codes"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 20000  
offset = 0

counts = { }
for row in getData(sourcescraper, limit, offset):
    country = row['Country']
    if country not in counts:
        counts[country] = { 'count':0, 'sumtonnage':0.0, 'sumpower':0.0 }
    cdata = counts[country]
    if row['Event_Code'] not in ['RET', 'DES', 'EXP']:
        cdata['count'] += 1
        cdata['sumtonnage'] += float(row['Gt_Tonnage'])
        cdata['sumpower'] += float(row['Main_Power'])
    

# Report on the types and ranges of values associated to each key
print '<h2>Fishing vessels per country</h2>'

print '''<p>Official stats for <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tsdnr420&plugin=0">Total engine power</a>, 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00116&plugin=0">Total number vessels</a>, and 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00083&plugin=0">Total fleet tonnage</a>.</p>'''

print '<table style="">'
print "<tr><th>Country</th><th>Number</th><th>Sum tonnage</th><th>Sum power</th></tr>"
for country, cdata in sorted(counts.items()):
    print "<tr><th>%s</th><td>%d</td><td>%.1f</td><td>%.1f</td></tr>" % (country, cdata['count'], cdata['sumtonnage'], cdata['sumpower'])
print "</table>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "european-community-fishing-fleet-register-codes"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 20000  
offset = 0

counts = { }
for row in getData(sourcescraper, limit, offset):
    country = row['Country']
    if country not in counts:
        counts[country] = { 'count':0, 'sumtonnage':0.0, 'sumpower':0.0 }
    cdata = counts[country]
    if row['Event_Code'] not in ['RET', 'DES', 'EXP']:
        cdata['count'] += 1
        cdata['sumtonnage'] += float(row['Gt_Tonnage'])
        cdata['sumpower'] += float(row['Main_Power'])
    

# Report on the types and ranges of values associated to each key
print '<h2>Fishing vessels per country</h2>'

print '''<p>Official stats for <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tsdnr420&plugin=0">Total engine power</a>, 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00116&plugin=0">Total number vessels</a>, and 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00083&plugin=0">Total fleet tonnage</a>.</p>'''

print '<table style="">'
print "<tr><th>Country</th><th>Number</th><th>Sum tonnage</th><th>Sum power</th></tr>"
for country, cdata in sorted(counts.items()):
    print "<tr><th>%s</th><td>%d</td><td>%.1f</td><td>%.1f</td></tr>" % (country, cdata['count'], cdata['sumtonnage'], cdata['sumpower'])
print "</table>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "european-community-fishing-fleet-register-codes"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 20000  
offset = 0

counts = { }
for row in getData(sourcescraper, limit, offset):
    country = row['Country']
    if country not in counts:
        counts[country] = { 'count':0, 'sumtonnage':0.0, 'sumpower':0.0 }
    cdata = counts[country]
    if row['Event_Code'] not in ['RET', 'DES', 'EXP']:
        cdata['count'] += 1
        cdata['sumtonnage'] += float(row['Gt_Tonnage'])
        cdata['sumpower'] += float(row['Main_Power'])
    

# Report on the types and ranges of values associated to each key
print '<h2>Fishing vessels per country</h2>'

print '''<p>Official stats for <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tsdnr420&plugin=0">Total engine power</a>, 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00116&plugin=0">Total number vessels</a>, and 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00083&plugin=0">Total fleet tonnage</a>.</p>'''

print '<table style="">'
print "<tr><th>Country</th><th>Number</th><th>Sum tonnage</th><th>Sum power</th></tr>"
for country, cdata in sorted(counts.items()):
    print "<tr><th>%s</th><td>%d</td><td>%.1f</td><td>%.1f</td></tr>" % (country, cdata['count'], cdata['sumtonnage'], cdata['sumpower'])
print "</table>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "european-community-fishing-fleet-register-codes"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 20000  
offset = 0

counts = { }
for row in getData(sourcescraper, limit, offset):
    country = row['Country']
    if country not in counts:
        counts[country] = { 'count':0, 'sumtonnage':0.0, 'sumpower':0.0 }
    cdata = counts[country]
    if row['Event_Code'] not in ['RET', 'DES', 'EXP']:
        cdata['count'] += 1
        cdata['sumtonnage'] += float(row['Gt_Tonnage'])
        cdata['sumpower'] += float(row['Main_Power'])
    

# Report on the types and ranges of values associated to each key
print '<h2>Fishing vessels per country</h2>'

print '''<p>Official stats for <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tsdnr420&plugin=0">Total engine power</a>, 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00116&plugin=0">Total number vessels</a>, and 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00083&plugin=0">Total fleet tonnage</a>.</p>'''

print '<table style="">'
print "<tr><th>Country</th><th>Number</th><th>Sum tonnage</th><th>Sum power</th></tr>"
for country, cdata in sorted(counts.items()):
    print "<tr><th>%s</th><td>%d</td><td>%.1f</td><td>%.1f</td></tr>" % (country, cdata['count'], cdata['sumtonnage'], cdata['sumpower'])
print "</table>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "european-community-fishing-fleet-register-codes"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 20000  
offset = 0

counts = { }
for row in getData(sourcescraper, limit, offset):
    country = row['Country']
    if country not in counts:
        counts[country] = { 'count':0, 'sumtonnage':0.0, 'sumpower':0.0 }
    cdata = counts[country]
    if row['Event_Code'] not in ['RET', 'DES', 'EXP']:
        cdata['count'] += 1
        cdata['sumtonnage'] += float(row['Gt_Tonnage'])
        cdata['sumpower'] += float(row['Main_Power'])
    

# Report on the types and ranges of values associated to each key
print '<h2>Fishing vessels per country</h2>'

print '''<p>Official stats for <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tsdnr420&plugin=0">Total engine power</a>, 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00116&plugin=0">Total number vessels</a>, and 
            <a href="http://epp.eurostat.ec.europa.eu/tgm/table.do?tab=table&init=1&language=en&pcode=tag00083&plugin=0">Total fleet tonnage</a>.</p>'''

print '<table style="">'
print "<tr><th>Country</th><th>Number</th><th>Sum tonnage</th><th>Sum power</th></tr>"
for country, cdata in sorted(counts.items()):
    print "<tr><th>%s</th><td>%d</td><td>%.1f</td><td>%.1f</td></tr>" % (country, cdata['count'], cdata['sumtonnage'], cdata['sumpower'])
print "</table>"

    