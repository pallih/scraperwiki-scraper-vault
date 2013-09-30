import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


import os
import json
from scraperwiki.datastore import sqlitecommand
import urllib

sqlitecommand("attach", "uk_lottery_parsecollector", "src")

urlquery = os.getenv("URLQUERY", "")
if urlquery:
    res = sqlitecommand("execute", "select * from src.lotterygrants where localauthority=?", (urllib.unquote(urlquery),))
else:
    res = sqlitecommand("execute", "select count(1) as c, sum(amount) as money, localauthority from src.lotterygrants where localauthority!='' group by localauthority")

r = [ dict(zip(res.get("keys"), d))  for d in res.get("data") ]
print json.dumps(r)


