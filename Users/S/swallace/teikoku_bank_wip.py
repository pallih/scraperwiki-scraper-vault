# -*- coding: utf-8; -*-

import mechanize
import lxml.html
import scraperwiki
import urllib

BASE_URL = "http://www.tdb.co.jp/service/u/1000.jsp"
SEARCH_ADDRESS = u"大阪府大阪市天王寺区"

#######################
###     methods     ###
#######################

def build_url(BASE_URL, page_num, address_sikugun):
    test = urllib.quote(address_sikugun.encode('shift_jis'))
    param = urllib.urlencode({"page_count":page_num,"companyName":"","companyNameAccord":1,"freeWord":""})
    url = BASE_URL + "?" + param + "&address_sikugun=" + test
    return url

def get_num_of_page(html):
    root = lxml.html.fromstring(html)
    select = root.cssselect("select")   
    pages = select[0]
    num_of_pages = len(pages)
    return num_of_pages

def scrape_page(html):
    root = lxml.html.fromstring(html)
    trs = root.cssselect(".searchResult tr")
    
    for tr in trs[1:]:
        data = {
            "TDS number":tr[0].text,
            "company":tr[1].cssselect(".company")[0].text,
            "address":tr[1].cssselect(".companyPlace")[0].text,
            "industry":tr[2].text
        }
        scraperwiki.sqlite.save(unique_keys=['TDS number'], data=data)
    
#######################
##       Start program       ##
#######################


#step1: get the number of pages to loop through
url = build_url(BASE_URL,1,SEARCH_ADDRESS)
html = scraperwiki.scrape(url)
page_nums = get_num_of_page(html)
print "Number of pages to scrape: " + str(page_nums)

#step2: scrape the pages and save to database
for i in range(1,page_nums+1):
    url = build_url(BASE_URL,i,SEARCH_ADDRESS)
    html = scraperwiki.scrape(url)
    scrape_page(html)


#see http://docs.python.org/2/library/urllib.html#examples
