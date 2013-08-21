from urllib2 import urlopen,URLError

class SiteWorks(Exception):
  pass

try:
  urlopen('https://rn.ftc.gov/pls/textilern/wrnquery$.startup',timeout=8)
except URLError:
  pass
else:
  raise SiteWorks("""

OMG rn.ftc.gov is up again! Now scrape it.

Read more here.
http://groups.google.com/group/scraperwiki/browse_thread/thread/826c58c456a81174?hl=en
 
""")