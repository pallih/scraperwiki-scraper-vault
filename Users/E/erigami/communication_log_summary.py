import scraperwiki as sw
import time
import urllib
import cgi


sw.sqlite.attach('communication_log')

# Basic counts
data = sw.sqlite.select('count(*) AS c FROM contact')
print 'Contacts: %s<br/>' % data[0]['c']

data = sw.sqlite.select('* FROM contact WHERE error<>0')
print 'Errors: %s<br/>' % len(data)
if len(data) > 0:
    for row in data:
        print 'Error %s: <a href="%s">%s</><br/>' % (row['contact_id'], row['uri'], row['uri'])
    print '<hr/>'

data = sw.sqlite.select('count(*) AS c FROM victim')
print 'Lobbied: %s<br/>' % data[0]['c']

data = sw.sqlite.select('MIN(date_contact_c) AS c FROM contact')
print 'Oldest contact: %s<br/>' % time.strftime('%Y-%m-%d', time.gmtime(data[0]['c']))


# Who is who
print "<h1>Top 20 Lobbiers</h1>"
data = sw.sqlite.select('behalf, count(behalf) AS c FROM contact GROUP BY behalf ORDER by c DESC LIMIT 20')
for row in data:
    b = row['behalf']
    print '<a href="../communication_log_lobbier/?%s">%s (%s)</a><br/>' % (b, cgi.escape(b), row['c'])

print '<a href="http://scraperwikiviews.com/run/communication_log_lobbiers_1/">See all lobbiers</a>'

print "<h1>Top 20 Lobbied (Organization)</h1>"
data = sw.sqlite.select('organization, count(organization) AS c FROM victim GROUP BY organization ORDER BY c DESC LIMIT 20')
for row in data:
    print "%s (%s)<br/>" % (row['organization'], row['c'])

print "<h1>Top 20 Lobbied (Person)</h1>"
data = sw.sqlite.select('person, count(person) AS c FROM victim GROUP BY person ORDER BY c DESC LIMIT 20')
for row in data:
    print "%s (%s)<br/>" % (row['person'], row['c'])

print "<h1>Top 20 Subjects</h1>"
data = sw.sqlite.select('subject, count(subject) AS c FROM contact_subject GROUP BY subject ORDER BY c DESC LIMIT 20')
for row in data:
    print "%s (%s)<br/>" % (row['subject'], row['c'])import scraperwiki as sw
import time
import urllib
import cgi


sw.sqlite.attach('communication_log')

# Basic counts
data = sw.sqlite.select('count(*) AS c FROM contact')
print 'Contacts: %s<br/>' % data[0]['c']

data = sw.sqlite.select('* FROM contact WHERE error<>0')
print 'Errors: %s<br/>' % len(data)
if len(data) > 0:
    for row in data:
        print 'Error %s: <a href="%s">%s</><br/>' % (row['contact_id'], row['uri'], row['uri'])
    print '<hr/>'

data = sw.sqlite.select('count(*) AS c FROM victim')
print 'Lobbied: %s<br/>' % data[0]['c']

data = sw.sqlite.select('MIN(date_contact_c) AS c FROM contact')
print 'Oldest contact: %s<br/>' % time.strftime('%Y-%m-%d', time.gmtime(data[0]['c']))


# Who is who
print "<h1>Top 20 Lobbiers</h1>"
data = sw.sqlite.select('behalf, count(behalf) AS c FROM contact GROUP BY behalf ORDER by c DESC LIMIT 20')
for row in data:
    b = row['behalf']
    print '<a href="../communication_log_lobbier/?%s">%s (%s)</a><br/>' % (b, cgi.escape(b), row['c'])

print '<a href="http://scraperwikiviews.com/run/communication_log_lobbiers_1/">See all lobbiers</a>'

print "<h1>Top 20 Lobbied (Organization)</h1>"
data = sw.sqlite.select('organization, count(organization) AS c FROM victim GROUP BY organization ORDER BY c DESC LIMIT 20')
for row in data:
    print "%s (%s)<br/>" % (row['organization'], row['c'])

print "<h1>Top 20 Lobbied (Person)</h1>"
data = sw.sqlite.select('person, count(person) AS c FROM victim GROUP BY person ORDER BY c DESC LIMIT 20')
for row in data:
    print "%s (%s)<br/>" % (row['person'], row['c'])

print "<h1>Top 20 Subjects</h1>"
data = sw.sqlite.select('subject, count(subject) AS c FROM contact_subject GROUP BY subject ORDER BY c DESC LIMIT 20')
for row in data:
    print "%s (%s)<br/>" % (row['subject'], row['c'])