import scraperwiki
import datetime

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32, "created_at": datetime.datetime.now()})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])import scraperwiki
import datetime

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32, "created_at": datetime.datetime.now()})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])import scraperwiki
import datetime

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32, "created_at": datetime.datetime.now()})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])import scraperwiki
import datetime

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32, "created_at": datetime.datetime.now()})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])

scraperwiki.sqlite.save(["name"], {"name":"Jack", "age": 32})
data = scraperwiki.sqlite.select("name, created_at from swdata")
print "{name} was created at {created_at}".format(**data[0])