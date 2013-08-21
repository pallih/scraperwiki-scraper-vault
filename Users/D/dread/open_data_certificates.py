import scraperwiki
from urllib2 import HTTPError
import lxml.html           

i = 1
while True:
  data = {}
  data['url'] = "https://certificates.theodi.org/certificates/%s" % i
  data['id'] = i
  try:
    html = scraperwiki.scrape(data['url'])
  except HTTPError, e:
    if e.code == 404:
      break
    raise
  root = lxml.html.fromstring(html)
  summary = root.cssselect("div.certificate-summary")[0]
  data['level'] = summary.cssselect("strong.certificate-level")[0].text_content().strip()
  data['title'] = summary.cssselect("h1")[0].text_content()
  print data
  scraperwiki.sqlite.save(unique_keys=['id'], data=data)
  i += 1
