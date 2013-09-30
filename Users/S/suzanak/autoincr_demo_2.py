import scraperwiki

# Blank Python
try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


scraperwiki.sqlite.save(unique_keys=[], data={'payload':'fat beats'}, table_name='magic')
import scraperwiki

# Blank Python
try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."


scraperwiki.sqlite.save(unique_keys=[], data={'payload':'fat beats'}, table_name='magic')
