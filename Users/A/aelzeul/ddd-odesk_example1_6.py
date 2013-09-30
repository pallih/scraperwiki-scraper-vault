import scraperwiki
import lxml.html
import re;
from datetime import datetime
from pprint import pprint as pp

domain = "http://www.groceryretailonline.com"
contents_base = "http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors"

scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Mikhail Malyshev")

def scrape_site():
    page_num = 0

    while True:
        # Get next contents page.
        page_num += 1
        url = contents_base + '?Page=' + str(page_num)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        # Get list of companies at this page.
        companies = root.cssselect('div#col1_content div.company')

        if len(companies) == 0:
            # Contents is over.
            print 'SPIDER-STOP'
            break

        # Retrieve link to each company and scrape it.
        for c in companies:
            rel_link = c.cssselect('a')[0].attrib.get('href')
            abs_link = domain + rel_link
            scrape_info(abs_link)
            #break                                   # [Debug] Scrape only 1 entry

        #if page_num == 1:                           # [Debug] Scrape only 1 contents page
        #    break                                   # [Debug]


def scrape_info(url):
    #print "Scraping " + url + " ..."

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    # Initalize all fields with empty string
    fields = ['emails', 'companyname', 'dba', 'website', 'categories',
        'maincategory', 'city', 'state', 'zip', 'country', 'address',
        'address2', 'boothnum', 'sourceurl', 'salesmethod', 'phonenumber',
        'faxnumber', 'contact1first', 'contact1last', 'contact1title',
        'contact2first', 'contact2last', 'contact2title', 'contact3first',
        'contact3last', 'contact3title', 'yearfounded', 'description',
        'certifications', 'contactlink']
    data = dict.fromkeys(fields, '')

    # Scrape
    data['datescraped'] = datetime.strftime(datetime.now(), '%Y-%m-%d')
    data['sourceurl'] = url
    
    main_block = root.cssselect('div#col1_content')[0]
    children = list(main_block)
    #pp(zip(range(len(children)),                      # [Debug] Output
    #       [c.tag for c in children],                 # [Debug]
    #       [text(c) for c in children]), width=200)   # [Debug]
    
    # Common
    data['companyname'] = clean(text(children[1]))
    data['address'] = clean(text(children[2]))
    child3 = text(children[3]).split('\r\n')
    data['city'] = clean(child3[1]).rstrip(',')
    data['state'] = clean(child3[2])
    data['zip'] = clean(child3[3])
    data['country'] = clean(text(children[4]))
    data['phonenumber'] = clean(text(children[6]).lstrip('Phone: '))
    data['faxnumber'] = clean(text(children[8]).lstrip('Fax: '))
    child10 = text(children[10]).lstrip('Contact:').split(' ', 1)
    data['contact1first'] = clean(child10[0])
    data['contact1last'] = clean(child10[1])
    
    # Categories
    products = children[13]
    main_categories = products.xpath('.//span[@class="toplevelcategory"]')
    end_categories = products.xpath('.//ul[not(ul)]//span')
    main_categories = [clean(text(c)) for c in main_categories]
    end_categories = [clean(text(c)) for c in end_categories]
    data['maincategory'] = ', '.join(main_categories)
    data['categories'] = ', '.join(end_categories)

    #pp(data)                                          # [Debug] output
    scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=data)

# Return element as text.
def text(element):
    return lxml.html.tostring(element, method='text', encoding=unicode)

# Trim whitespace and encode before uploading.
def clean(string):
    return string.strip().encode('utf-8')

scrape_site()

import scraperwiki
import lxml.html
import re;
from datetime import datetime
from pprint import pprint as pp

domain = "http://www.groceryretailonline.com"
contents_base = "http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors"

scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Mikhail Malyshev")

def scrape_site():
    page_num = 0

    while True:
        # Get next contents page.
        page_num += 1
        url = contents_base + '?Page=' + str(page_num)
        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        # Get list of companies at this page.
        companies = root.cssselect('div#col1_content div.company')

        if len(companies) == 0:
            # Contents is over.
            print 'SPIDER-STOP'
            break

        # Retrieve link to each company and scrape it.
        for c in companies:
            rel_link = c.cssselect('a')[0].attrib.get('href')
            abs_link = domain + rel_link
            scrape_info(abs_link)
            #break                                   # [Debug] Scrape only 1 entry

        #if page_num == 1:                           # [Debug] Scrape only 1 contents page
        #    break                                   # [Debug]


def scrape_info(url):
    #print "Scraping " + url + " ..."

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    # Initalize all fields with empty string
    fields = ['emails', 'companyname', 'dba', 'website', 'categories',
        'maincategory', 'city', 'state', 'zip', 'country', 'address',
        'address2', 'boothnum', 'sourceurl', 'salesmethod', 'phonenumber',
        'faxnumber', 'contact1first', 'contact1last', 'contact1title',
        'contact2first', 'contact2last', 'contact2title', 'contact3first',
        'contact3last', 'contact3title', 'yearfounded', 'description',
        'certifications', 'contactlink']
    data = dict.fromkeys(fields, '')

    # Scrape
    data['datescraped'] = datetime.strftime(datetime.now(), '%Y-%m-%d')
    data['sourceurl'] = url
    
    main_block = root.cssselect('div#col1_content')[0]
    children = list(main_block)
    #pp(zip(range(len(children)),                      # [Debug] Output
    #       [c.tag for c in children],                 # [Debug]
    #       [text(c) for c in children]), width=200)   # [Debug]
    
    # Common
    data['companyname'] = clean(text(children[1]))
    data['address'] = clean(text(children[2]))
    child3 = text(children[3]).split('\r\n')
    data['city'] = clean(child3[1]).rstrip(',')
    data['state'] = clean(child3[2])
    data['zip'] = clean(child3[3])
    data['country'] = clean(text(children[4]))
    data['phonenumber'] = clean(text(children[6]).lstrip('Phone: '))
    data['faxnumber'] = clean(text(children[8]).lstrip('Fax: '))
    child10 = text(children[10]).lstrip('Contact:').split(' ', 1)
    data['contact1first'] = clean(child10[0])
    data['contact1last'] = clean(child10[1])
    
    # Categories
    products = children[13]
    main_categories = products.xpath('.//span[@class="toplevelcategory"]')
    end_categories = products.xpath('.//ul[not(ul)]//span')
    main_categories = [clean(text(c)) for c in main_categories]
    end_categories = [clean(text(c)) for c in end_categories]
    data['maincategory'] = ', '.join(main_categories)
    data['categories'] = ', '.join(end_categories)

    #pp(data)                                          # [Debug] output
    scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=data)

# Return element as text.
def text(element):
    return lxml.html.tostring(element, method='text', encoding=unicode)

# Trim whitespace and encode before uploading.
def clean(string):
    return string.strip().encode('utf-8')

scrape_site()

