import scraperwiki

scraperwiki.sqlite.execute("DROP TABLE IF EXISTS [spaces in name]")
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS [full stop.]")
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS [Pack my box with five dozen liquor jugs]")
scraperwiki.sqlite.commit()

# letting the scraperwiki.sqlite function create the table schema for me
scraperwiki.sqlite.save(['id'], [{'id': 1}, {'id': 2}, {'id': 3}], 'spaces in name')

# manually defining the table schema, plus table name has a full stop
scraperwiki.sqlite.execute("CREATE TABLE [full stop.] (id INTEGER PRIMARY KEY)")
scraperwiki.sqlite.execute("INSERT INTO [full stop.] (id) VALUES (11)")
scraperwiki.sqlite.execute("INSERT INTO [full stop.] (id) VALUES (12)")
scraperwiki.sqlite.execute("INSERT INTO [full stop.] (id) VALUES (13)")
scraperwiki.sqlite.commit()

# really long table name with a full stop, and an invalid column data type of "gloves"
scraperwiki.sqlite.execute("CREATE TABLE [Pack my box with five dozen liquor jugs] (hand gloves)")
scraperwiki.sqlite.execute("INSERT INTO [Pack my box with five dozen liquor jugs] (hand) VALUES (31)")
scraperwiki.sqlite.execute("INSERT INTO [Pack my box with five dozen liquor jugs] (hand) VALUES (32)")
scraperwiki.sqlite.execute("INSERT INTO [Pack my box with five dozen liquor jugs] (hand) VALUES (33)")
scraperwiki.sqlite.commit()


