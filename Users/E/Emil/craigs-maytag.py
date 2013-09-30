import scraperwiki

# Blank Python
# A scraper to collect words with a query *see bottom

import scraperwiki
import requests
import lxml.html

#this function returns all the subdomains in the US.
def get_target_subdomains():
    areas = {}
    r = requests.get('http://www.craigslist.org/about/sites/', verify=False)
    if r.status_code==200:
        dom = lxml.html.fromstring(r.text)
        subdomains = dom.cssselect('.box')[0].cssselect("a")
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
    r = requests.get(url, verify=False)
    if r.status_code == 200:
        dom = lxml.html.fromstring(r.text)
        additional_pages = dom.cssselect("span.pagelinks")
        if len(additional_pages):
            pages = additional_pages[0].cssselect("a")
            for page in pages:
                page_url = get_element_or_none(page, "a", "href")
                url_que.append(page_url)
    else:
        print "request to %s failed" % url
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
            try:
                r = requests.get(url, verify=False)
                if r.status_code == 200:
                    dom = lxml.html.fromstring(r.text)
                    targetList = dom.cssselect(".srch.row")
                    for target in targetList:
                        ad = {
                            "url": get_element_or_none(target, "span.pl a", "href"),
                            "title": get_element_or_none(target, "span.pl a"),
                            "price": get_element_or_none(target, "span.pl a span.itemprice"),
                            "category": get_element_or_none(target, "small.gc a"),
                            "contains": get_element_or_none(target, "span.itempx span.p"),
                            "date": get_element_or_none(target, "span.itemdate"),
                            "area_from_subdomain": subdomain_area,
                            "location": get_element_or_none(target, "span.itempn small"),
                            "query": query
                        }
                        #let get some more info inside the article
                        r2 = requests.get(ad["url"], verify=False)
                        if r2.status_code == 200:
                            dom2 = lxml.html.fromstring(r2.text)
                            ad["posting_body"] = get_element_or_none(dom2, "#postingbody"),
                            ad["blurbs"] = get_element_or_none(dom2, "ul.blurbs"),
                            ad["map_adress"] = get_element_or_none(dom2, "p.mapadress"),
                            ad["map_link"] = get_element_or_none(dom2, "p.mapadress a", "href"),
                            ad["img_link"] = get_element_or_none(dom2, "#iwi", "src")
                        else:
                            print "request to %s failed" % ad[url]
                        # lets save this ad to our list of ads
                        ads.append(ad)
                        ad_count += 1
                else:
                    print "request to %s failed" % url
            except:
                print "error1"
                pass

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

def get_pagelinks_or_none(context, css):
    try:
        element = context.cssselect(css)
    except:
        return None
    

# insert the query here try it out on the real website first, have fun
subdomain_urls = get_target_subdomains()
scrape_ads("maytag", subdomain_urls)
import scraperwiki

# Blank Python
# A scraper to collect words with a query *see bottom

import scraperwiki
import requests
import lxml.html

#this function returns all the subdomains in the US.
def get_target_subdomains():
    areas = {}
    r = requests.get('http://www.craigslist.org/about/sites/', verify=False)
    if r.status_code==200:
        dom = lxml.html.fromstring(r.text)
        subdomains = dom.cssselect('.box')[0].cssselect("a")
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
    r = requests.get(url, verify=False)
    if r.status_code == 200:
        dom = lxml.html.fromstring(r.text)
        additional_pages = dom.cssselect("span.pagelinks")
        if len(additional_pages):
            pages = additional_pages[0].cssselect("a")
            for page in pages:
                page_url = get_element_or_none(page, "a", "href")
                url_que.append(page_url)
    else:
        print "request to %s failed" % url
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
            try:
                r = requests.get(url, verify=False)
                if r.status_code == 200:
                    dom = lxml.html.fromstring(r.text)
                    targetList = dom.cssselect(".srch.row")
                    for target in targetList:
                        ad = {
                            "url": get_element_or_none(target, "span.pl a", "href"),
                            "title": get_element_or_none(target, "span.pl a"),
                            "price": get_element_or_none(target, "span.pl a span.itemprice"),
                            "category": get_element_or_none(target, "small.gc a"),
                            "contains": get_element_or_none(target, "span.itempx span.p"),
                            "date": get_element_or_none(target, "span.itemdate"),
                            "area_from_subdomain": subdomain_area,
                            "location": get_element_or_none(target, "span.itempn small"),
                            "query": query
                        }
                        #let get some more info inside the article
                        r2 = requests.get(ad["url"], verify=False)
                        if r2.status_code == 200:
                            dom2 = lxml.html.fromstring(r2.text)
                            ad["posting_body"] = get_element_or_none(dom2, "#postingbody"),
                            ad["blurbs"] = get_element_or_none(dom2, "ul.blurbs"),
                            ad["map_adress"] = get_element_or_none(dom2, "p.mapadress"),
                            ad["map_link"] = get_element_or_none(dom2, "p.mapadress a", "href"),
                            ad["img_link"] = get_element_or_none(dom2, "#iwi", "src")
                        else:
                            print "request to %s failed" % ad[url]
                        # lets save this ad to our list of ads
                        ads.append(ad)
                        ad_count += 1
                else:
                    print "request to %s failed" % url
            except:
                print "error1"
                pass

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

def get_pagelinks_or_none(context, css):
    try:
        element = context.cssselect(css)
    except:
        return None
    

# insert the query here try it out on the real website first, have fun
subdomain_urls = get_target_subdomains()
scrape_ads("maytag", subdomain_urls)
