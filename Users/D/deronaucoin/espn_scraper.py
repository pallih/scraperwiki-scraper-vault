import scraperwiki
import urllib
from lxml.html import fromstring, tostring
# Blank Python


url = "http://scores.espn.go.com/ncf/playbyplay?gameId=312440097"

resp = urllib.urlopen(url)

html = fromstring(resp.read())

pbptable = html.find_class('mod-data mod-pbp')



print divs

