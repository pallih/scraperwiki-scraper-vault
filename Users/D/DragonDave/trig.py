import scraperwiki

# Blank Python

#scraperwiki.sqlite.execute("create table if not exists trig core(a int);")
#scraperwiki.sqlite.execute("create table if not exists trig updated(row int);")
#scraperwiki.sqlite.execute("drop trigger trig;")
scraperwiki.sqlite.execute("create trigger if not exists trig after insert on core begin insert into updated values (new.rowid); end;")

scraperwiki.sqlite.execute("delete from updated;")
scraperwiki.sqlite.commit() 
scraperwiki.sqlite.execute("insert into core values (12);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.save(unique_keys=[], data={'a':5}, table_name="core", verbose=2) 
scraperwiki.sqlite.commit() import scraperwiki

# Blank Python

#scraperwiki.sqlite.execute("create table if not exists trig core(a int);")
#scraperwiki.sqlite.execute("create table if not exists trig updated(row int);")
#scraperwiki.sqlite.execute("drop trigger trig;")
scraperwiki.sqlite.execute("create trigger if not exists trig after insert on core begin insert into updated values (new.rowid); end;")

scraperwiki.sqlite.execute("delete from updated;")
scraperwiki.sqlite.commit() 
scraperwiki.sqlite.execute("insert into core values (12);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.execute("insert into core values (4);")
scraperwiki.sqlite.save(unique_keys=[], data={'a':5}, table_name="core", verbose=2) 
scraperwiki.sqlite.commit() 