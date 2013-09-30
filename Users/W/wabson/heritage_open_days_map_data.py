###########################################################
# Proxy view for retreiving JSON data from API            #
###########################################################
import scraperwiki.sqlite
import scraperwiki.utils
import urllib2
import urllib
import json

def safe_quote(val):
    return val.replace("\\", "\\\\").replace("'", "\\'")

sourcescraper = "heritage_open_days"
limit = 5000
offset = 0

events = []

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

predicates = ["lat != '' AND lng != ''"]

params = scraperwiki.utils.GET()
region = "South East"
if "region" in params:
    region = params["region"]


predicates.append("region = '%s'" % (safe_quote(region)))

# Optional filters
if ("day" in params and params["day"] != "All" and params["day"] != "Any"):
    predicates.append("opening_times LIKE '%" + safe_quote(params["day"]) + "%'")
if ("not_normally_open" in params):
    predicates.append("not_normally_open = %s" % (safe_quote(int(params["not_normally_open"]))))
if ("not_normally_free" in params):
    predicates.append("not_normally_free = %s" % (safe_quote(int(params["not_normally_free"]))))
if ("wheelchair_access" in params and params["wheelchair_access"] == "full"):
    predicates.append("full_wheelchair_access = 'Yes'")
elif ("wheelchair_access" in params and params["wheelchair_access"] == "partial"):
    predicates.append("full_wheelchair_access = 'Partial'")
elif ("wheelchair_access" in params and params["wheelchair_access"] == "none"):
    predicates.append("full_wheelchair_access = ''")

cols = "name, address, description, lat, lng, prebooking_required, directions, opening_times, full_wheelchair_access, access_information, additional_information, organiser, event_code, not_normally_open, not_normally_free"

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("SELECT %s FROM src.swdata WHERE %s limit %s offset %s" % (cols, " AND ".join(predicates), limit, offset))

keys = sdata.get("keys")
rows = sdata.get("data")

for row in rows:
    lat = row[3]
    lng = row[4]
    events.append({
        'name': row[0],
        'address': row[1],
        'description': row[2],
        'lat': float(lat),
        'lng': float(lng),
        'prebooking_required': row[5],
        'directions': "",
        'opening_times': row[7],
        'full_wheelchair_access': row[8],
        'access_information': row[9],
        'additional_information': "",
        'organiser': "",
        'event_code': row[12],
        'not_normally_open': int(row[13]) == 1,
        'not_normally_free': int(row[14]) == 1
    })

print(json.dumps(events))

#jsonurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=heritage_open_days&query=select%20name%2C%20address%2C%20description%2C%20CAST(lat%20AS%20NUMERIC)%20AS%20lat%2C%20CAST(lng%20AS%20NUMERIC)%20as%20lng%20from%20swdata%20where%20lat%20%3E%2051.396030%20limit%2010""
###########################################################
# Proxy view for retreiving JSON data from API            #
###########################################################
import scraperwiki.sqlite
import scraperwiki.utils
import urllib2
import urllib
import json

def safe_quote(val):
    return val.replace("\\", "\\\\").replace("'", "\\'")

sourcescraper = "heritage_open_days"
limit = 5000
offset = 0

events = []

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

predicates = ["lat != '' AND lng != ''"]

params = scraperwiki.utils.GET()
region = "South East"
if "region" in params:
    region = params["region"]


predicates.append("region = '%s'" % (safe_quote(region)))

# Optional filters
if ("day" in params and params["day"] != "All" and params["day"] != "Any"):
    predicates.append("opening_times LIKE '%" + safe_quote(params["day"]) + "%'")
if ("not_normally_open" in params):
    predicates.append("not_normally_open = %s" % (safe_quote(int(params["not_normally_open"]))))
if ("not_normally_free" in params):
    predicates.append("not_normally_free = %s" % (safe_quote(int(params["not_normally_free"]))))
if ("wheelchair_access" in params and params["wheelchair_access"] == "full"):
    predicates.append("full_wheelchair_access = 'Yes'")
elif ("wheelchair_access" in params and params["wheelchair_access"] == "partial"):
    predicates.append("full_wheelchair_access = 'Partial'")
elif ("wheelchair_access" in params and params["wheelchair_access"] == "none"):
    predicates.append("full_wheelchair_access = ''")

cols = "name, address, description, lat, lng, prebooking_required, directions, opening_times, full_wheelchair_access, access_information, additional_information, organiser, event_code, not_normally_open, not_normally_free"

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("SELECT %s FROM src.swdata WHERE %s limit %s offset %s" % (cols, " AND ".join(predicates), limit, offset))

keys = sdata.get("keys")
rows = sdata.get("data")

for row in rows:
    lat = row[3]
    lng = row[4]
    events.append({
        'name': row[0],
        'address': row[1],
        'description': row[2],
        'lat': float(lat),
        'lng': float(lng),
        'prebooking_required': row[5],
        'directions': "",
        'opening_times': row[7],
        'full_wheelchair_access': row[8],
        'access_information': row[9],
        'additional_information': "",
        'organiser': "",
        'event_code': row[12],
        'not_normally_open': int(row[13]) == 1,
        'not_normally_free': int(row[14]) == 1
    })

print(json.dumps(events))

#jsonurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=heritage_open_days&query=select%20name%2C%20address%2C%20description%2C%20CAST(lat%20AS%20NUMERIC)%20AS%20lat%2C%20CAST(lng%20AS%20NUMERIC)%20as%20lng%20from%20swdata%20where%20lat%20%3E%2051.396030%20limit%2010""
