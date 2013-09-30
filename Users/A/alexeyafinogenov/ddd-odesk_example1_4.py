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
import datetime
domaine = 'http://www.groceryretailonline.com'
s_url = 'http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors'

scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")
def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    p_num=1
    r_num=0
    while True:
        root = lxml.html.fromstring(html_content)
        data_list = root.cssselect('div[id="col1_content"] div')
        if len(data_list)==0:
            print 'SPIDER-STOP'
            break
        for i in range(len(data_list)-1):
            rel_link = data_list[i].cssselect('a')[0].attrib.get('href')
            abs_link = domaine+rel_link
            scrape_info(abs_link, r_num)
            r_num+=1
            print abs_link
        for attempt in range(5):
            try:
                html_content = scraperwiki.scrape(s_url+'?Page='+str(p_num+1))
                p_num+=1
                break
            except:
                pass

def scrape_info(comp_link, num):
    my_data = []
    my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))
    my_data.append(('sourceurl', comp_link))
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
    root = lxml.html.fromstring(html_content)
    div = root.cssselect('div[id="col1_content"] ')[0]
    company_name = div.cssselect('span ')[0].text_content()
    my_data.append(('companyname', company_name))
    data_list = div.text_content().split('\r\n')
    adress = data_list[5]+data_list[6]
    my_data.append(('address', adress.strip()))
    for data in data_list[6:]:
        if re.search('Phone:',data):
            contacts = data.split(':')
            try:
                my_data.append(('country', contacts[0][:-5].strip()))
                my_data.append(('city', data_list[7].split(',')[0].strip()))
                my_data.append(('state', data_list[8].split('\\x')[0].strip()))
                my_data.append(('zip', data_list[9].strip()))
                my_data.append(('phonenumber', contacts[1][:-3]))
                my_data.append(('faxnumber', contacts[2][:-7]))
                if contacts[3].split()[0] != 'Products':
                    if '@' in contacts[3].split()[0]:
                        my_data.append(('emails', contacts[3].split()[1][:-8]))
                    else:
                        my_data.append(('contact1first', contacts[3].split()[0]))
                        my_data.append(('contact1last', contacts[3].split()[1][:-8]))
            except:
                pass
    m_cats=''
    m_categories = div.cssselect('li span.toplevelcategory')
    for m_cat in m_categories:
        m_cats=m_cats+', '+m_cat.text
    my_data.append(('maincategory', m_cats[2:]))
    categories = div.cssselect('li span')
    
    cats=''
    for cat in categories:
        cats=cats+', '+cat.text
    print cats
    my_data.append(('categories', cats[2:]))
    print my_data
    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

scrape_site(s_url, domaine)# author: Clint Eastwood

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
import datetime
domaine = 'http://www.groceryretailonline.com'
s_url = 'http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors'

scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")
def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    p_num=1
    r_num=0
    while True:
        root = lxml.html.fromstring(html_content)
        data_list = root.cssselect('div[id="col1_content"] div')
        if len(data_list)==0:
            print 'SPIDER-STOP'
            break
        for i in range(len(data_list)-1):
            rel_link = data_list[i].cssselect('a')[0].attrib.get('href')
            abs_link = domaine+rel_link
            scrape_info(abs_link, r_num)
            r_num+=1
            print abs_link
        for attempt in range(5):
            try:
                html_content = scraperwiki.scrape(s_url+'?Page='+str(p_num+1))
                p_num+=1
                break
            except:
                pass

def scrape_info(comp_link, num):
    my_data = []
    my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))
    my_data.append(('sourceurl', comp_link))
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
    root = lxml.html.fromstring(html_content)
    div = root.cssselect('div[id="col1_content"] ')[0]
    company_name = div.cssselect('span ')[0].text_content()
    my_data.append(('companyname', company_name))
    data_list = div.text_content().split('\r\n')
    adress = data_list[5]+data_list[6]
    my_data.append(('address', adress.strip()))
    for data in data_list[6:]:
        if re.search('Phone:',data):
            contacts = data.split(':')
            try:
                my_data.append(('country', contacts[0][:-5].strip()))
                my_data.append(('city', data_list[7].split(',')[0].strip()))
                my_data.append(('state', data_list[8].split('\\x')[0].strip()))
                my_data.append(('zip', data_list[9].strip()))
                my_data.append(('phonenumber', contacts[1][:-3]))
                my_data.append(('faxnumber', contacts[2][:-7]))
                if contacts[3].split()[0] != 'Products':
                    if '@' in contacts[3].split()[0]:
                        my_data.append(('emails', contacts[3].split()[1][:-8]))
                    else:
                        my_data.append(('contact1first', contacts[3].split()[0]))
                        my_data.append(('contact1last', contacts[3].split()[1][:-8]))
            except:
                pass
    m_cats=''
    m_categories = div.cssselect('li span.toplevelcategory')
    for m_cat in m_categories:
        m_cats=m_cats+', '+m_cat.text
    my_data.append(('maincategory', m_cats[2:]))
    categories = div.cssselect('li span')
    
    cats=''
    for cat in categories:
        cats=cats+', '+cat.text
    print cats
    my_data.append(('categories', cats[2:]))
    print my_data
    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

scrape_site(s_url, domaine)