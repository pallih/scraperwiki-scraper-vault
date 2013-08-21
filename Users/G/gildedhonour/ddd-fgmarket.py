import scraperwiki
import lxml.html
import re 
import datetime

base_domain_url = "http://www.fgmarket.com/"

def print_delimeter():
    print ("--------------------------------------------------------")

def scrape_premium_company(company_item_html, current_page):
    print ("data_scraped => %s" % datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"))
    company_name = company_item_html.cssselect("div.prem-header h3.listingname a")[0]
    print("company_name => %s, page => %d " % (company_name.text, current_page))
    
    #company profile url
    company_url_href = company_item_html.cssselect("div.prem-body div.website div.profile-link a.vendorInfo")[0].get('href')
    company_base_domain_url = base_domain_url[0:len(base_domain_url)-1] + company_url_href
    
    
    #company profile details
    company_base_domain_url_root = lxml.html.fromstring(scraperwiki.scrape(company_base_domain_url))
    web_site_link1 = company_base_domain_url_root.cssselect("div.website-link a")[0]
    
    
    #concrete address
    address_html_raw = company_item_html.cssselect("div.prem-body div.addresses div.address")[0]
    address_additional = address_html_raw.xpath('br[1]/preceding-sibling::node()')[0]

    #address
    address_main = address_html_raw.xpath('br[1]/following-sibling::node()')[0] 
    matches = re.match(r'(^.+),\s+(\S{2})\s+(\d+)', address_main, re.M | re.I)
    if matches:
        city = matches.group(1) 
        state = matches.group(2)
        zip = matches.group(3) 
    
    #phone number and fax
    phone_number = (company_item_html.cssselect("div.prem-body table.phonenumbers")[0]).text
    phone_number_raw = (company_item_html.cssselect("div.prem-body table.phonenumbers")[0]).text_content()
    fax_number = ''
    matches = re.match(r'.+Fax:(.+)', phone_number_raw, re.M | re.I)
    if matches:
        fax_number = matches.group(1)


    #desctiption
    description_html_raw = lxml.html.fromstring(scraperwiki.scrape(company_base_domain_url))
    description_html = description_html_raw.cssselect("div#spotlight")
    description_plain = ''
    if len(description_html) > 0:
        description_plain = description_html[0].text_content()[0:1000]

    #contact_link   
    contact_link = company_base_domain_url + "#contact_form"

    #categories
    root_company_html_raw = lxml.html.fromstring(scraperwiki.scrape(company_base_domain_url))
    categories_list = []
    for item in root_company_html_raw.xpath("//div[@class='box profile-categories']/ul/li"):
        try:
            categories_list.append(item.text.strip())
        except AttributeError:
            pass

    
    #dictionary of scraped data
    data = {
        'datescraped'   : datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"),
        'companyname'   : company_name.text,
        'sourceurl'     : company_base_domain_url,
        'website'       : web_site_link1.text,
        'maincategory'  : ", ".join(str(item) for item in categories_list),
        'city'          : city,
        'state'         : state,
        'zip'           : zip,
        'country'       : "USA",
        'address'       : address_additional,
        'phonenumber'   : phone_number,
        'faxnumber'     : fax_number,
        'description'   : description_plain,
        'contactlink'   : company_base_domain_url + "#contact_form"
    }

    scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=data)
    print_delimeter()

def get_first_page_url(category_url):
    return base_domain_url + category_url + "?page=1&sortby=name"

def get_next_page_url(category_url, page_url):
    return base_domain_url + category_url + page_url

def next_page_exists(page_html_raw):
    next_page_html_raw = page_html_raw.cssselect("div.category-content div.category-listings nav.pagination a")[-1]
    return next_page_html_raw.text_content().lower() == "next"  

def scrape_fgmarket():
    scraperwiki.sqlite.save_var("source", "www.fgmarket.com ")
    scraperwiki.sqlite.save_var("author", "Alex Maslakov") 
    root_html = lxml.html.fromstring(scraperwiki.scrape(base_domain_url))
    
    #for each outer category
    for category_item_html in root_html.cssselect("div.home-section div.home-content div.box.last-content div.box-columns div.box-column-half ul.box-column-half-inner.home-category-set  li a.home-category-main")[0:1]:
        first_page_url = get_first_page_url(category_item_html.get('href'))
        
        #parse the 1st page category html
        first_page_html_raw = lxml.html.fromstring(scraperwiki.scrape(first_page_url))
        
        #scrape each company on the first page
        premium_companies_html = first_page_html_raw.cssselect("div.category-content div.category-listings div.prem-listing")
        if len(premium_companies_html) > 0:
            for company_item_html in premium_companies_html:
                scrape_premium_company(company_item_html, 1)

        #scrape each company on the other pages
        next_page_html_raw = first_page_html_raw
        counter = 2
        while next_page_exists(next_page_html_raw):
            #next page url
            next_page_url_html_raw = next_page_html_raw.cssselect("div.category-content div.category-listings nav.pagination a")[-1]
            next_page_url = get_next_page_url(category_item_html.get('href'), next_page_url_html_raw.get('href'))
            next_page_html_raw = lxml.html.fromstring(scraperwiki.scrape(next_page_url))

            #scrape each company on the first page
            for company_item_html in next_page_html_raw.cssselect("div.category-content div.category-listings div.prem-listing"):
                scrape_premium_company(company_item_html, counter)
                       
            counter += 1 

   
scrape_fgmarket()