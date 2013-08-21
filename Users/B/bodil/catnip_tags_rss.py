import scraperwiki
import xml.etree.ElementTree as ET
from cStringIO import StringIO

scraperwiki.sqlite.attach("catnip_tags")
data = scraperwiki.sqlite.select("* from catnip_tags.swdata order by time desc limit 10")

scraperwiki.utils.httpresponseheader("Content-Type", "application/atom+xml")

x = ET.TreeBuilder()
def tag(tag, data = None, attrs = {}):
    x.start(tag, attrs)
    if data:
        x.data(data)
    x.end(tag)

x.start("feed", {"xmlns": "http://www.w3.org/2005/Atom"})

tag("title", "Catnip Tags")
tag("updated", data[0]["time"])

for i in data:
    x.start("entry", {})
    tag("title", i["tag"])
    tag("id", i["hash"])
    tag("link", attrs={"href": i["href"]})
    tag("updated", i["time"])
    tag("summary", """Version %s tagged at commit <a href="%s">%s</a> at %s.""" % (i["tag"], i["href"], i["hash"], i["time"]))
    x.end("entry")

x.end("feed")

doc = ET.ElementTree(x.close())
out = StringIO()
out.write("""<?xml version="1.0" encoding="utf-8"?>\n""")
doc.write(out)
print out.getvalue()
