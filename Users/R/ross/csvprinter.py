import scraperwiki
import cgi, os           

# Get queryparams and pull the relevant bits.
params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
sourcescraper = params['scraper']
sourcetable = params['table']

# Make sure we return the data as text/csv
scraperwiki.utils.httpresponseheader("Content-Type", "text/csv; charset=utf-8")
scraperwiki.utils.httpresponseheader("Content-Disposition", 'attachment; filename=\"%s-%s.csv\"' % (sourcescraper, sourcetable,))

# Make sure we attach to the DB, and call it src
scraperwiki.sqlite.attach(sourcescraper, "src")

# Get the table info and write it out as a header
info = scraperwiki.sqlite.table_info("src." + sourcetable)
print ",".join(['\"%s\"' % d['name'] for d in info])


count = scraperwiki.sqlite.select("count(*) from src." + sourcetable)[0]['count(*)']
limit, offset = 1000, 0
while count > -1:
    record = scraperwiki.sqlite.select("* from src.%s limit %d offset %d" % (sourcetable, limit, offset,) )
    for r in record:
        print ",".join(['\"%s\"' % r[d['name']] for d in info])                
    offset = offset + limit
    count = count - 1000
import scraperwiki
import cgi, os           

# Get queryparams and pull the relevant bits.
params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
sourcescraper = params['scraper']
sourcetable = params['table']

# Make sure we return the data as text/csv
scraperwiki.utils.httpresponseheader("Content-Type", "text/csv; charset=utf-8")
scraperwiki.utils.httpresponseheader("Content-Disposition", 'attachment; filename=\"%s-%s.csv\"' % (sourcescraper, sourcetable,))

# Make sure we attach to the DB, and call it src
scraperwiki.sqlite.attach(sourcescraper, "src")

# Get the table info and write it out as a header
info = scraperwiki.sqlite.table_info("src." + sourcetable)
print ",".join(['\"%s\"' % d['name'] for d in info])


count = scraperwiki.sqlite.select("count(*) from src." + sourcetable)[0]['count(*)']
limit, offset = 1000, 0
while count > -1:
    record = scraperwiki.sqlite.select("* from src.%s limit %d offset %d" % (sourcetable, limit, offset,) )
    for r in record:
        print ",".join(['\"%s\"' % r[d['name']] for d in info])                
    offset = offset + limit
    count = count - 1000
import scraperwiki
import cgi, os           

# Get queryparams and pull the relevant bits.
params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
sourcescraper = params['scraper']
sourcetable = params['table']

# Make sure we return the data as text/csv
scraperwiki.utils.httpresponseheader("Content-Type", "text/csv; charset=utf-8")
scraperwiki.utils.httpresponseheader("Content-Disposition", 'attachment; filename=\"%s-%s.csv\"' % (sourcescraper, sourcetable,))

# Make sure we attach to the DB, and call it src
scraperwiki.sqlite.attach(sourcescraper, "src")

# Get the table info and write it out as a header
info = scraperwiki.sqlite.table_info("src." + sourcetable)
print ",".join(['\"%s\"' % d['name'] for d in info])


count = scraperwiki.sqlite.select("count(*) from src." + sourcetable)[0]['count(*)']
limit, offset = 1000, 0
while count > -1:
    record = scraperwiki.sqlite.select("* from src.%s limit %d offset %d" % (sourcetable, limit, offset,) )
    for r in record:
        print ",".join(['\"%s\"' % r[d['name']] for d in info])                
    offset = offset + limit
    count = count - 1000
import scraperwiki
import cgi, os           

# Get queryparams and pull the relevant bits.
params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
sourcescraper = params['scraper']
sourcetable = params['table']

# Make sure we return the data as text/csv
scraperwiki.utils.httpresponseheader("Content-Type", "text/csv; charset=utf-8")
scraperwiki.utils.httpresponseheader("Content-Disposition", 'attachment; filename=\"%s-%s.csv\"' % (sourcescraper, sourcetable,))

# Make sure we attach to the DB, and call it src
scraperwiki.sqlite.attach(sourcescraper, "src")

# Get the table info and write it out as a header
info = scraperwiki.sqlite.table_info("src." + sourcetable)
print ",".join(['\"%s\"' % d['name'] for d in info])


count = scraperwiki.sqlite.select("count(*) from src." + sourcetable)[0]['count(*)']
limit, offset = 1000, 0
while count > -1:
    record = scraperwiki.sqlite.select("* from src.%s limit %d offset %d" % (sourcetable, limit, offset,) )
    for r in record:
        print ",".join(['\"%s\"' % r[d['name']] for d in info])                
    offset = offset + limit
    count = count - 1000
