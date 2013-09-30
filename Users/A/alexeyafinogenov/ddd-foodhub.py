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


import scraperwiki
import lxml.html
import re
import datetime
import requests

domain = 'http://food-hub.org'
email = 'milanaromanova@list.ru'
pwd = 'milanaromanova'

scraperwiki.sqlite.save_var("source", "food-hub.org")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

def strip_non_text(string):
    return re.sub("\n|\r|\t|:","",string)


def scrape_site():
    request = login()
    for user_id in xrange(1, 12000):
        scrape_info(request, user_id)

def login():
    payload = {'data[User][email]': email, 'data[User][password]': pwd, 'data[keeploggedin]': 1}
    request = requests.post("http://food-hub.org/users/login", data=payload)
    return request

def scrape_info(request, user_id):
    url = 'http://food-hub.org/users/view/%s' % user_id
    request = requests.get(url, cookies=request.cookies)
    root = lxml.html.fromstring(request.text)
    header = root.cssselect('div[id="content"] h1')[0].text_content() 
    if 'This account is not active.' in header:
        return
    my_data = []
    my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))
    companyname = root.cssselect('div[class="editable no-margin"] h1')[0].text_content()
    my_data.append(('companyname ', companyname )) 
    print companyname 
    email = root.cssselect('div[id="hcard"] div[class="contact"] a[class="email"]')
    if email:
        email = email[0].text_content()
        my_data.append(('emails', email)) 
    website = root.cssselect('div[id="hcard"] div[class="adr"] span[class="website"] a[class="url"]')
    if website:
        website = website[0].text_content()
        my_data.append(('website', website)) 

    categories = root.cssselect('div[id="primary"] ul[class="breadcrumbs"] li')
    maincategory = ' > '.join([cat.text_content() for cat in categories[1:]])
    my_data.append(('maincategory', maincategory )) 
    categories = root.cssselect('div[id="user-data"] div[class="contact"] div[class="business-types"]')[0].text_content()
    categories = categories.split('Member since')[0].split(',')
    if len(categories) > 1:
        main_categories, categories = strip_non_text(categories[0]), strip_non_text(categories[1])
        my_data.append(('categories', categories)) 
    city = root.cssselect('div[id="hcard"] div[class="adr"] span[class="locality"]')
    if city:
        city = city[0].text_content()
        my_data.append(('city', city)) 
    state = root.cssselect('div[id="hcard"] div[class="adr"] span[class="region"]')
    if state:
        state = state[0].text_content()
        my_data.append(('state', state)) 
    zip = root.cssselect('div[id="hcard"] div[class="adr"] span[class="postal-code"]')
    if zip:
        zip = zip[0].text_content()
        my_data.append(('zip', zip)) 
    address = root.cssselect('div[id="hcard"] div[class="adr"] span[class="street-address"]')
    if address:
        address = address[0].text_content()
        my_data.append(('address', address))
    sourceurl = request.url
    my_data.append(('sourceurl', sourceurl)) 
    phonenumber = root.cssselect('div[id="hcard"] div[class="contact"] span[class="tel"]')
    if phonenumber:
        phonenumber = phonenumber[0].text_content()
        my_data.append(('phonenumber', phonenumber)) 
    contact = root.cssselect('div[id="hcard"] div[class="contact"]')
    if contact:
        contact = [strip_non_text(c) for c in contact[0].xpath('text()') if strip_non_text(c)]
        if contact:
            contact = contact[0].strip().split(' ')
            if len(contact) > 1:
                contact1first, contact1last = ' '.join(contact[:-1]).strip(), contact[-1]
                my_data.append(('contact1first', contact1first)) 
                my_data.append(('contact1last', contact1last)) 
            else:
                my_data.append(('contact1first', contact[0])) 
    description = root.cssselect('div[id="about-us"] p')[0].text_content()
    empty_descripion = 'Has Not Completed This Description.  Send Them A Message To Learn More.'
    if empty_descripion not in description.title():
        my_data.append(('description', description[:1000]))

    scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(my_data))

scrape_site()# author: Clint Eastwood

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


