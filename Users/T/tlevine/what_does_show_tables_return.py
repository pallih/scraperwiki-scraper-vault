import scraperwiki
scraperwiki.sqlite.save([], {'foo': 'bar'}, 'baz')
print scraperwiki.sqlite.show_tables()
print scraperwiki.sqlite.select('name, sql from sqlite_master where type = "table";')
print scraperwiki.sqlite.select('* from sqlite_master where type = "table";')

print scraperwiki.httpresponseheaderimport scraperwiki
scraperwiki.sqlite.save([], {'foo': 'bar'}, 'baz')
print scraperwiki.sqlite.show_tables()
print scraperwiki.sqlite.select('name, sql from sqlite_master where type = "table";')
print scraperwiki.sqlite.select('* from sqlite_master where type = "table";')

print scraperwiki.httpresponseheader