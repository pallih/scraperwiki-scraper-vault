# -*- coding: utf-8 -*-
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

re_rating = re.compile("reviewer-rating")


"""
Url settings for scraping
"""
product_id = 10002735
review_max = 10

"""
Scraping
"""

# generating first review's url

base_url= "http://www.cosme.net/product/product_id/%d/reviews" % product_id
soup = BeautifulSoup(scraperwiki.scrape(base_url).decode('sjis', "ignore"))

div = soup.find(attrs={"class":"review-sec"})
a = soup.find('a', attrs={"class":'cmn-viewmore'})
review_url = str(a.attrMap['href'])


# getting reviews iteratively

review_count = 1

while 1:
    # scraping review's data
    print "getting review: %d, url: %s" % (review_count, review_url)
    review_page_soup = BeautifulSoup(scraperwiki.scrape(review_url).decode('sjis', "ignore"))
    div = review_page_soup.find(attrs={"class":"review-sec"})
    data = {}
    data['product_id'] = product_id
    data['age'] = div.li.text
    data['rating'] = div.find('p', attrs={"class":re_rating}).text
    data['skin'] = div.li.findNextSibling('li').text
    data['review'] = div.find('p', attrs={"class":"read"}).text
    scraperwiki.sqlite.save(["product_id", "age", 'skin', 'review'], data)

    # getting next review url
    next_url_li = review_page_soup.find("li", attrs={"class":"next"})
    review_count += 1

    if review_count > review_max:
        break
    elif next_url_li:
        review_url = next_url_li.a.attrs[0][1]
    else:
        break
# -*- coding: utf-8 -*-
import re
import scraperwiki
from BeautifulSoup import BeautifulSoup

re_rating = re.compile("reviewer-rating")


"""
Url settings for scraping
"""
product_id = 10002735
review_max = 10

"""
Scraping
"""

# generating first review's url

base_url= "http://www.cosme.net/product/product_id/%d/reviews" % product_id
soup = BeautifulSoup(scraperwiki.scrape(base_url).decode('sjis', "ignore"))

div = soup.find(attrs={"class":"review-sec"})
a = soup.find('a', attrs={"class":'cmn-viewmore'})
review_url = str(a.attrMap['href'])


# getting reviews iteratively

review_count = 1

while 1:
    # scraping review's data
    print "getting review: %d, url: %s" % (review_count, review_url)
    review_page_soup = BeautifulSoup(scraperwiki.scrape(review_url).decode('sjis', "ignore"))
    div = review_page_soup.find(attrs={"class":"review-sec"})
    data = {}
    data['product_id'] = product_id
    data['age'] = div.li.text
    data['rating'] = div.find('p', attrs={"class":re_rating}).text
    data['skin'] = div.li.findNextSibling('li').text
    data['review'] = div.find('p', attrs={"class":"read"}).text
    scraperwiki.sqlite.save(["product_id", "age", 'skin', 'review'], data)

    # getting next review url
    next_url_li = review_page_soup.find("li", attrs={"class":"next"})
    review_count += 1

    if review_count > review_max:
        break
    elif next_url_li:
        review_url = next_url_li.a.attrs[0][1]
    else:
        break
