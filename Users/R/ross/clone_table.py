import scraperwiki

SCRAPERNAME = 'worldwide_shark_attacks'
TABLE = 'hawaii'
NEW_TABLE_NAME = 'new hawaii'

# Attach future queries to the specified scraper/database so that we 
# can include SCRAPERNAME.TABLE in future queries
scraperwiki.sqlite.attach(SCRAPERNAME);

# Get a dictionary of the table schemas we want which contains the SQL we 
# need to create a matching table.
tables = scraperwiki.sqlite.show_tables( SCRAPERNAME )
print tables


# We could create a local copy of the table with the following two lines, however
# if we use the sqlite.save command, and specify a new table name then it will create
# it as needed.
#scraperwiki.sqlite.execute( tables['Hawaii'] )
#scraperwiki.sqlite.commit()

# Select from the table which will return a list of dictionaries, which also has 
# the advantage of being a shortcut for mass upload in the save command.
results = scraperwiki.sqlite.select('* from %s.%s' % (SCRAPERNAME, TABLE) )
scraperwiki.sqlite.save([], results, table_name=NEW_TABLE_NAME)