import scraperwiki
import lxml.html
import re
import datetime
import requests

domain = 'http://food-hub.org'
email = 'milanaromanova@list.ru'
pwd = 'milanaromanova'

scraperwiki.sqlite.save_var("source", "food-hub.org")
scraperwiki.sqlite.save_var("author", "Alexey Afinogenov")

def strip_non_text(string):
    return re.sub("\n|\r|\t|:","",string)


def scrape_site():
    request = login()
    for user_id in xrange(1, 12000):
        scrape_info(request, user_id)

def login():
    payload = {'data[User][email]': email, 'data[User][password]': pwd, 'data[keeploggedin]': 1}
    request = requests.post("http://food-hub.org/users/login", data=payload)
    return request

def scrape_info(request, user_id):
    url = 'http://food-hub.org/users/view/%s' % user_id
    request = requests.get(url, cookies=request.cookies)
    root = lxml.html.fromstring(request.text)
    header = root.cssselect('div[id="content"] h1')[0].text_content() 
    if 'This account is not active.' in header:
        return
    my_data = []
    my_data.append(('datescraped', datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")))
    companyname = root.cssselect('div[class="editable no-margin"] h1')[0].text_content()
    my_data.append(('companyname ', companyname )) 
    print companyname 
    email = root.cssselect('div[id="hcard"] div[class="contact"] a[class="email"]')
    if email:
        email = email[0].text_content()
        my_data.append(('emails', email)) 
    website = root.cssselect('div[id="hcard"] div[class="adr"] span[class="website"] a[class="url"]')
    if website:
        website = website[0].text_content()
        my_data.append(('website', website)) 

    categories = root.cssselect('div[id="primary"] ul[class="breadcrumbs"] li')
    maincategory = ' > '.join([cat.text_content() for cat in categories[1:]])
    my_data.append(('maincategory', maincategory )) 
    categories = root.cssselect('div[id="user-data"] div[class="contact"] div[class="business-types"]')[0].text_content()
    categories = categories.split('Member since')[0].split(',')
    if len(categories) > 1:
        main_categories, categories = strip_non_text(categories[0]), strip_non_text(categories[1])
        my_data.append(('categories', categories)) 
    city = root.cssselect('div[id="hcard"] div[class="adr"] span[class="locality"]')
    if city:
        city = city[0].text_content()
        my_data.append(('city', city)) 
    state = root.cssselect('div[id="hcard"] div[class="adr"] span[class="region"]')
    if state:
        state = state[0].text_content()
        my_data.append(('state', state)) 
    zip = root.cssselect('div[id="hcard"] div[class="adr"] span[class="postal-code"]')
    if zip:
        zip = zip[0].text_content()
        my_data.append(('zip', zip)) 
    address = root.cssselect('div[id="hcard"] div[class="adr"] span[class="street-address"]')
    if address:
        address = address[0].text_content()
        my_data.append(('address', address))
    sourceurl = request.url
    my_data.append(('sourceurl', sourceurl)) 
    phonenumber = root.cssselect('div[id="hcard"] div[class="contact"] span[class="tel"]')
    if phonenumber:
        phonenumber = phonenumber[0].text_content()
        my_data.append(('phonenumber', phonenumber)) 
    contact = root.cssselect('div[id="hcard"] div[class="contact"]')
    if contact:
        contact = [strip_non_text(c) for c in contact[0].xpath('text()') if strip_non_text(c)]
        if contact:
            contact = contact[0].strip().split(' ')
            if len(contact) > 1:
                contact1first, contact1last = ' '.join(contact[:-1]).strip(), contact[-1]
                my_data.append(('contact1first', contact1first)) 
                my_data.append(('contact1last', contact1last)) 
            else:
                my_data.append(('contact1first', contact[0])) 
    description = root.cssselect('div[id="about-us"] p')[0].text_content()
    empty_descripion = 'Has Not Completed This Description.  Send Them A Message To Learn More.'
    if empty_descripion not in description.title():
        my_data.append(('description', description[:1000]))

    scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(my_data))

scrape_site()