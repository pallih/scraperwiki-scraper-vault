# -*- coding: utf-8 -*-
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

"""
Url settings for scraping
"""
base_url = u"http://ja.wikipedia.org/wiki/%E8%89%B2%E5%90%8D%E4%B8%80%E8%A6%A7"


soup = BeautifulSoup(scraperwiki.scrape(base_url))
print soup
print "hoge"

"""
Scraping
re_rating = re.compile("reviewer-rating")

for page in range(page_min, page_max):
    # generating base url
    base_url= "http://www.cosme.net/product/product_id/%d/reviews" % product_id
    if page != 1:
        base_url += "/p/%d" % page

    # getting url
    soup = BeautifulSoup(scraperwiki.scrape(base_url).decode('sjis', "ignore"))

    # parsing
    for t in soup.findAll(attrs={"class":"review-sec"}):
        data = {}
        data['age'] = t.li.text
        data['rating'] = t.find('p', attrs={"class":re_rating}).text
        data['skin'] = t.li.findNextSibling('li').text
        data['review'] = t.find('p', attrs={"class":"read"}).text
        scraperwiki.sqlite.save(["age", 'skin', 'review'], data)
"""
# -*- coding: utf-8 -*-
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

"""
Url settings for scraping
"""
base_url = u"http://ja.wikipedia.org/wiki/%E8%89%B2%E5%90%8D%E4%B8%80%E8%A6%A7"


soup = BeautifulSoup(scraperwiki.scrape(base_url))
print soup
print "hoge"

"""
Scraping
re_rating = re.compile("reviewer-rating")

for page in range(page_min, page_max):
    # generating base url
    base_url= "http://www.cosme.net/product/product_id/%d/reviews" % product_id
    if page != 1:
        base_url += "/p/%d" % page

    # getting url
    soup = BeautifulSoup(scraperwiki.scrape(base_url).decode('sjis', "ignore"))

    # parsing
    for t in soup.findAll(attrs={"class":"review-sec"}):
        data = {}
        data['age'] = t.li.text
        data['rating'] = t.find('p', attrs={"class":re_rating}).text
        data['skin'] = t.li.findNextSibling('li').text
        data['review'] = t.find('p', attrs={"class":"read"}).text
        scraperwiki.sqlite.save(["age", 'skin', 'review'], data)
"""
