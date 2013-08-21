import scraperwiki
import lxml, lxml.html, lxml.etree
import re

for x in range(1, 2):
    html = scraperwiki.scrape("http://www.vouchercloud.nl/mobiele-vouchercodes/pg" + str(x))
    root = lxml.html.fromstring(html)
    for li.redes_merchant filtered_redes_merchant in root.cssselect('ul.results'):
         print li.redes_merchant filtered_redes_merchant
