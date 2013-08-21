# -*- coding: utf-8 -*-
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

"""
Url settings for scraping
"""
product_id = 2887439
page_min = 0
page_max = 72


"""
Scraping
"""
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
