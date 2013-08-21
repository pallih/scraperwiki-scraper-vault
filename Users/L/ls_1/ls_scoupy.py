import scraperwiki
import lxml, lxml.html, lxml.etree
import re

for x in range(1, 220):
    html = scraperwiki.scrape("http://scoupy.nl/nl/coupons#/page/" + str(x))
    root = lxml.html.fromstring(html)
    for div in root.cssselect("article"):
        deal = div[0]
        deal_id = deal.cssselect('input')[0].attrib['value']
        deal_title = deal.cssselect('input')[1].attrib['value']
        deal_text = deal.cssselect('input')[2].attrib['value']
        deal_retailer = deal.cssselect('input')[3].attrib['value']
        deal_url = deal.cssselect('input')[4].attrib['value']
        data = { 'deal_id' : deal_id,
                'deal_title' : deal_title,
                'deal_text' : deal_text,
                'deal_retailer' : deal_retailer,
                'deal_url' : deal_url }
        scraperwiki.sqlite.save(unique_keys=['deal_id'], data=data)
