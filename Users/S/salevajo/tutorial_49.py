import scraperwiki
import re

# Aktuelle Session erzeugen
sessionPage = scraperwiki.scrape("http://alephino.documentaarchiv.de/alipac")
print sessionPage
# Basis URL der aktuellen Session extrahieren
url = re.search('URL=(.*)/find-simple"', sessionPage).group(1)
print url

# Suche der Künstler der documenta 1 bis N
N = 12
for documentaN in range(1, N) :
    search = url + "/sysix?SCAN_CODE=ALL%3AART&SCAN_START=documenta%20"+str(documentaN)
    result = scraperwiki.scrape(search)
    print result