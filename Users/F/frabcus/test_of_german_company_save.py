import scraperwiki

record =  {'court': u'Kiel', 'name': u'Adolf K\xf6hn vorm. Chr. K\xf6hn GmbH & Co KG', 'register_type': u'HRA', 'idnum': u'1 EC', 'state': u'Schleswig-Holstein', 'location': u'Eckernf\xf6rde', 'last_seen': '2011-04-30'}

record =  {'court': u'Kiel', 'name': u'Adolf K\xf6hn vorm. Chr. K\xf6hn GmbH & Co KG', 'register_type': u'HRA', 'idnum': u'1 EC', 'state': u'Schleswig-Holstein', 'location': u'Eckernf\xf6rde', 'last_seen': '2011-05-01'}

scraperwiki.sqlite.save(unique_keys=['court', 'register_type', 'idnum'], data=record)


print scraperwiki.sqlite.table_info("swdata")


import scraperwiki

record =  {'court': u'Kiel', 'name': u'Adolf K\xf6hn vorm. Chr. K\xf6hn GmbH & Co KG', 'register_type': u'HRA', 'idnum': u'1 EC', 'state': u'Schleswig-Holstein', 'location': u'Eckernf\xf6rde', 'last_seen': '2011-04-30'}

record =  {'court': u'Kiel', 'name': u'Adolf K\xf6hn vorm. Chr. K\xf6hn GmbH & Co KG', 'register_type': u'HRA', 'idnum': u'1 EC', 'state': u'Schleswig-Holstein', 'location': u'Eckernf\xf6rde', 'last_seen': '2011-05-01'}

scraperwiki.sqlite.save(unique_keys=['court', 'register_type', 'idnum'], data=record)


print scraperwiki.sqlite.table_info("swdata")


