# It would be nice to have a "date_first_scraped" field that persisted between runs.
# This would make it possible to create an RSS feed and add new items as they appear. 
# This scraper shows one way to create such a field... is there a better way?
from datetime import datetime
import scraperwiki

# Extend this with additional fields.
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS swdata (num INT PRIMARY KEY, date_first_scraped TEXT)')
scraperwiki.sqlite.commit()

for i in range(0,1000):
    scraperwiki.sqlite.execute("INSERT OR IGNORE INTO swdata VALUES(?,?)", [i, str(datetime.utcnow())])
    # Use an UPDATE statement to fill in additional fields.
    # scraperwiki.sqlite.execute("UPDATE swdata SET foo = ? WHERE num = ?", ['bar', i])

scraperwiki.sqlite.commit()
# It would be nice to have a "date_first_scraped" field that persisted between runs.
# This would make it possible to create an RSS feed and add new items as they appear. 
# This scraper shows one way to create such a field... is there a better way?
from datetime import datetime
import scraperwiki

# Extend this with additional fields.
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS swdata (num INT PRIMARY KEY, date_first_scraped TEXT)')
scraperwiki.sqlite.commit()

for i in range(0,1000):
    scraperwiki.sqlite.execute("INSERT OR IGNORE INTO swdata VALUES(?,?)", [i, str(datetime.utcnow())])
    # Use an UPDATE statement to fill in additional fields.
    # scraperwiki.sqlite.execute("UPDATE swdata SET foo = ? WHERE num = ?", ['bar', i])

scraperwiki.sqlite.commit()
