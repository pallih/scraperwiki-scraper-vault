import scraperwiki

#search = scraperwiki.swimport('twitter_search_extended').search

#search(['olympics'], num_pages=5)
import pprint

import datetime

pprint.pprint(scraperwiki.sqlite.show_tables())
pprint.pprint(scraperwiki.sqlite.execute("select * from sqlite_master"))
pprint.pprint(scraperwiki.sqlite.select("* from sqlite_master"))
pprint.pprint(scraperwiki.sqlite.execute("drop table foo4"))
pprint.pprint(scraperwiki.sqlite.execute("create table foo4 (id integer, asd text)"))
pprint.pprint(scraperwiki.sqlite.execute("select * from foo"))

pprint.pprint(scraperwiki.sqlite.save(["id"], {"id": datetime.datetime.now()}))

scraperwiki.sqlite.save_var("sad","aosid")

pprint.pprint(scraperwiki.sqlite.save(["id"], {"id": datetime.datetime.now()}))

scraperwiki.sqlite.save_var("asodi-09", datetime.datetime.now())

import scraperwiki

#search = scraperwiki.swimport('twitter_search_extended').search

#search(['olympics'], num_pages=5)
import pprint

import datetime

pprint.pprint(scraperwiki.sqlite.show_tables())
pprint.pprint(scraperwiki.sqlite.execute("select * from sqlite_master"))
pprint.pprint(scraperwiki.sqlite.select("* from sqlite_master"))
pprint.pprint(scraperwiki.sqlite.execute("drop table foo4"))
pprint.pprint(scraperwiki.sqlite.execute("create table foo4 (id integer, asd text)"))
pprint.pprint(scraperwiki.sqlite.execute("select * from foo"))

pprint.pprint(scraperwiki.sqlite.save(["id"], {"id": datetime.datetime.now()}))

scraperwiki.sqlite.save_var("sad","aosid")

pprint.pprint(scraperwiki.sqlite.save(["id"], {"id": datetime.datetime.now()}))

scraperwiki.sqlite.save_var("asodi-09", datetime.datetime.now())

