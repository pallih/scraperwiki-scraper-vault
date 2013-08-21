# -*- coding: utf-8 -*-
import scraperwiki
import random
from lxml.cssselect import CSSSelector
from lxml import etree
import lxml.html
import cookielib, urllib2

scraperwiki.sqlite.attach("handelsregisterbekanntmachungende", "src")
#print scraperwiki.sqlite.select("DISTINCT `courtName`, `courtRefNum` from src.swdata limit 1")
#print len(scraperwiki.sqlite.select("`courtName`, `courtRefNum` FROM src.swdata"))
#print scraperwiki.sqlite.select("`courtName` AS cn, rtrim(`courtRefNum`) as crn, COUNT(`id`) AS cnt from src.swdata group by cn, crn having cnt > 1 limit 1")

# This is empty -> Every courtName starts with "Amtsgericht"
# print scraperwiki.sqlite.select("`courtName` from src.swdata where `courtName` NOT LIKE '%Amtsgericht%' limit 1")

maskUrl = "https://www.handelsregister.de/rp_web/mask.do?Typ=n"
companies = scraperwiki.sqlite.select("`courtName` AS cn, rtrim(`courtRefNum`) as crn FROM src.swdata LIMIT 1")


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPSHandler())
#opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPSHandler(debuglevel=1))
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'),
    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
    ('Accept-Language', 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3'),
    ('Accept-Encoding', 'gzip,deflate'),
    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
    ('Keep-Alive', '115'),
    ('Connection', 'keep-alive'),
    ('Cache-Control', 'max-age=0'),
    ('Referer', 'https://www.handelsregister.de/rp_web/search.do'),
    ('Pragma', 'no-cache, no-cache')
]

court_option_selector = CSSSelector("select[name=registergericht] option")
response = opener.open(maskUrl)
html = response.read()
root = lxml.html.fromstring(html)
courtMap = dict([(opt.text_content(),opt.get('value')) for opt in court_option_selector(root)])
print courtMap
print courtMap.get("Leipzig")

for company in companies:
    courtName = company['cn'][12:]
    (regType, sep, regNum) = company['crn'].partition(' ')
    print courtName
    print regType
    print regNum
    #urllib.urlencode
    #forms = mechanize.ParseResponse(response, backwards_compat=False)
    #form = forms[0]
    #response.close()
    #browser.select_form(nr=0)
    #forms = browser.forms()
    #print browser.possible_items("registergericht")
    

    #browser["registerArt"] = [ 'regType' ]
    #browser["registerNummer"] = [ 'regNum' ]
    #browser["registergericht"] = [ 'regType' ]

    #print form
    #form.set_value([regType], "registerArt")
    #form.set_value(regNum, "registerNummer")
    #form.set_value_by_label([courtName], "registergericht")
    #print form.find_control("registerArt")
    #print form.find_control("registerNummer")
    #print form.find_control("registergericht")
    #response = browser.submit()
