import scraperwiki

html = scraperwiki.scrape("http://www.pcworld.com/shopping/browse/category.html")

import lxml.html           
root = lxml.html.fromstring(html)


for div in root.cssselect("div.shoppingDirectory div.module section clearfix"):

    data = {
        'cell' : (div.cssselect("p.Cell Phones &amp; Accessories a"))[0].text,
        'Company' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.ymd"))[0].text_content(),
        'Business' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.cate-txt.location"))[0].text,
        'Value (USD)' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.description"))[0].text,
        'Derived products' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 ul.cate li span"))[2].text
    }
    scraperwiki.sqlite.save(unique_keys=['cell'], data=data)
import scraperwiki

html = scraperwiki.scrape("http://www.pcworld.com/shopping/browse/category.html")

import lxml.html           
root = lxml.html.fromstring(html)


for div in root.cssselect("div.shoppingDirectory div.module section clearfix"):

    data = {
        'cell' : (div.cssselect("p.Cell Phones &amp; Accessories a"))[0].text,
        'Company' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.ymd"))[0].text_content(),
        'Business' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.cate-txt.location"))[0].text,
        'Value (USD)' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 p.description"))[0].text,
        'Derived products' : (div.cssselect("div.dtl-txtb.clearfix div.dtl-txtb-rb2 ul.cate li span"))[2].text
    }
    scraperwiki.sqlite.save(unique_keys=['cell'], data=data)
