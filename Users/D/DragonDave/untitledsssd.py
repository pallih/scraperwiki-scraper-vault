import scraperwiki

# Blank Python

print scraperwiki.sqlite.execute("select * from sqlite_master where tbl_name", None)
url = 'jam'
scraperwiki.sqlite.select('* from sqlite_master where tbl_name=?',url)import scraperwiki

# Blank Python

print scraperwiki.sqlite.execute("select * from sqlite_master where tbl_name", None)
url = 'jam'
scraperwiki.sqlite.select('* from sqlite_master where tbl_name=?',url)