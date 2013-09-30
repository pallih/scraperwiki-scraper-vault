import scraperwiki
import lxml, lxml.html, lxml.etree
import re

for x in range(1, 2):
    html = scraperwiki.scrape("http://www.vouchercloud.nl/mobiele-vouchercodes/pg" + str(x))
    root = lxml.html.fromstring(html)
    for div in root.cssselect("div.real_search_results ul"):
        for deal in div.cssselect("ul.results li.redes_merchant ul.offers li.offer"):
            print deal.cssselect("h3 a")[0].attrib['title']
            print "http://www.vouchercloud.nl/" + deal.cssselect("h3 a")[0].attrib['href']
            print deal.cssselect("h4 a")[0].text_content()
            print
              
import scraperwiki
import lxml, lxml.html, lxml.etree
import re

for x in range(1, 2):
    html = scraperwiki.scrape("http://www.vouchercloud.nl/mobiele-vouchercodes/pg" + str(x))
    root = lxml.html.fromstring(html)
    for div in root.cssselect("div.real_search_results ul"):
        for deal in div.cssselect("ul.results li.redes_merchant ul.offers li.offer"):
            print deal.cssselect("h3 a")[0].attrib['title']
            print "http://www.vouchercloud.nl/" + deal.cssselect("h3 a")[0].attrib['href']
            print deal.cssselect("h4 a")[0].text_content()
            print
              
