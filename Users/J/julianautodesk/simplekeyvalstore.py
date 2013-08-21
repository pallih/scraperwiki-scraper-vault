import os
import cgi
import scraperwiki
import json

scraperwiki.utils.httpresponseheader("Content-Type", "application/javascript")

qs = os.getenv("QUERY_STRING", "")
params = dict(cgi.parse_qsl(qs))

if "key" in params:
    res = scraperwiki.sqlite.get_var(params["key"], params.get("default"))
    if "value" in params:
        scraperwiki.sqlite.save_var(params["key"], params["value"])
else:
    res = "error: Key is missing"

res = json.dumps(res)
if "callback" in params:
    res = "%s(%s)" % (params["callback"], res)

print res
