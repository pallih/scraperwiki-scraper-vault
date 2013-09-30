import scraperwiki
import re
from datetime import date

# Blank Python
sourcescraper = 'hasler_marathon_results'

# The Hasler season runs from 1st September to 31st August each year. This gives the year in which the Hasler season for the given date finishes, i.e. when the finals are held.
def get_hasler_end_year(date):
    return int(date.year) if date.month < 9 else int(date.year + 1)

params = scraperwiki.utils.GET()

hasler_year = get_hasler_end_year(date.today()) if 'y' not in params else int(params['y'])
club = 'RIC' if 'c' not in params else params['c']

scraperwiki.sqlite.attach('hasler_marathon_club_list')
scraperwiki.sqlite.attach(sourcescraper)

query = "race_date, races.race_name as race_name, races.results_url as race_url, race_division, name_1 AS name, div_1 AS division, class_1 as class, name_2 AS partner_name, club_2 AS partner_club, position, time, retired, points_1 as points, p_d_1 as p_d from results INNER JOIN races ON races.results_url=results.race_name WHERE club_1='" + club + "' AND race_date LIKE '____-%' AND race_date >= '" + str(hasler_year-1) + "-09' AND race_date < '" + str(hasler_year) + "-09' AND races.race_name <> 'Hasler Final' AND time <> 'dsq' AND time <> 'dns' AND division LIKE 'U1??' UNION SELECT race_date, races.race_name as race_name, races.results_url as race_url, race_division, name_2 AS name, div_2 AS division, class_2 as class, name_1 AS partner_name, club_1 AS partner_club, position, time, retired, points_2 as points, p_d_2 as p_d from results INNER JOIN races ON races.results_url=results.race_name WHERE club_2='" + club + "' AND race_date LIKE '____-%' AND race_date >= '" + str(hasler_year-1) + "-09' AND race_date < '" + str(hasler_year) + "-09' AND races.race_name <> 'Hasler Final' AND time <> 'dsq' AND time <> 'dns' AND division LIKE 'U1??' ORDER BY name, race_date"

def ordinal_str(n):
    if n == '1':
        return "%sst" % (n)
    elif n == '2':
        return "%snd" % (n)
    elif n == '3':
        return "%srd" % (n)
    elif re.match('[0-9]+', n):
        return "%sth" % (n)
    else:
        return None

data = scraperwiki.sqlite.select(query)
clubdata = scraperwiki.sqlite.select("name, code FROM hasler_marathon_club_list.swdata")
people = []
k1num = {}
k2num = {}
races = {}
divs = {}
classes = {}
for row in data:
    name = row['name']
    if not name in people:
        people.append(name)
    
    raceurl = row['race_url'] if row['race_url'].startswith('http') else 'http://www.marathon-canoeing.org.uk/marathon/results/%s' % (row['race_url'])
    rd = '%s in %s at <a href="%s">%s</a>' % ((ordinal_str(row['position']) or ('rtd' if row['retired'] else '')), row['race_division'], raceurl, row['race_name'])
    if (row['partner_name']):
        rd += " (with %s)" % (row['partner_name'])
    if (row['p_d'] and len(row['p_d']) == 2):
        rd += " (%s)" % (row['p_d'])
    races[name] = races[name] if name in races else []
    races[name].append(rd)
    k1num[name] = k1num[name] if name in k1num else 0
    k2num[name] = k2num[name] if name in k2num else 0
    divs[name] = row['division']
    classes[name] = row['class']
    #if row['p_d'] and row['p_d'][0] in ['P', 'D']:
    #    divs[name] = row['p_d'][1:]
    # TODO check if paddler is racing in their current division? They do not get points otherwise.
    if (('_' in row['race_division'] and not row['race_division'].endswith('K1') and not row['race_division'].endswith('C1')) or row['race_division'].startswith('Hody') or row['race_division'].endswith('C2') or row['race_division'].endswith('K2') or row['race_division'] == 'Mixed'):
        k2num[name] += 1
    else:
        k1num[name] += 1

print """<html>
<head>
<title>Hasler Final Qualifications</title>
<style type="text/css">
body {
    font-family: arial, helvetica, sans-serif;
    font-size: 0.85em;
}
table {
    border-collapse: collapse;
}
table td, table th {
    font-size: 0.85em;
    border-bottom: 1px solid #999999;
    padding: 5px;
    text-align: left;
}
td.ok {
    background-color: #66cc66;
}
td.onemore {
    background-color: #cccc66;
}
</style>
</head>
<body>
"""

print "<h1>Hasler Final Qualifications</h1>\n"

print '<form action="." method="GET">'
print '<p>Club: <select name="c">'
for c in clubdata:
    print '<option value="%s"%s>%s</option>' % (c['code'], ' selected="selected"' if c['code'] == club else '', c['name'])
print '</select> <input type="submit" value="Go" name="_" />'
print '</form>'

print "<table>\n"
print "<tr><th>Name</th><th>Class</th><th>Division</th><th>Races (total)</th><th>Races (K1)</th><th>Results</th></tr>\n"
lastname = ''
nq = 0
nqk1 = 0
n = len(people)
for name in people:
    bar = 3 # Points needed to qualify
    if divs[name].startswith('U'):
        bar = 3
    elif classes[name] in ['S', 'SM', 'M', 'VM'] and int(divs[name]) == 1:
        bar = 2
    elif classes[name] in ['JM', 'J'] and int(divs[name]) <= 2:
        bar = 2
    elif classes[name] in ['F', 'VF'] and int(divs[name]) <= 3:
        bar = 2
    elif classes[name] == 'JF' and int(divs[name]) <= 4:
        bar = 2
    elif classes[name] in ['SC', 'C', 'VC', 'JC'] and int(divs[name]) <= 3: # Div 3 and above canoe
        bar = 2
    if (k1num[name] + k2num[name] >= bar):
        nq += 1
    if (k1num[name] >= bar):
        nqk1 += 1
    print "<tr\n>"
    print "<td>" + name + "</td>\n"
    print "<td>" + classes[name] + "</td>\n"
    print "<td>" + divs[name] + "</td>\n"
    print '<td class="' + ('onemore' if (k1num[name] + k2num[name] + 1 == bar) else ('ok' if (k1num[name] + k2num[name] >= bar) else '')) + '">' + str(k1num[name] + k2num[name]) + "</td>\n"
    print '<td class="' + ('onemore' if (k1num[name] + 1 == bar) else ('ok' if (k1num[name] >= bar) else '')) + '">' + (str(k1num[name]) if k1num[name] else '-') + "</td>\n"
    print "<td>" + '<br />'.join(races[name]) + "</td>\n"
    print "</td>\n"
    print "</tr>\n"
    lastname = row['name']
print "</table>\n"
print "<p>Total competitors: %d, Qualifiers: %d (%d%%), K1 Qualifiers: %d (%d%%)</p>" % (n, nq, nq*100/n, nqk1, nqk1*100/n)
print "</body></html>"