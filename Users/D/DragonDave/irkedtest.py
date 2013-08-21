import scraperwiki
import lxml
irked=scraperwiki.swimport('irked')

root=lxml.html.fromstring('<html><body>a</body><body>b</body></html>')

print root.onecss('body').text
print root.onecss('clive').text