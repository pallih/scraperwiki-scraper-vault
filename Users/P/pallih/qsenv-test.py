import scraperwiki
import os
import cgi

#qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
print os.getenv("QUERY_STRING")  # prints out the query_string value
#for q in qsenv:
#    print q
#scraperwiki.sqlite.save(data=qsenv)



