# -*- coding: utf-8 -*

import scraperwiki
import mechanize
import lxml.html
import re
import time
import datetime
regex_malsnumer = re.compile(".*/\d*")
regex_domstoll = re.compile(".*/\d* (.*)")

baseurl = 'http://domstolar.is/'
domstolar = ['reykjavik', 'vesturland', 'vestfirdir', 'nordurlandvestra', 'nordurlandeystra', 'austurland', 'sudurland', 'reykjanes'] 

def scrape(url,domstoll_short):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    content = root.xpath ('//div[@class="column-one-content-sub"]/*')
    for c in content[2:-3]:
        record = {}
        record['date'] = c[0][0][0].text
        record['domari'] = c[0][1][0].tail
        malsnumer = regex_malsnumer.findall(c[0][1].text)
        record['malsnumer'] = malsnumer[0]
        domstoll = regex_domstoll.findall(c[0][1].text)
        record['domstoll'] = domstoll[0]
        record['nanar'] = c[1].text
        record['nanar url'] = baseurl + c[2][0].get('href')[1:]
        scraperwiki.sqlite.save(['malsnumer'], data=record, table_name=domstoll_short)
    next_page_link = root.xpath('//span[@class="newspagedprev"]/*')
    if not next_page_link:
        print 'last result page'
        print
    else:
        print 'next page: ', next_page_link[0].get('href')[1:]
        scrape(baseurl + next_page_link[0].get('href')[1:],domstoll_short)

for d in domstolar:
    url = baseurl + d + '/domar/'
    domstoll_short = d
    print 'Processing ', domstoll_short
    print '----------'
    scrape(url,domstoll_short)
