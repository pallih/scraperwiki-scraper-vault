# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here: 
# 
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description
# use companyname as the unique key when writing to the database

# please name the scrapers ddd-<<short identifier>>, ie ddd-housewares-1

# use scraperwiki.sqlite.save_var("source", value) to save a string of the name of the source you scraped
# example scraperwiki.sqlite.save_var("source", "NAFST - Fancy Food Show")

# use scraperwiki.sqlite.save_var("author", value) to save your name
# example scraperwiki.sqlite.save_var("author", " Clint Eastwood")

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!

# if you need to use a proxy (some sites block the ip of scraperwiki) - please use the following code
#proxy_url = "72.77.197.214:19629" (http://www.xroxy.com/proxy-country-US.htm has good ones to use)
#proxy = urllib2.ProxyHandler({'http': proxy_url})
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; v' + str(random.random())
#opener = urllib2.build_opener(proxy)
#opener.addheaders = [('User-agent', user_agent)]
#page_html = opener.open(url).read()

import re;

def remove_html(string):
    return re.sub("<.*?>", "", string)

def clean(string):
    return safestr(final_clean(strip_non_text(remove_html(string.strip()))))

def strip_non_text(string):
    return re.sub("\n|\r|&\w{3};|<.*?>",",",string)

def final_clean(string):
    return re.sub("[, ]{2,10}", ",", string)

def split_and_clean(string, delim):
    return ",".join(re.sub("[^a-zA-Z ]", "", rec, re.I) for rec in [clean(rec) for rec in string.split(delim) if rec.strip() != ""])

SAFESTR_RX = re.compile("^u\'(.+)\'$")
def safestr(string):
    try:
        return english_string(string).encode('utf-8', 'replace')
    except:
        return re.sub(SAFESTR_RX, '\1', repr(string))

# example scraper below

import scraperwiki
import lxml.html
import re
domaine = 'http://www.groceryretailonline.com'
s_url = 'http://www.groceryretailonline.com/BuyersGuide.mvc/CompanyDetail/452035'

def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    print html_content
    

scrape_site(s_url, domaine)

# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here: 
# 
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description
# use companyname as the unique key when writing to the database

# please name the scrapers ddd-<<short identifier>>, ie ddd-housewares-1

# use scraperwiki.sqlite.save_var("source", value) to save a string of the name of the source you scraped
# example scraperwiki.sqlite.save_var("source", "NAFST - Fancy Food Show")

# use scraperwiki.sqlite.save_var("author", value) to save your name
# example scraperwiki.sqlite.save_var("author", " Clint Eastwood")

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!

# if you need to use a proxy (some sites block the ip of scraperwiki) - please use the following code
#proxy_url = "72.77.197.214:19629" (http://www.xroxy.com/proxy-country-US.htm has good ones to use)
#proxy = urllib2.ProxyHandler({'http': proxy_url})
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; v' + str(random.random())
#opener = urllib2.build_opener(proxy)
#opener.addheaders = [('User-agent', user_agent)]
#page_html = opener.open(url).read()

import re;

def remove_html(string):
    return re.sub("<.*?>", "", string)

def clean(string):
    return safestr(final_clean(strip_non_text(remove_html(string.strip()))))

def strip_non_text(string):
    return re.sub("\n|\r|&\w{3};|<.*?>",",",string)

def final_clean(string):
    return re.sub("[, ]{2,10}", ",", string)

def split_and_clean(string, delim):
    return ",".join(re.sub("[^a-zA-Z ]", "", rec, re.I) for rec in [clean(rec) for rec in string.split(delim) if rec.strip() != ""])

SAFESTR_RX = re.compile("^u\'(.+)\'$")
def safestr(string):
    try:
        return english_string(string).encode('utf-8', 'replace')
    except:
        return re.sub(SAFESTR_RX, '\1', repr(string))

# example scraper below

import scraperwiki
import lxml.html
import re
domaine = 'http://www.groceryretailonline.com'
s_url = 'http://www.groceryretailonline.com/BuyersGuide.mvc/CompanyDetail/452035'

def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    print html_content
    

scrape_site(s_url, domaine)

