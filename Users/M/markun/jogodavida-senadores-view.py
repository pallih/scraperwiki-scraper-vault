import scraperwiki
import os
import json

scraperwiki.sqlite.attach("jogodavida-senadores-list")

comission = os.getenv("QUERY_STRING")  # prints out the query_string value

ids_raw = scraperwiki.sqlite.select('senator_id from comissions where short_name=?', comission)

senators = []
for id in ids_raw:
    senator = scraperwiki.sqlite.select('name, email from senadores_list where id=?', id['senator_id'])
    senators = senators + senator
print json.dumps(senators, sort_keys=True, indent=4)

