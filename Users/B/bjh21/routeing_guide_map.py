import scraperwiki
scraperwiki.sqlite.attach('atoc_routeing_guide')
import cgi
import os

args = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
map = scraperwiki.sqlite.select("data FROM maps WHERE pageno = ?", (int(args.get('pageno', 1))))[0]['data']
scraperwiki.utils.httpresponseheader("Content-Type", "image/png")
scraperwiki.dumpMessage({"content":map, "message_type":"console", "encoding":"base64"})
