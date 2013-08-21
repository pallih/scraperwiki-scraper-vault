# -*- coding: utf8 -*-

import scraperwiki
import lxml.html
from lxml.cssselect import CSSSelector
import mechanize
import random
import re
import sys

# randomize list
def shuffle(l):
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

# returns a randomly selected user agent strings
def get_random_ua_string():
    ua = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MRA 4.6 (build 01425))',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; de; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0'
    ]
    ua = shuffle(ua)
    return ua[0]

browser = mechanize.Browser()
browser.addheaders = [("User-agent", get_random_ua_string())]
browser.set_handle_robots(False)

product_name_selector = CSSSelector("table tr td.cellborder a.b[href*='.idealo.de/preisvergleich/OffersOfProduct/'], table.fs13 tr td div a.fs13[href*='.idealo.de/preisvergleich/OffersOfProduct/']")
# here we get a bug, because :contains converts to a lower-case function in XPath, which then contains the whole website content to be comparable in an case-insensitive way.
# if this string contains special characters not allowed as input to lower-case() we get an error -> no :contains!
#parent_categories_selector = CSSSelector("div#breadcrumb a.path:not(:contains(Preisvergleich))")
parent_categories_selector = CSSSelector("div#breadcrumb a.path")
category_selector = CSSSelector("table#cont_table tr td table tr td table tr td table tr td.headlines h2 strong")
#next_page_selector = CSSSelector("div#pagination a.page-block:contains(weiter)") # for some werd reason this gives a XPathFunctionError on some pages (?)
next_page_selector = CSSSelector("div#pagination a.page-block") # workaround: take the last element in this list by hand
product_id_pattern = re.compile(r'/preisvergleich/OffersOfProduct/(\d+)_.*\.html')
category_pattern = re.compile(r'http://www[0-9]*.idealo.de/preisvergleich/ProductCategory/([0-9]+)\.html')

# category scraper
def scrape_categories():
    subsitemap_link_selector = CSSSelector("a[href*='.idealo.de/preisvergleich/S-Sitemap/']")
    category_links_selector = CSSSelector("a[href*='.idealo.de/preisvergleich/ProductCategory/']")
    url = "http://www.idealo.de/preisvergleich/Sitemap.html"
    response = browser.open(url)
    html = response.read()
    doc = lxml.html.fromstring(html)
    doc.make_links_absolute(url)
    subsitemap_urls = [ node.get('href') for node in subsitemap_link_selector(doc) ]
    for url in subsitemap_urls:
        response = browser.open(url)
        html = response.read()
        doc = lxml.html.fromstring(html)
        doc.make_links_absolute(url)

        for category_link in category_links_selector(doc):
            category_url = category_link.get('href')
            category_match = category_pattern.search(category_url)
            if category_match:
                record = { 'id' : category_match.group(1), 'nextUrl' : category_url, 'name' : '' }
                try:
                    scraperwiki.sqlite.save(unique_keys=["id"], data=record, table_name="categories")
                    print "SAVE: ", record
                except:
                    print "Could not write record", record

# product list scraper
def scrape_product_list_page(id, url):
    print "NEW CATEGORY: ", url
    response = browser.open(url)
    html = response.read()
    doc = lxml.html.fromstring(html)
    doc.make_links_absolute(url)

    category_match = category_pattern.search(url)
    if category_match:
        # this is the first page of a category list -> here we have the correct category title
        categories = [x.text_content().strip() for x in parent_categories_selector(doc)]
        del categories[0] # remove the first element (workaround due to ":contains" bug)
        print categories
        print category_selector(doc).pop().text_content()
        categories.append(category_selector(doc).pop().text_content().strip())
        categories_string = ";".join(categories)
        record = { 'id' : id, 'nextUrl' : url, 'name' : categories_string }
        try:
            #scraperwiki.sqlite.save(unique_keys=["id"], data=record, table_name="categories")
            scraperwiki.sqlite.execute("update `categories` set `name`=? where `id`=?", (categories_string, id));
            print "SAVE: ", record
        except:
            print "Could not write record", record

    for product_node in product_name_selector(doc):
        product_url = product_node.get('href')
        product_id_match = product_id_pattern.search(product_url)
        if product_id_match:
            product_id = product_id_match.group(1).strip()
            record = { 'id' : product_id, 'name' : product_node.text_content().strip(), 'category_id' : id }
            try:
                scraperwiki.sqlite.save(unique_keys=["id"], data=record)
                print "SAVE: ", record
            except:
                print "Could not write record: ", record
        else:
            print "Could not extract product id: ", product_url

    print next_page_selector.path
    next_page_nodes = next_page_selector(doc)
    next_page = ""
    if len(next_page_nodes) > 0 and "weiter" in next_page_nodes[-1].text_content():
        next_page = next_page_nodes[-1].get('href')
    return next_page

# general product scraper
def scrape_products():
    result = scraperwiki.sqlite.execute("select `id`, `nextUrl` from `categories` where `nextUrl` != '' AND `id` in (18357,14012,18556,12073,13734,13852,18910,15192,15061,13892,14752,18912,13072,14972,18909,18911,18913)")
    #result = scraperwiki.sqlite.execute("select `id`, `nextUrl` from `categories` where `nextUrl` != ''")
    for row in result.get('data'):
        cat_id = row[0]
        next_url = row[1]
        #print scraperwiki.sqlite.execute("update `categories` set `name`=? where `id`=?", ("test", 6754));
        #print scraperwiki.sqlite.execute("select `name` from `categories` where `id`=6754")
        #sys.exit(0)
        while next_url != "":
            next_url = scrape_product_list_page(cat_id, next_url)
            print "NEXT URL: ", next_url
            scraperwiki.sqlite.execute("update `categories` set `nextUrl`=? where `id`=?", (next_url, cat_id));

#url = "http://www1.idealo.de/preisvergleich/ProductCategory/18416.html"

#scrape_categories()
#print scrape_product_list(url)
scrape_products()
