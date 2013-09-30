import scraperwiki

# Blank Python
# A scraper to collect words with a query *see bottom

import scraperwiki
import requests
import lxml.html

#this function returns all the subdomains in the US.
def get_target_subdomains():
    areas = {}
    url = 'http://www.craigslist.org/about/sites/'
    dom = get_page_dom(url)
    if dom is not None:
        subdomains = dom.cssselect('.colmask')[0].cssselect("a")
        if len(subdomains):
            for domain in subdomains:
                area = get_element_or_none(domain, 'a')
                url = get_element_or_none(domain, 'a', 'href')
                areas[area] = url
            return areas

# this function gives us the url of all the pages conatining our search result.
# every page holds a maximum of 100 results. and no search return more than 2500 hits
def get_url_que(url):
    url_que = [url]
    dom = get_page_dom(url)
    if dom is not None:
        additional_pages = dom.cssselect("span.pagelinks")
        if len(additional_pages):
            pages = additional_pages[0].cssselect("a")
            print pages
            for page in pages:
                page_url = get_element_or_none(page, "a", "href")
                url_que.append(page_url)
    else:
        print "(1) request to %s failed" % url
    return url_que
    

def scrape_ads(query, areas):
    ads = []
    for subdomain_area, subdomain_url in areas.items():
        ad_count = 0
        queryUrl = subdomain_url + "/search/?areaID=&subAreaID=&query="+query+"&catAbb=sss"
        # here we get all the urls that hold our search result, page 1 , 2, 3 etc. and we save them.
        url_que = get_url_que(queryUrl)

        # now that we have a list of pages containing our search resu lt lets
        # loop through all of them to collect informaiton and their individual url
        for url in url_que:
            dom = get_page_dom(url)
            if dom is not None:
                targetList = dom.cssselect("p.row")
                for target in targetList:
                    ad = {
                        "url": get_element_or_none(target, "span.pl a", "href"),
                        "title": get_element_or_none(target, "span.pl a"),
                        "price": get_element_or_none(target, "span.price"),
                        "category": get_element_or_none(target, "span.l2 a.gc"),
                        "date": get_element_or_none(target, "span.pl span.date"),
                        "area_from_subdomain": subdomain_area,
                        "query": query
                    }
                    # lets make sure we got a URL and not an URI
                    if "http://" not in ad["url"]:
                        ad["url"] = subdomain_url + ad["url"]
                        print "uri changed to url. %s" % ad["url"]
                    #let get some more info inside the article
                    dom2 = get_page_dom(ad["url"])
                    if dom2 is not None:
                        ad["posting_body"] = get_element_or_none(dom2, "#postingbody"),
                        ad["blurbs"] = get_element_or_none(dom2, "ul.blurbs"),
                        ad["map_adress"] = get_element_or_none(dom2, "p.mapadress"),
                        ad["map_link"] = get_element_or_none(dom2, "p.mapadress a", "href"),
                        ad["img_link"] = get_element_or_none(dom2, "#iwi", "src")
                    else:
                        print "request to %s failed" % ad["url"]
                    # lets save this ad to our list of ads
                    ads.append(ad)
                    ad_count += 1
            else:
                print "(2) request to %s failed" % url

        # lets save everytime we're finished with one of the subdomains
        scraperwiki.sqlite.save(['url'], ads)
        print "saving results. scraped %s ads, from %s pages, from the subdomain: %s, with the query: %s" % (ad_count, len(url_que), subdomain_area, query)

    # lets printout when were finished scraping
    print "scraping complete. total ads scraped: %s" % len(ads)
            

# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text_content()

def get_page_dom(url, verify=False):
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            dom = lxml.html.fromstring(r.text)
            return dom
        else:
            return None
    except:
        return None
    

# insert the query here try it out on the real website first, have fun
subdomain_urls = get_target_subdomains()
scrape_ads("washing+machine", subdomain_urls)import scraperwiki

# Blank Python
# A scraper to collect words with a query *see bottom

import scraperwiki
import requests
import lxml.html

