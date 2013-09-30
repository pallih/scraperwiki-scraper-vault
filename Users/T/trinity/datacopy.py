import scraperwiki
import json

scraperwiki.sqlite.save(unique_keys=["a"], data={"a":1, "bbb":"Bye there"})           
print scraperwiki.sqlite.execute("select * from swdata")  