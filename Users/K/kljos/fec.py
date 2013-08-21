import scraperwiki
import lxml.etree
import lxml.html
# To load directly from a url, use
root = lxml.html.parse("http://www.fec.gov/finance/disclosure/ftpsum.shtml")
print root