#this function returns all the subdomains in the US.
def get_target_subdomains():
    areas = {}
    url = 'http://www.craigslist.org/about/sites/'
    dom = get_page_dom(url)
    if dom is not None:
        subdomains = dom.cssselect('.colmask')[0].cssselect("a")
        if len(subdomains):
            for domain in subdomains:
                area = get_element_or_none(domain, 'a')
                url = get_element_or_none(domain, 'a', 'href')
                areas[area] = url
            return areas

# this function gives us the url of all the pages conatining our search result.
# every page holds a maximum of 100 results. and no search return more than 2500 hits
def get_url_que(url):
    url_que = [url]
    dom = get_page_dom(url)
    if dom is not None:
        additional_pages = dom.cssselect("span.pagelinks")
        if len(additional_pages):
            pages = additional_pages[0].cssselect("a")
            print pages
            for page in pages:
                page_url = get_element_or_none(page, "a", "href")
                url_que.append(page_url)
    else:
        print "(1) request to %s failed" % url
    return url_que
    

def scrape_ads(query, areas):
    ads = []
    for subdomain_area, subdomain_url in areas.items():
        ad_count = 0
        queryUrl = subdomain_url + "/search/?areaID=&subAreaID=&query="+query+"&catAbb=sss"
        # here we get all the urls that hold our search result, page 1 , 2, 3 etc. and we save them.
        url_que = get_url_que(queryUrl)

        # now that we have a list of pages containing our search resu lt lets
        # loop through all of them to collect informaiton and their individual url
        for url in url_que:
            dom = get_page_dom(url)
            if dom is not None:
                targetList = dom.cssselect("p.row")
                for target in targetList:
                    ad = {
                        "url": get_element_or_none(target, "span.pl a", "href"),
                        "title": get_element_or_none(target, "span.pl a"),
                        "price": get_element_or_none(target, "span.price"),
                        "category": get_element_or_none(target, "span.l2 a.gc"),
                        "date": get_element_or_none(target, "span.pl span.date"),
                        "area_from_subdomain": subdomain_area,
                        "query": query
                    }
                    # lets make sure we got a URL and not an URI
                    if "http://" not in ad["url"]:
                        ad["url"] = subdomain_url + ad["url"]
                        print "uri changed to url. %s" % ad["url"]
                    #let get some more info inside the article
                    dom2 = get_page_dom(ad["url"])
                    if dom2 is not None:
                        ad["posting_body"] = get_element_or_none(dom2, "#postingbody"),
                        ad["blurbs"] = get_element_or_none(dom2, "ul.blurbs"),
                        ad["map_adress"] = get_element_or_none(dom2, "p.mapadress"),
                        ad["map_link"] = get_element_or_none(dom2, "p.mapadress a", "href"),
                        ad["img_link"] = get_element_or_none(dom2, "#iwi", "src")
                    else:
                        print "request to %s failed" % ad["url"]
                    # lets save this ad to our list of ads
                    ads.append(ad)
                    ad_count += 1
            else:
                print "(2) request to %s failed" % url

        # lets save everytime we're finished with one of the subdomains
        scraperwiki.sqlite.save(['url'], ads)
        print "saving results. scraped %s ads, from %s pages, from the subdomain: %s, with the query: %s" % (ad_count, len(url_que), subdomain_area, query)

    # lets printout when were finished scraping
    print "scraping complete. total ads scraped: %s" % len(ads)
            

# A handy function to get text or attributes out of HTML elements
def get_element_or_none(context, css, attribute=None):
    try:
        element = context.cssselect(css)[0]
    except:
        return None
    else:
        if attribute:
            return element.get(attribute)
        else:
            return element.text_content()

def get_page_dom(url, verify=False):
    try:
        r = requests.get(url, verify=False)
        if r.status_code == 200:
            dom = lxml.html.fromstring(r.text)
            return dom
        else:
            return None
    except:
        return None
    

# insert the query here try it out on the real website first, have fun
subdomain_urls = get_target_subdomains()
scrape_ads("washing+machine", subdomain_urls)