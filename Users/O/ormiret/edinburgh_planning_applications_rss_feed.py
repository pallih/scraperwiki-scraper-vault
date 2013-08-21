import scraperwiki
import StringIO
import re
from datetime import datetime
import time

def totimestamp(dt):
    return time.mktime(dt.timetuple()) + dt.microsecond/1e6

sourcescraper = "edinburgh_planning_applications"
def timeAsrfc822(theTime):
    import rfc822
    return rfc822.formatdate(totimestamp(theTime))

limit = 20
offset = 0

# set the correct Content-Type
scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata order by date_scraped desc limit ? offset ? ", (limit, offset))
keys = sdata.get("keys")
rows = sdata.get("data")

out = StringIO.StringIO()
out.write('<?xml version="1.0" encoding="utf-8" ?>\n')
out.write('<rss version="2.0">\n')
out.write("""<channel>
<title>Edinburgh planning applications</title>
<description>Planning applications submitted to Edinburgh City Council.</description>
<link>http://scraperwiki.com/scrapers/edinburgh_planning_applications/</link>
<lastBuildDate>"""+timeAsrfc822(datetime.now())+"</lastBuildDate>\n")
out.write("<pubDate>"+timeAsrfc822(datetime.now())+"</pubDate>\n")

for row in rows:
    out.write("<item>\n")
    out.write("<title>"+row[keys.index("address")]+"</title>\n")
    out.write("<description>&lt;p&gt;"+row[keys.index("proposal")]+"&lt;/p&gt;\n&lt;p&gt;\nStatus: "+row[keys.index("status")])
    out.write("&lt;/p&gt;\n&lt;p&gt;Applicant name: "+row[keys.index("applicant name")])
    out.write("&lt;/p&gt;\n&lt;p&gt;Date received: "+row[keys.index("date received")])
    out.write("&lt;/p&gt;\n</description>\n")
    out.write("<link>http://citydev-portal.edinburgh.gov.uk/publicaccess/tdc/DcApplication/application_detailview.aspx?caseno="+row[keys.index("detail")]+"</link>\n")
    out.write("<pubDate>"+timeAsrfc822(datetime.strptime(row[keys.index("date_scraped")], "%Y-%m-%dT%H:%M:%S.%f"))+"</pubDate>\n")
    out.write("<guid>http://citydev-portal.edinburgh.gov.uk/publicaccess/tdc/DcApplication/application_detailview.aspx?caseno="+row[keys.index("detail")]+"</guid>\n")
    out.write("</item>\n")
out.write("</channel>\n</rss>\n")

    
print out.getvalue()

