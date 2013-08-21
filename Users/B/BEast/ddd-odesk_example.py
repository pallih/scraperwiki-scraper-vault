import scraperwiki
import re
print dir(re)

link = 'http://www.groceryretailonline.com/BuyersGuide.mvc/CompanyDetail/452035'
#print link

source = 'groceryretailonline.com'
#scraperwiki.sqlite.save_var('source', source)
#scraperwiki.sqlite.save_var('author', 'Dmitriy Severinov')
#scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))






# author: Clint Eastwood

# this is an example scraper, feel free to use lxml, soup or any other html parser (in this case pure regex - multi-threaded)
# the inserted data should use the schema listed here:
#
# if for a specific record, one of these fields is not found, use empty string "" as the record value
# only add the fields needed or provided by the page/scrape description

# use this to save each record to the sql database : scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

# for good practice, trim white space on the field values and use the cleaning functions provided below
# !!!!!make sure to use use safestr() to handle internatalization issues (can't write to sql datastore with i18n characters)!!!!!


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

domaine = 'http://www.groceryretailonline.com'
s_url = 'http://www.groceryretailonline.com/BuyersGuide.mvc/Sponsors'

scraperwiki.sqlite.save_var("source", "groceryretailonline.com")
scraperwiki.sqlite.save_var("author", "Sergey Batulin")
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
            #print abs_link
        for attempt in range(5):
            try:
                html_content = scraperwiki.scrape(s_url+'?Page='+str(p_num+1))
                p_num+=1
                break
            except:
                pass

def scrape_info(comp_link, num):
    my_data = []
    my_data.append(('id', num))
    my_data.append(('sourceurl', comp_link))
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
    root = lxml.html.fromstring(html_content)
    div = root.cssselect('div[id="col1_content"] ')[0]
    data_list = div.text_content().split('\r\n')
    #print data_list
    adress = data_list[4]+data_list[5]+data_list[6]
    my_data.append(('companyname', data_list[3]))
    my_data.append(('address', adress))
    for data in data_list[6:]:
        if re.search('Phone:',data):
            #print data
            contacts = data.split(':')
            try:
                my_data.append(('country', contacts[0][:-5]))
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
    my_data.append(('categories', cats[2:]))
    print my_data
    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

scrape_site(s_url, domaine)
