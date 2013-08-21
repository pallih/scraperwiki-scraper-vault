import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


import os
import urllib
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation


sourcescraper = "pfi-database"

limit = 200
offset = 0

cin = { }
cco = { }

memberkeys = [ 'advisors', 'banks', 'contractor', 'members', 'private_advisors', 'private_contractors' ]

pfis = [ ]
memberquery = os.getenv('URLQUERY')
if memberquery:
    memberquery = urllib.unquote_plus(memberquery[2:])
print memberquery


for i, row in enumerate(getData(sourcescraper, limit, offset)):

    if i <= 1:
        print row

    members = set()
    for k in memberkeys:
        try:
            members = members.union(eval(row.get(k, '[]')))
        except SyntaxError:
            pass
        except NameError:
            pass

    value = float(row.get('Capital_Value', 0))
    members = sorted(members)
    for member in members:
        if member not in cin:
            cin[member] = 0.0
            cco[member] = 0
        cin[member] += value
        cco[member] += 1

    if memberquery in members:
        pfis.append((row.get('pfinumber'), row.get('Project_Name')))

if pfis:
    print "<h2>%s has worked on </h2>" % memberquery
    print "<ul>"
    for pfi in pfis:
        print '<li><a href="http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s">%s</a></li>' % (urllib.quote_plus(pfi[0]), pfi[1])
    print "</ul>"

print "<h2>List of top PFI companies</h2>"

am = cin.items()
am.sort(key=lambda x: -x[1])
#print am[:10]

ac = cco.items()
ac.sort(key=lambda x: -x[1])
print "<table>"
for name, number in ac[:20]:
    print '<tr> <td><a href="?%s">%s</a></td> <td>%d</td> </tr>' % (urllib.urlencode({"a":name}), name, number)
print "</table>"


