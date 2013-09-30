# Full text search example, taken from here:
# http://www.sqlite.org/fts3.html#section_1_4

import scraperwiki

# Run these once to make the table and set up some values:
# scraperwiki.sqlite.execute("CREATE VIRTUAL TABLE oomail USING fts3(subject, body)")
#scraperwiki.sqlite.execute("INSERT INTO oomail(docid, subject, body) VALUES(1, 'software feedback', 'found it too slow')")
#scraperwiki.sqlite.execute("INSERT INTO oomail(docid, subject, body) VALUES(2, 'software feedback', 'no feedback')")
#scraperwiki.sqlite.execute("INSERT INTO oomail(docid, subject, body) VALUES(3, 'slow lunch order',  'was a software problem')")
#scraperwiki.sqlite.commit()

# Then these kinds of queries work:
print scraperwiki.sqlite.execute("SELECT * FROM oomail WHERE subject MATCH 'software'") #    -- Selects rows 1 and 2
# print scraperwiki.sqlite.execute("SELECT * FROM mail WHERE body    MATCH 'feedback'") #    -- Selects row 2
# print scraperwiki.sqlite.execute("SELECT * FROM mail WHERE mail    MATCH 'software'") #    -- Selects rows 1, 2 and 3
# print scraperwiki.sqlite.execute("SELECT * FROM mail WHERE mail    MATCH 'slow'") #        -- Selects rows 1 and 3
# Full text search example, taken from here:
# http://www.sqlite.org/fts3.html#section_1_4

import scraperwiki

# Run these once to make the table and set up some values:
# scraperwiki.sqlite.execute("CREATE VIRTUAL TABLE oomail USING fts3(subject, body)")
#scraperwiki.sqlite.execute("INSERT INTO oomail(docid, subject, body) VALUES(1, 'software feedback', 'found it too slow')")
#scraperwiki.sqlite.execute("INSERT INTO oomail(docid, subject, body) VALUES(2, 'software feedback', 'no feedback')")
#scraperwiki.sqlite.execute("INSERT INTO oomail(docid, subject, body) VALUES(3, 'slow lunch order',  'was a software problem')")
#scraperwiki.sqlite.commit()

# Then these kinds of queries work:
print scraperwiki.sqlite.execute("SELECT * FROM oomail WHERE subject MATCH 'software'") #    -- Selects rows 1 and 2
# print scraperwiki.sqlite.execute("SELECT * FROM mail WHERE body    MATCH 'feedback'") #    -- Selects row 2
# print scraperwiki.sqlite.execute("SELECT * FROM mail WHERE mail    MATCH 'software'") #    -- Selects rows 1, 2 and 3
# print scraperwiki.sqlite.execute("SELECT * FROM mail WHERE mail    MATCH 'slow'") #        -- Selects rows 1 and 3
