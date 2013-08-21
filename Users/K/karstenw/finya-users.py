import scraperwiki
import re
import time

html = scraperwiki.scrape("http://www.finya.de")
pat = re.compile("<h3 .*>([\d\.]+) Mitglieder jetzt online!</h3>")
m = re.search(pat, html)

data = {
  'users' : int(m.group(1).replace(".", "")),
  'ts' : time.time()
}

scraperwiki.sqlite.save(unique_keys=['ts'], data=data)

