from scraperwiki.sqlite import execute
execute('DROP TABLE foo')
execute('CREATE TABLE foo (bar TEXT)')
execute('INSERT INTO foo VALUES ("baz")')